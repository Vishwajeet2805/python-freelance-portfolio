# Invoice Generator Automation

A Python automation tool that reads invoice records from CSV and generates professional PDF invoices.

## Features

- CSV-based input
- Automatic invoice numbering
- PDF invoice generation
- Quantity and price calculations
- Multiple invoices in one run
- Automatic output folder
- Input validation and error handling

## Tech Stack

- Python
- CSV
- ReportLab
- File handling

## Run

```bash
pip install -r requirements.txt
python main.py
```

Generated invoices are saved in the `invoices/` folder.

## Input Format

```csv
customer_name,email,product,quantity,price
Rahul Sharma,rahul@example.com,Laptop Stand,2,1200
```

## Example

2 × ₹1,200 = ₹2,400

The program creates a PDF with the customer details, product, quantity, unit price, total, invoice number, and date.

## Portfolio Highlights

This project demonstrates practical business automation, PDF generation, CSV processing, validation, and batch document generation.

## Email Automation

The project intentionally generates the invoice files but does not automatically send email. Email delivery can be added using a business SMTP provider after obtaining the required credentials and consent.
