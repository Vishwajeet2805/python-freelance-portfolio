# Python Data Cleaner & Report Generator

A Python automation tool that cleans CSV datasets and generates a summary report automatically.

## Features
- Removes duplicate records
- Removes empty rows
- Standardizes column names
- Cleans and formats names
- Normalizes email addresses
- Handles missing values
- Converts numeric data safely
- Calculates totals and averages
- Generates a cleaned CSV
- Generates an automatic report

## Tech Stack
- Python
- Pandas
- CSV
- File handling
- Exception handling

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Input
The included `sample_data.csv` intentionally contains duplicate records, inconsistent capitalization, and missing emails.

## Output
Running the program creates:
- `cleaned_data.csv`
- `report.txt`

## Workflow

Input CSV → Clean & Validate → Export Clean CSV → Generate Report

## Portfolio Note
This project demonstrates practical Python automation and data-cleaning skills useful for repetitive business-data tasks.
