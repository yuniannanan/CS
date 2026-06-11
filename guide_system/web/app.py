# -*- coding: utf-8 -*-
"""
智能导医系统 - Web 版本 Flask 后端
"""

import sys
import os
from pathlib import Path

# 确保项目根目录在 Python 路径中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 切换到项目根目录，确保 config.ini 和 guide_system.db 能被找到
os.chdir(str(project_root))

from flask import Flask, request, jsonify, render_template

from models.database import DatabaseManager
from core.symptom_extractor import SymptomExtractor
from core.expert_system import ExpertSystem

# 导入医院场景模型
from models.hospital_map import HOSPITAL_MODEL

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

# 使用绝对路径初始化数据库
config_path = str(project_root / "config.ini")
database = DatabaseManager(config_path)
extractor = SymptomExtractor(database)
expert = ExpertSystem(database)

# 启动时加载数据
extractor.load_symptom_library()
expert.load_rules()

# 预加载 Whisper 模型（避免首次请求超时）
print("Pre-loading Whisper model (may take 5-10s)...")
try:
    from core.whisper_asr import _get_model
    _get_model()
    print("Whisper model loaded successfully")
except Exception as e:
    print("Whisper preload warning:", e)


# ---- API 路由 ----

@app.route("/")
def index():
    """首页"""
    return render_template("index.html")


