import os
import sys
import base64
import subprocess
import markdown

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def generate_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(base_dir, "PRODUCE_VISION_GUIDE.md")
    img_path = os.path.join(base_dir, "assets", "producevision_ad_banner.jpg")
    html_out = os.path.join(base_dir, "PRODUCE_VISION_GUIDE.html")
    pdf_out = os.path.join(base_dir, "ProduceVision_Studio_Pro_Technical_Guide.pdf")

    print(f"Reading {md_path}...")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert banner image to base64 data URI
    img_b64_uri = ""
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode("utf-8")
            img_b64_uri = f"data:image/jpeg;base64,{b64_data}"
        md_text = md_text.replace("assets/producevision_ad_banner.jpg", img_b64_uri)

    # Convert Markdown to HTML
    html_content = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"]
    )

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ProduceVision Studio Pro — Technical User Manual & Detection Guide</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 16mm 18mm 16mm;
        @bottom-right {{
            content: "Page " counter(page);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 8pt;
            color: #64748B;
        }}
        @bottom-left {{
            content: "ProduceVision Studio Pro · Enterprise Detection Manual";
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 8pt;
            color: #64748B;
        }}
    }}

    *, *::before, *::after {{
        box-sizing: border-box;
    }}

    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #0F172A;
        line-height: 1.6;
        font-size: 10pt;
        background: #FFFFFF;
        margin: 0;
        padding: 0;
    }}

    h1, h2, h3, h4, h5 {{
        color: #0F172A;
        font-weight: 800;
        line-height: 1.25;
        margin-top: 1.4em;
        margin-bottom: 0.5em;
    }}

    h1 {{
        font-size: 20pt;
        color: #047857;
        border-bottom: 3px solid #10B981;
        padding-bottom: 6px;
        margin-top: 0;
    }}

    h2 {{
        font-size: 14pt;
        color: #0F766E;
        border-bottom: 1.5px solid #CBD5E1;
        padding-bottom: 4px;
        page-break-after: avoid;
        margin-top: 1.8em;
    }}

    h3 {{
        font-size: 11.5pt;
        color: #1E293B;
        page-break-after: avoid;
    }}

    p {{
        margin-top: 0;
        margin-bottom: 0.8em;
        color: #334155;
    }}

    img {{
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
        margin: 12px 0 16px 0;
        display: block;
    }}

    blockquote {{
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        margin: 12px 0;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        color: #065F46;
        font-size: 9.5pt;
    }}

    blockquote strong {{
        color: #047857;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 8.5pt;
        page-break-inside: avoid;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        overflow: hidden;
    }}

    th {{
        background-color: #0F172A;
        color: #F8FAFC;
        text-align: left;
        padding: 8px 10px;
        font-weight: 700;
        letter-spacing: 0.02em;
        border: 1px solid #334155;
    }}

    td {{
        padding: 7px 10px;
        border: 1px solid #E2E8F0;
        color: #1E293B;
        vertical-align: top;
    }}

    tr:nth-child(even) {{
        background-color: #F8FAFC;
    }}

    code {{
        background: #F1F5F9;
        color: #0F766E;
        padding: 2px 5px;
        border-radius: 4px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
        border: 1px solid #E2E8F0;
    }}

    pre {{
        background: #0B1329;
        color: #E2E8F0;
        padding: 12px 14px;
        border-radius: 6px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 8.5pt;
        line-height: 1.45;
        overflow-x: auto;
        margin: 10px 0;
        page-break-inside: avoid;
        border: 1px solid #1E293B;
    }}

    pre code {{
        background: transparent;
        color: inherit;
        padding: 0;
        border: none;
    }}

    ul, ol {{
        margin-top: 0;
        margin-bottom: 0.8em;
        padding-left: 20px;
        color: #334155;
    }}

    li {{
        margin-bottom: 4px;
    }}

    hr {{
        border: none;
        height: 1px;
        background: #E2E8F0;
        margin: 20px 0;
    }}

    .page-break {{
        page-break-before: always;
    }}

    .badge {{
        display: inline-block;
        background: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
        padding: 2px 8px;
        border-radius: 99px;
        font-size: 7.5pt;
        font-weight: 700;
        margin-right: 4px;
    }}

    .footer-note {{
        margin-top: 30px;
        padding: 14px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        text-align: center;
        font-size: 8.5pt;
        color: #64748B;
    }}
</style>
</head>
<body>
{html_content}

<div class="footer-note">
    <strong>ProduceVision Studio Pro</strong> · Open-Source Computer Vision System · 
    <a href="https://huggingface.co/spaces/NEwBEE67/FruitnVeg" style="color: #059669; text-decoration: none;">Live Demo</a> · 
    <a href="https://github.com/DeathSHMASHER/Fruit-and-veg-" style="color: #059669; text-decoration: none;">GitHub Repository</a>
</div>
</body>
</html>
"""

    print(f"Writing {html_out}...")
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Compile to PDF using Microsoft Edge headless
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            browser_exe = p
            break

    if not browser_exe:
        print("❌ Error: Could not find Edge or Chrome browser executable.")
        sys.exit(1)

    print(f"Compiling PDF via {browser_exe}...")
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_out}",
        html_out
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_out) and os.path.getsize(pdf_out) > 1000:
        size_kb = os.path.getsize(pdf_out) / 1024
        print(f"✅ PDF successfully created: {pdf_out} ({size_kb:.1f} KB)")
    else:
        print(f"❌ Failed to create PDF. Stdout: {res.stdout}, Stderr: {res.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    generate_pdf()
