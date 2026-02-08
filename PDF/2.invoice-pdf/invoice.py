import jinja2
import pdfkit
from datetime import datetime
import os

# -----------------------
# Paths (ABSOLUTE)
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_TEMPLATE = os.path.join(BASE_DIR, "invoice.html")
CSS_FILE = os.path.join(BASE_DIR, "invoice.css")
OUTPUT_PDF = os.path.join(BASE_DIR, "invoice.pdf")

WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# -----------------------
# Data
# -----------------------
client_name = "Sachin Gunjal"

items = [
    ("Wifi", 499),
    ("Laptop", 399),
    ("Bag", 129)
]

total = sum(item[1] for item in items)

today_date = datetime.today().strftime("%d %b, %Y")
month = datetime.today().strftime("%B")

context = {
    "client_name": client_name,
    "today_date": today_date,
    "month": month,
    "items": items,
    "total": f"${total:.2f}"
}

# -----------------------
# Jinja2 Rendering
# -----------------------
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(BASE_DIR),
    autoescape=True
)

template = env.get_template("invoice.html")
html_output = template.render(context)

# -----------------------
# PDF Generation
# -----------------------
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

pdfkit.from_string(
    html_output,
    OUTPUT_PDF,
    configuration=config,
    css=CSS_FILE
)

print("Invoice PDF generated successfully.")