@app.route("/api/diagnose", methods=["POST"])
def diagnose():
    """症状分诊接口"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "请输入症状描述"}), 400

    text = data.get("text", "").strip()
    if not text:
        return jsonify({"success": False, "message": "症状描述不能为空"}), 400

    # 1. 提取症状
    extract_result = extractor.extract_symptoms(text)
    if not extract_result["success"]:
        return jsonify({"success": False, "message": extract_result["message"]}), 200

    symptoms = extract_result["data"]["symptoms"]

    # 2. 保存记录
    symptoms_json = str([s["name"] for s in symptoms])
    database.execute_update(
        "INSERT INTO records (create_time, input_text, matched_symptoms, recommended_dept, confidence) "
        "VALUES (datetime('now'), ?, ?, NULL, 0)",
        (text, symptoms_json)
    )

    # 3. 专家系统分诊
    diagnose_result = expert.diagnose(symptoms)
    if not diagnose_result["success"]:
        return jsonify({"success": False, "message": diagnose_result["message"]}), 200

    primary = diagnose_result["data"]["primary"]
    dept_id = primary.get("dept_id", 0)

    # 4. 更新记录
    database.execute_update(
        "UPDATE records SET recommended_dept = ?, confidence = ? "
        "WHERE record_id = (SELECT MAX(record_id) FROM records)",
        (dept_id, primary.get("confidence", 0))
    )

    # 5. 查询科室详情
    dept_data = database.execute_query(
        "SELECT dept_name, floor, location_desc FROM departments WHERE dept_id = ?",
        (dept_id,)
    )
    if dept_data:
        primary["dept_name"] = dept_data[0]["dept_name"]
        primary["floor"] = dept_data[0]["floor"]
        primary["location_desc"] = dept_data[0]["location_desc"]

    return jsonify({
        "success": True,
        "version": "v2-enhanced",
        "data": {
            "primary": primary,
            "alternatives": diagnose_result["data"].get("alternatives", []),
            "symptoms": symptoms,
            "symptom_summary": diagnose_result["data"].get("symptom_summary", {}),
            "matched_rules": diagnose_result["data"].get("matched_rules", []),
        },
        "message": "分诊完成"
    })


@app.route("/api/voice", methods=["POST"])
def voice_recognize():
    """语音识别 — 离线Whisper，支持WAV/PCM自动检测"""
    audio_data = request.get_data()
    if not audio_data or len(audio_data) < 400:
        return jsonify({"success": False, "message": "音频太短，请长按说话至少1秒"}), 400

    # 自动检测格式：WAV 以 "RIFF" 开头，否则当作 PCM
    fmt = "wav" if audio_data[:4] == b"RIFF" else "pcm"

    try:
        from core.whisper_asr import recognize
        result = recognize(audio_data, fmt=fmt)
        return jsonify(result)
    except ImportError:
        return jsonify({
            "success": False, "message": "语音模块未安装，请运行: pip install openai-whisper scipy"
        }), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/route/<int:dept_id>", methods=["GET"])
def get_route(dept_id):
    """获取导航路线"""
    dept_data = database.execute_query(
        "SELECT * FROM departments WHERE dept_id = ?",
        (dept_id,)
    )
    if not dept_data:
        return jsonify({"success": False, "message": "未找到科室信息"}), 404

    dept = dept_data[0]
    steps = _build_route(dept)
    return jsonify({
        "success": True,
        "data": {
            "dept_name": dept["dept_name"],
            "floor": dept["floor"],
            "location_desc": dept["location_desc"],
            "steps": steps
        }
    })


@app.route("/api/departments", methods=["GET"])
def list_departments():
    """获取所有科室列表"""
    depts = database.execute_query("SELECT * FROM departments ORDER BY dept_id")
    return jsonify({"success": True, "data": depts})


@app.route("/api/history", methods=["GET"])
def get_history():
    """获取历史记录"""
    try:
        records = database.execute_query(
            "SELECT r.*, d.dept_name FROM records r "
            "LEFT JOIN departments d ON r.recommended_dept = d.dept_id "
            "ORDER BY r.record_id DESC LIMIT 20"
        )
        return jsonify({"success": True, "data": records})
    except Exception:
        records = database.execute_query(
            "SELECT * FROM records ORDER BY record_id DESC LIMIT 20"
        )
        return jsonify({"success": True, "data": records})


@app.route("/api/rules", methods=["GET", "POST", "PUT", "DELETE"])
def manage_rules():
    """
    规则管理接口
    GET: 获取所有规则（支持 ?type=single|compound|exclusion）
    POST: 新增规则
    PUT: 更新规则（需 ?rule_id=）
    DELETE: 删除规则（需 ?rule_id=）
    """
    if request.method == "GET":
        rule_type = request.args.get("type", "all")
        if rule_type == "all":
            rules = database.execute_query("SELECT * FROM rules ORDER BY rule_id")
        else:
            rules = database.execute_query(
                "SELECT * FROM rules WHERE rule_type=? ORDER BY rule_id", (rule_type,)
            )
        # 补充症状名和科室名
        symptom_names = {s["symptom_id"]: s["symptom_name"]
                        for s in database.execute_query("SELECT symptom_id, symptom_name FROM symptoms")}
        dept_names = {d["dept_id"]: d["dept_name"]
                     for d in database.execute_query("SELECT dept_id, dept_name FROM departments")}
        for r in rules:
            r["symptom_name"] = symptom_names.get(r["symptom_id"], f"症状#{r['symptom_id']}")
            r["dept_name"] = dept_names.get(r["dept_id"], f"科室#{r['dept_id']}")
        return jsonify({"success": True, "data": rules, "total": len(rules)})

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "缺少规则数据"}), 400
        try:
            import json as j
            extra_sids = j.dumps(data.get("extra_symptom_ids", []))
            rid = database.execute_insert(
                "INSERT INTO rules (symptom_id, dept_id, rule_weight, conditions, severity, "
                "rule_type, extra_symptom_ids, conditions_detail, is_active) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (data["symptom_id"], data["dept_id"], data.get("rule_weight", 1.0),
                 data.get("conditions", ""), data.get("severity", "medium"),
                 data.get("rule_type", "single"), extra_sids,
                 data.get("conditions_detail", ""), data.get("is_active", 1))
            )
            return jsonify({"success": True, "data": {"rule_id": rid}, "message": "规则添加成功"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    elif request.method == "PUT":
        rule_id = request.args.get("rule_id")
        if not rule_id:
            return jsonify({"success": False, "message": "缺少 rule_id"}), 400
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "缺少更新数据"}), 400
        try:
            import json as j
            extra_sids = j.dumps(data.get("extra_symptom_ids", "[]"))
            database.execute_update(
                "UPDATE rules SET symptom_id=?, dept_id=?, rule_weight=?, conditions=?, "
                "severity=?, rule_type=?, extra_symptom_ids=?, conditions_detail=?, is_active=? "
                "WHERE rule_id=?",
                (data.get("symptom_id"), data.get("dept_id"), data.get("rule_weight"),
                 data.get("conditions"), data.get("severity"), data.get("rule_type"),
                 extra_sids, data.get("conditions_detail", ""),
                 data.get("is_active", 1), int(rule_id))
            )
            return jsonify({"success": True, "message": "规则更新成功"})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    elif request.method == "DELETE":
        rule_id = request.args.get("rule_id")
        if not rule_id:
            return jsonify({"success": False, "message": "缺少 rule_id"}), 400
        database.execute_update("DELETE FROM rules WHERE rule_id=?", (int(rule_id),))
        return jsonify({"success": True, "message": "规则已删除"})


@app.route("/api/symptoms", methods=["GET"])
def list_symptoms():
    """获取所有症状列表"""
    symptoms = database.execute_query("SELECT * FROM symptoms ORDER BY symptom_id")
    return jsonify({"success": True, "data": symptoms})


@app.route("/api/hospital/map", methods=["GET"])
def get_hospital_map():
    """获取医院场景地图模型"""
    return jsonify({"success": True, "data": HOSPITAL_MODEL})


@app.route("/api/hospital/floor/<int:floor>", methods=["GET"])
def get_floor(floor):
    """获取指定楼层布局"""
    if floor not in HOSPITAL_MODEL["floors_data"]:
        return jsonify({"success": False, "message": "楼层不存在"}), 404
    return jsonify({
        "success": True,
        "data": {
            "floor": floor,
            "name": HOSPITAL_MODEL["floors_data"][floor]["name"],
            "departments": HOSPITAL_MODEL["floors_data"][floor]["departments"],
            "facilities": HOSPITAL_MODEL["floors_data"][floor]["facilities"],
            "note": HOSPITAL_MODEL["floors_data"][floor]["note"],
            "entrance": HOSPITAL_MODEL["entrance"],
            "elevator": HOSPITAL_MODEL["elevator"],
        }
    })


@app.route("/api/hospital/route/<int:dept_id>", methods=["GET"])
def get_hospital_route(dept_id):
    """获取从入口到目标科室的导航路线"""
    # 查找科室所在楼层
    target_floor = None
    target_dept = None
    for floor_num, floor_data in HOSPITAL_MODEL["floors_data"].items():
        for dept in floor_data["departments"]:
            if dept["id"] == dept_id:
                target_floor = floor_num
                target_dept = dept
                break
        if target_floor:
            break

    if not target_dept:
        return jsonify({"success": False, "message": "科室未找到"}), 404

    entrance = HOSPITAL_MODEL["entrance"]
    elevator = HOSPITAL_MODEL["elevator"]

    # 构建导航步骤
    steps = []
    segments = []

    if target_floor == 1:
        # 同楼层：入口→导诊台→目标科室
        steps = [
            f"从正门进入1楼大厅",
            f"前往大厅中央的导诊台（ℹ 导诊台）确认挂号信息",
            f"从导诊台前往「{target_dept['name']}」诊区（{target_dept['name']}在1楼{('东侧' if target_dept['x']<300 else '北侧') if target_dept['x']<400 else '西侧'}）",
            f"到达「{target_dept['name']}」，向护士报到就诊"
        ]
        segments = [
            {"from": entrance, "to": {"x": 470, "y": 460}},  # 入口→导诊台
            {"from": {"x": 470, "y": 460}, "to": {"x": target_dept["x"] + target_dept["w"]//2, "y": target_dept["y"] + target_dept["h"]//2}},
        ]
    else:
        steps = [
            f"从正门进入1楼大厅",
            f"前往大厅中央导诊台（ℹ 导诊台）或挂号处（🏷 挂号处）",
            f"乘坐电梯（📍电梯）前往{target_floor}楼",
            f"到达{target_floor}楼后，根据指示牌找到「{target_dept['name']}」",
            f"到达「{target_dept['name']}」，向护士报到就诊"
        ]
        segments = [
            {"from": entrance, "to": {"x": 470, "y": 460}},  # 入口→导诊台
            {"from": {"x": 470, "y": 460}, "to": elevator},     # 导诊台→电梯
        ]

    return jsonify({
        "success": True,
        "data": {
            "dept_name": target_dept["name"],
            "floor": target_floor,
            "floor_name": HOSPITAL_MODEL["floors_data"][target_floor]["name"],
            "dept_position": {"x": target_dept["x"], "y": target_dept["y"], "w": target_dept["w"], "h": target_dept["h"]},
            "steps": steps,
            "segments": segments,
            "entrance": entrance,
            "elevator": elevator,
        }
    })


# ---- 辅助函数 ----

def _build_route(dept: dict) -> list:
    """生成导航路线步骤"""
    steps = []
    name = dept.get("dept_name", "目标科室")
    floor = dept.get("floor", 1)
    location = dept.get("location_desc", "")

    steps.append("从医院正门进入大厅，前往导诊台")
    if floor == 1:
        steps.append("在1楼大厅找到指示牌")
    else:
        steps.append("乘坐电梯或走楼梯前往{}楼".format(int(floor)))
    if location:
        steps.append("按指示牌前往「{}」".format(location))
    steps.append("到达「{}」，向护士报到就诊".format(name))
    return steps


# ---- 启动 ----

if __name__ == "__main__":
    import ssl

    cert_file = project_root / "cert.pem"
    key_file = project_root / "key.pem"

    print("=" * 55)
    print("  智能导医系统 - Web 版")
    print("=" * 55)

    if cert_file.exists() and key_file.exists():
        # HTTPS 模式 — 手机端可正常使用语音识别
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(str(cert_file), str(key_file))

        print("  电脑:  https://127.0.0.1:8443")
        print("  手机:  https://192.168.31.113:8443")
        print("")
        print("  ! 自签名证书，手机端打开后点击「高级→继续访问」")
        print("  ! 首次需在弹窗中允许麦克风权限")
        print("=" * 55)

        app.run(host="0.0.0.0", port=8443, ssl_context=context, debug=False)
    else:
        # HTTP 回退 — 仅电脑Chrome可用语音（localhost豁免HTTPS）
        print("  http://127.0.0.1:5000")
        print("  (未找到SSL证书，HTTP回退模式)")
        print("=" * 55)
        app.run(host="0.0.0.0", port=5000, debug=True)
