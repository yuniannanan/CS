import markdown
import subprocess
import os

md_path = "C:/Users/LiangYaoHui/Desktop/课程设计/智能导医系统架构设计.md"
html_path = "C:/Users/LiangYaoHui/Desktop/课程设计/智能导医系统架构设计.html"
pdf_path = "C:/Users/LiangYaoHui/Desktop/课程设计/智能导医系统架构设计.pdf"

# 读取markdown内容
with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# 配置markdown扩展
md = markdown.Markdown(extensions=[
    "tables",
    "fenced_code",
    "toc",
    "nl2br",
    "pymdownx.superfences",
    "pymdownx.highlight"
])

html_body = md.convert(md_content)

# 构建完整HTML，包含CJK字体支持样式
css_style = """
<style>
@page {
    size: A4;
    margin: 1.5cm 1.5cm;
}
body {
    font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #333;
    max-width: 100%;
}
h1 {
    font-size: 22pt;
    color: #1a1a1a;
    border-bottom: 2px solid #1890FF;
    padding-bottom: 8px;
    margin-top: 30pt;
    page-break-before: always;
}
h1:first-of-type {
    page-break-before: auto;
}
h2 {
    font-size: 16pt;
    color: #2c2c2c;
    border-left: 4px solid #1890FF;
    padding-left: 12px;
    margin-top: 24pt;
}
h3 {
    font-size: 13pt;
    color: #333;
    margin-top: 18pt;
}
h4 {
    font-size: 11.5pt;
    color: #444;
    margin-top: 14pt;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
    font-size: 10pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 8px 10px;
    text-align: left;
}
th {
    background-color: #f0f5ff;
    font-weight: bold;
}
tr:nth-child(even) {
    background-color: #fafafa;
}
code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 10pt;
}
pre {
    background-color: #f8f8f8;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    border-left: 3px solid #1890FF;
}
pre code {
    background-color: transparent;
    padding: 0;
}
blockquote {
    border-left: 4px solid #52C41A;
    margin: 10pt 0;
    padding: 8px 16px;
    background-color: #f6ffed;
    color: #333;
}
ul, ol {
    margin: 8pt 0;
    padding-left: 24pt;
}
li {
    margin: 4pt 0;
}
strong {
    color: #1a1a1a;
}
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 20pt 0;
}
a {
    color: #1890FF;
    text-decoration: none;
}
.toc {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 4px;
    margin-bottom: 20pt;
}
.mermaid {
    display: none;
}
img {
    display: block;
    max-width: 100%;
    width: 100%;
    height: auto;
    margin: 12pt auto;
    image-rendering: auto;
}
p:has(img) {
    text-align: center;
}
p img + em,
p img + br + em {
    display: block;
    text-align: center;
    font-size: 9pt;
    color: #888;
    margin-top: 6pt;
}
</style>
"""

html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=2480, initial-scale=1">
    <title>智能导医系统架构设计文档</title>
    {css_style}
</head>
<body>
{html_body}
</body>
</html>
"""

# 保存HTML文件
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_full)

print(f"HTML已生成: {html_path}")

# 使用Edge浏览器headless模式打印PDF
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    f"--print-to-pdf-no-header",
    f"file:///{html_path.replace(':', '|').replace('/', '\\')}"
]

# 修正file协议路径
file_url = "file:///" + html_path.replace("\\", "/")

cmd = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=2480,3508",
    f"--print-to-pdf={pdf_path}",
    "--run-all-compositor-stages-before-draw",
    file_url
]

print(f"正在生成PDF: {pdf_path}")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path)
    print(f"PDF生成成功! 文件大小: {size / 1024:.1f} KB")
else:
    print(f"PDF生成失败")
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
