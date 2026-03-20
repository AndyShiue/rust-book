"""Merge chapter markdown files into a single styled HTML book with mobile TOC."""
import markdown
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
OUT = BASE / "rust_book.html"

CHAPTERS = [
    ("第一章：基礎", "chapter1"),
    ("第二章：函數、陣列與切片", "chapter2"),
    ("第三章：Struct、Enum 與 Pattern Matching", "chapter3"),
    ("第四章：所有權與借用", "chapter4"),
    ("第五章：泛型、Trait Bound 與生命週期", "chapter5"),
    ("第六章：閉包與迭代器", "chapter6"),
]

parts = []
for title, folder in CHAPTERS:
    parts.append(f"# {title}\n\n")
    chapter_dir = BASE / folder
    files = sorted(chapter_dir.glob("*.md"))
    for f in files:
        text = f.read_text(encoding="utf-8")
        # Insert blank line before list items that follow a line ending with fullwidth colon
        text = re.sub(r'(：\s*)\n(- )', r'\1\n\n\2', text)
        # Demote all headings by one level so chapter title stays h1
        text = re.sub(r"^##### ", "###### ", text, flags=re.MULTILINE)
        text = re.sub(r"^#### ", "##### ", text, flags=re.MULTILINE)
        text = re.sub(r"^### ", "#### ", text, flags=re.MULTILINE)
        text = re.sub(r"^## ", "### ", text, flags=re.MULTILINE)
        text = re.sub(r"^# ", "## ", text, flags=re.MULTILINE)
        parts.append(text)
        parts.append("\n\n---\n\n")

merged = "\n".join(parts)

# Escape < and > outside of code blocks/inline code so markdown doesn't eat them as HTML tags
def escape_angles_outside_code(text):
    """Replace < > with &lt; &gt; except inside ``` fenced code blocks and `inline code`."""
    result = []
    lines = text.split('\n')
    in_code_block = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if in_code_block:
            result.append(line)
            continue
        # Outside code block: escape < > but preserve inline code
        parts_line = re.split(r'(`[^`]+`)', line)
        escaped_parts = []
        for part in parts_line:
            if part.startswith('`') and part.endswith('`'):
                escaped_parts.append(part)  # inline code, keep as-is
            else:
                escaped_parts.append(part.replace('<', '&lt;').replace('>', '&gt;'))
        result.append(''.join(escaped_parts))
    return '\n'.join(result)

merged = escape_angles_outside_code(merged)

md = markdown.Markdown(extensions=[
    "fenced_code",
    "codehilite",
    "tables",
    "toc",
], extension_configs={
    "codehilite": {"css_class": "highlight", "guess_lang": False},
    "toc": {"permalink": False, "toc_depth": 2},
})

body = md.convert(merged)
toc = md.toc

