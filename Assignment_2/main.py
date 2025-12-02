import camelot
import pandas as pd

def pdf_to_excel_camelot(pdf_file: str, excel_file: str):
    try:
        # Try reading tables from PDF
        tables = camelot.read_pdf(pdf_file, pages="all")

        if tables.n == 0:
            print("No tables found in the PDF.")
            return

        # Write each table to a separate sheet
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            for i, table in enumerate(tables):
                sheet_name = f"Sheet{i+1}"
                df = table.df  
                try:
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                except Exception as e:
                    print(f" Failed to write table {i+1} to Excel: {e}")

        print(f" Extracted {tables.n} tables and written to {excel_file}")

    except FileNotFoundError:
        print(f" Error: The file '{pdf_file}' was not found.")
    except PermissionError:
        print(f" Error: Permission denied while writing to '{excel_file}'.")
    except camelot.core.CamelotError as e:
        print(f" Failed to parse PDF: {e}")
    except Exception as e:
        print(f" Unexpected error occurred: {e}")

# Example usage
pdf_to_excel_camelot("input.pdf", "output.xlsx")
