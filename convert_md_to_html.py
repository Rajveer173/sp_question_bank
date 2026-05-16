import markdown

# Read markdown file
with open('Compiler_Design_Question_Bank_THEORY_NUMERICALS_ONLY.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert to HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'extra', 'codehilite'])

# Create full HTML document with styling
full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Compiler Design - Question Bank</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
        h3 {{ color: #7f8c8d; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            border: 1px solid #bdc3c7;
            padding: 10px;
        }}
        tr:nth-child(even) {{
            background-color: #ecf0f1;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #c7254e;
        }}
        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            line-height: 1.4;
        }}
        pre code {{
            color: #ecf0f1;
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 15px 0;
            padding-left: 15px;
            color: #7f8c8d;
        }}
        .page-break {{
            page-break-after: always;
        }}
        @media print {{
            body {{ margin: 0; padding: 20px; }}
            h1 {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

# Write HTML file
with open('Compiler_Design_Theory_Numericals.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("✓ Markdown converted to HTML successfully!")
print("  File: Compiler_Design_Theory_Numericals.html")