html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rust 教學</title>
<style>
  :root {{
    --bg: #1e1e2e;
    --surface: #252536;
    --text: #cdd6f4;
    --heading: #89b4fa;
    --accent: #f9e2af;
    --green: #a6e3a1;
    --red: #f38ba8;
    --comment: #6c7086;
    --code-bg: #181825;
    --link: #89dceb;
    --border: #313244;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: "Noto Sans TC", "Segoe UI", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    font-size: 17px;
    overflow-wrap: break-word;
    word-break: break-word;
  }}

  code {{
    overflow-wrap: break-word;
    word-break: break-all;
  }}

  h1, h2, h3, h4, h5, h6 {{
    overflow-wrap: break-word;
    word-break: break-word;
  }}

  /* Drawer TOC */
  .drawer-toggle {{
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 100;
    background: var(--surface);
    color: var(--accent);
    border: 1px solid var(--border);
    border-radius: 8px;
    width: 44px;
    height: 44px;
    font-size: 22px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}

  .drawer-overlay {{
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 40;
  }}

  .drawer-overlay.open {{
    display: block;
  }}

  .drawer {{
    position: fixed;
    top: 0;
    left: -320px;
    width: 300px;
    height: 100vh;
    background: var(--surface);
    border-right: 1px solid var(--border);
    z-index: 50;
    overflow-y: auto;
    padding: 24px 16px;
    transition: left 0.25s ease;
  }}

  .drawer.open {{
    left: 0;
  }}

  .drawer h2 {{
    color: var(--accent);
    font-size: 18px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}

  .drawer ul {{
    list-style: none;
    padding-left: 0;
  }}

  .drawer > div > ul > li {{
    margin-bottom: 4px;
  }}

  .drawer ul ul {{
    padding-left: 16px;
  }}

  .drawer a {{
    color: var(--text);
    text-decoration: none;
    font-size: 14px;
    display: block;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background 0.15s;
  }}

  .drawer a:hover {{
    background: var(--border);
    color: var(--link);
  }}

  /* Main content */
  .content {{
    max-width: 800px;
    margin: 0 auto;
    padding: 48px 48px 96px;
  }}

  h1 {{
    color: var(--accent);
    font-size: 2.2em;
    margin-bottom: 8px;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 12px;
  }}

  h2 {{
    color: var(--heading);
    font-size: 1.7em;
    margin-top: 64px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}

  h3 {{
    color: var(--green);
    font-size: 1.35em;
    margin-top: 48px;
    margin-bottom: 12px;
  }}

  h4 {{
    color: var(--accent);
    font-size: 1.1em;
    margin-top: 32px;
    margin-bottom: 8px;
  }}

  p {{
    margin-bottom: 16px;
  }}

  a {{
    color: var(--link);
  }}

  strong {{
    color: var(--accent);
  }}

  code {{
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "Consolas", "Fira Code", monospace;
    font-size: 0.9em;
    color: var(--green);
  }}

  pre {{
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    overflow-x: auto;
    margin-bottom: 20px;
    line-height: 1.5;
  }}

  pre code {{
    background: none;
    padding: 0;
    color: var(--text);
    font-size: 15px;
  }}

  .highlight {{ background: var(--code-bg); }}
  .highlight .k, .highlight .kd, .highlight .kn {{ color: #cba6f7; }}
  .highlight .kt {{ color: #89b4fa; }}
  .highlight .s, .highlight .s2, .highlight .s1 {{ color: #a6e3a1; }}
  .highlight .mi, .highlight .mf {{ color: #fab387; }}
  .highlight .c, .highlight .c1, .highlight .cm {{ color: #6c7086; font-style: italic; }}
  .highlight .n {{ color: #cdd6f4; }}
  .highlight .nf, .highlight .fm {{ color: #89dceb; }}
  .highlight .nb {{ color: #f9e2af; }}
  .highlight .o {{ color: #89dceb; }}
  .highlight .p {{ color: #cdd6f4; }}
  .highlight .bp {{ color: #f38ba8; }}

  ul, ol {{
    margin-bottom: 16px;
    padding-left: 28px;
  }}

  li {{
    margin-bottom: 4px;
  }}

  hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 48px 0;
  }}

  table {{
    border-collapse: collapse;
    margin-bottom: 20px;
    width: 100%;
  }}

  th, td {{
    border: 1px solid var(--border);
    padding: 8px 12px;
    text-align: left;
  }}

  th {{
    background: var(--surface);
    color: var(--accent);
  }}

  blockquote {{
    border-left: 3px solid var(--accent);
    padding-left: 16px;
    color: var(--comment);
    margin-bottom: 16px;
  }}

  /* Mobile */
  @media (max-width: 900px) {{
    .content {{
      padding: 24px 20px 64px;
    }}
  }}
</style>
</head>
<body>
<button class="drawer-toggle" onclick="toggleDrawer()">☰</button>
<div id="drawerOverlay" class="drawer-overlay" onclick="toggleDrawer()"></div>
<nav id="drawer" class="drawer">
  <h2>📖 目錄</h2>
  <div>{toc}</div>
</nav>
<main class="content">
  {body}
</main>

<script>
function toggleDrawer() {{
  document.getElementById('drawer').classList.toggle('open');
  document.getElementById('drawerOverlay').classList.toggle('open');
}}
document.getElementById('drawer').addEventListener('click', function(e) {{
  if (e.target.tagName === 'A') {{
    toggleDrawer();
  }}
}});
</script>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
size_kb = OUT.stat().st_size / 1024
print(f"Done: {OUT.name} ({size_kb:.0f} KB)")
