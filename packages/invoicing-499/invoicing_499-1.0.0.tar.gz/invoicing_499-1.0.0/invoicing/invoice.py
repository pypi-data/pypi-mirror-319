import glob
import pandas as pd
from fpdf import FPDF
from pathlib import Path

def generate(invoice_path, pdf_path):
    files = glob.glob(f"{invoice_path}/*.xlsx")

    for file in files:
        df = pd.read_excel(file, sheet_name="Sheet 1")

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(file).stem
        invoice_id = filename.split("-")[0]
        date = filename.split("-")[1]

        pdf.set_font("Times",size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice No. {invoice_id}",ln=1)

        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
        pdf.ln(4)
        headers = [item.replace("_", " ").title() for item in list(df.columns)]

        pdf.set_font("Times", size=12, style="B")
        pdf.cell(w=30, h=8, txt=f"{headers[0]}", border=1)
        pdf.cell(w=60, h=8, txt=f"{headers[1]}", border=1)
        pdf.cell(w=40, h=8, txt=f"{headers[2]}", border=1)
        pdf.cell(w=30, h=8, txt=f"{headers[3]}", border=1)
        pdf.cell(w=30, h=8, txt=f"{headers[4]}", border=1, ln=1)

        for index, row in df.iterrows():
            pdf.set_font("Times",size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=f"{row['product_id']}", border=1)
            pdf.cell(w=60, h=8, txt=f"{row['product_name']}", border=1)
            pdf.cell(w=40, h=8, txt=f"{row['amount_purchased']}", border=1)
            pdf.cell(w=30, h=8, txt=f"{row['price_per_unit']}", border=1)
            pdf.cell(w=30, h=8, txt=f"{row['total_price']}", border=1, ln=1)

        pdf.set_font("Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=f"", border=1)
        pdf.cell(w=60, h=8, txt=f"", border=1)
        pdf.cell(w=40, h=8, txt=f"", border=1)
        pdf.cell(w=30, h=8, txt=f"", border=1)
        pdf.cell(w=30, h=8, txt=f"{df['total_price'].sum()}", border=1, ln=1)

        pdf.ln(5)
        pdf.set_font("Times", size=14, style="B")
        pdf.set_text_color(0,0,0)
        pdf.cell(w=30, h=8, txt=f"The Total price is {df['total_price'].sum()}", ln=1)

        pdf.set_font("Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"PyhonHow")
        pdf.image(r"D:\02-Learning\Python\Udemy\60DaysPython\App20-Build-Package\pythonhow.png", w=10)

        pdf.output(f"{pdf_path}/{filename}.pdf")