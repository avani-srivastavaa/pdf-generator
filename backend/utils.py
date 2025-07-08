from jinja2 import Environment, FileSystemLoader
import pdfkit
import uuid
import os
from datetime import datetime, timedelta

# Set up base path and Jinja environment
base_dir = os.path.abspath(os.path.dirname(__file__))
template_path = os.path.join(base_dir, 'templates')
env = Environment(loader=FileSystemLoader(template_path))

def render_pdf(data):
    doc_type = data.get("type")
    if not doc_type:
        raise ValueError("Missing document type")

    template_file = f"{doc_type}.html"
    try:
        template = env.get_template(template_file)
    except Exception as e:
        raise FileNotFoundError(f"Template '{template_file}' not found: {e}")

    # Inject absolute path for local image references
    # data["os_path"] = base_dir.replace("\\", "/")  # ensure path works on Windows

    print("Resolved background path:", f"{data['os_path']}/static/images/background.png")

    # Parse and calculate 'to_date' (3 months from 'from_date')
    try:
        print("RECEIVED DATA:", data)
        from_date = datetime.strptime(data.get("from_date"), "%Y-%m-%d")
        to_date = from_date + timedelta(days=90)
        data["to_date"] = to_date.strftime("%Y-%m-%d")
    except Exception:
        data["to_date"] = "---"

    # Render HTML using Jinja
    html_out = template.render(data=data)

    # Create output path
    output_dir = os.path.join(base_dir, "generated")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{uuid.uuid4().hex}.pdf")

    # Generate PDF with image access + zero margins
    pdfkit.from_string(
        html_out,
        filename,
        options={
            "enable-local-file-access": "",
            "page-size": "A4",
            "margin-top": "0mm",
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            "margin-right": "0mm",
            'encoding': "UTF-8",
            # 'disable-smart-shrinking': '',
            'zoom': '1.3'
        }
    )


    return filename
