import camelot
import pdfplumber
import pandas as pd
from tabulate import tabulate

# Base class
class PDFExtractorBase:
    def __init__(self, pdf_file: str):
        self.pdf_file = pdf_file

    def read_pdf(self):
        raise NotImplementedError("Subclasses must implement read_pdf()")


# Camelot extractor
class CamelotPDFExtractor(PDFExtractorBase):
    def read_pdf(self):
        try:
            tables = camelot.read_pdf(self.pdf_file, pages="all")
            if tables.n == 0:
                print(" Camelot found no tables.")
                return []
            return [t.df for t in tables]
        except FileNotFoundError:
            print(f" PDF file '{self.pdf_file}' not found.")
            return []
        except Exception as e:
            print(f" Camelot failed: {e}")
            return []


# pdfplumber extractor
class PDFPlumberExtractor(PDFExtractorBase):
    def read_pdf(self):
        extracted_tables = []
        try:
            with pdfplumber.open(self.pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    try:
                        table = page.extract_table()
                        if table:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            extracted_tables.append(df)
                    except Exception as e:
                        print(f" Failed to extract table from page {page_num}: {e}")
            return extracted_tables
        except FileNotFoundError:
            print(f" PDF file '{self.pdf_file}' not found.")
            return []
        except Exception as e:
            print(f" pdfplumber failed: {e}")
            return []


# Excel exporter
class ExcelExporter:
    def __init__(self, excel_file: str):
        self.excel_file = excel_file

    def export(self, tables: list):
        try:
            with pd.ExcelWriter(self.excel_file, engine="openpyxl") as writer:
                for i, df in enumerate(tables):
                    sheet_name = f"Sheet{i+1}"
                    try:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as e:
                        print(f" Failed to write table {i+1} to Excel: {e}")
            print(f" Data successfully written to {self.excel_file}")
        except PermissionError:
            print(f" Permission denied while writing to '{self.excel_file}'.")
        except Exception as e:
            print(f" Failed to write Excel file: {e}")


# Auto-choosing pipeline
class AutoPDFToExcelPipeline:
    def __init__(self, pdf_file: str, excel_file: str):
        self.pdf_file = pdf_file
        self.excel_file = excel_file

    def run(self):
        # Try Camelot first
        extractor = CamelotPDFExtractor(self.pdf_file)
        tables = extractor.read_pdf()

        if tables:
            print("ℹ Using Camelot extractor (text-based PDF).")
        else:
            print("ℹ Falling back to pdfplumber extractor (scanned/image PDF).")
            extractor = PDFPlumberExtractor(self.pdf_file)
            tables = extractor.read_pdf()

        if not tables:
            print(" No tables could be extracted from the PDF.")
            return

        # Print tables in console
        for i, df in enumerate(tables):
            try:
                print(f"\nTable {i+1}:")
                print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
            except Exception as e:
                print(f" Could not print Table {i+1}: {e}")

        # Export to Excel
        exporter = ExcelExporter(self.excel_file)
        exporter.export(tables)


# Example usage
pipeline = AutoPDFToExcelPipeline("input.pdf", "output.xlsx")
pipeline.run()
