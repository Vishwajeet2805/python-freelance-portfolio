from pathlib import Path
from datetime import datetime
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

INPUT_FILE = "invoice_data.csv"
OUTPUT_DIR = Path("invoices")


def money(value):
    return f"₹{value:,.2f}"


def create_invoice(row):
    customer = row["customer_name"].strip()
    email = row["email"].strip()
    product = row["product"].strip()
    quantity = int(row["quantity"])
    price = float(row["price"])
    total = quantity * price

    OUTPUT_DIR.mkdir(exist_ok=True)
    invoice_number = f"INV-{datetime.now():%Y%m%d%H%M%S}-{customer[:3].upper()}"
    pdf_path = OUTPUT_DIR / f"{invoice_number}.pdf"

    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, height - 60, "INVOICE")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, height - 90, f"Invoice: {invoice_number}")
    pdf.drawString(50, height - 110, f"Date: {datetime.now():%Y-%m-%d}")

    pdf.drawString(50, height - 150, f"Customer: {customer}")
    pdf.drawString(50, height - 170, f"Email: {email}")

    y = height - 220
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Product")
    pdf.drawString(300, y, "Qty")
    pdf.drawString(370, y, "Unit Price")
    pdf.drawString(470, y, "Total")

    pdf.setFont("Helvetica", 11)
    y -= 25
    pdf.drawString(50, y, product)
    pdf.drawString(300, y, str(quantity))
    pdf.drawString(370, y, money(price))
    pdf.drawString(470, y, money(total))

    y -= 45
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(370, y, f"TOTAL: {money(total)}")

    y -= 60
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Thank you for your business.")

    pdf.save()

    return invoice_number, pdf_path, total


def main():
    try:
        with open(INPUT_FILE, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            print("No invoice records found.")
            return

        for row in rows:
            invoice_number, path, total = create_invoice(row)
            print(f"Created {invoice_number}: {path} ({money(total)})")

        print("\nAll invoices generated successfully.")

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} was not found.")
    except (ValueError, KeyError) as error:
        print(f"Invalid invoice data: {error}")


if __name__ == "__main__":
    main()
