import pandas as pd
from pathlib import Path

INPUT_FILE = "sample_data.csv"
OUTPUT_FILE = "cleaned_data.csv"
REPORT_FILE = "report.txt"


def clean_data(input_file):
    try:
        df = pd.read_csv(input_file)
        original_rows = len(df)

        df = df.dropna(how="all")
        duplicates_removed = int(df.duplicated().sum())
        df = df.drop_duplicates()

        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )

        if "name" in df.columns:
            df["name"] = (
                df["name"].fillna("Unknown").astype(str)
                .str.strip().str.title()
            )

        if "email" in df.columns:
            df["email"] = (
                df["email"].fillna("Unknown").astype(str)
                .str.strip().str.lower()
            )

        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(
                df["amount"], errors="coerce"
            ).fillna(0)

        df.to_csv(OUTPUT_FILE, index=False)

        total_amount = df["amount"].sum() if "amount" in df.columns else 0
        average_amount = (
            df["amount"].mean()
            if "amount" in df.columns and len(df) > 0
            else 0
        )
        missing_emails = (
            int((df["email"] == "Unknown").sum())
            if "email" in df.columns else 0
        )

        report = f"""DATA CLEANING REPORT
====================

Original Records: {original_rows}
Final Records: {len(df)}
Duplicates Removed: {duplicates_removed}
Missing Emails: {missing_emails}

Total Amount: ₹{total_amount:.2f}
Average Amount: ₹{average_amount:.2f}

Output File:
{OUTPUT_FILE}
"""

        Path(REPORT_FILE).write_text(report.strip(), encoding="utf-8")
        print("Data cleaning completed successfully!")
        print(f"Cleaned file: {OUTPUT_FILE}")
        print(f"Report: {REPORT_FILE}")

    except FileNotFoundError:
        print(f"Error: '{input_file}' was not found.")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    clean_data(INPUT_FILE)
