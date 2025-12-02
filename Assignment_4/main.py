import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def excel_to_pdf_reportlab_multisheet_safe(excel_file: str, pdf_file: str):
    # Step 1: Read Excel
    try:
        sheets = pd.read_excel(excel_file, sheet_name=None)  # Read all sheets
    except FileNotFoundError:
        print(f" Error: Excel file '{excel_file}' not found.")
        return
    except PermissionError:
        print(f" Error: Permission denied while accessing '{excel_file}'.")
        return
    except Exception as e:
        print(f" Failed to read Excel file: {e}")
        return

    # Step 2: Prepare PDF
    pdf = SimpleDocTemplate(pdf_file)
    styles = getSampleStyleSheet()
    elements = []

    # Step 3: Process each sheet
    for sheet_name, df in sheets.items():
        try:
            if df.empty:
                print(f" Skipping empty sheet: {sheet_name}")
                continue

            print(f" Processing sheet: {sheet_name}")

            # Add sheet title
            elements.append(Paragraph(f"Sheet: {sheet_name}", styles['Heading2']))
            elements.append(Spacer(1, 12))

            # Convert DataFrame to list of lists
            data = [df.columns.tolist()] + df.values.tolist()

            # Create table
            table = Table(data)

            # Style table
            style = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ])
            table.setStyle(style)

            elements.append(table)
            elements.append(PageBreak())

        except Exception as e:
            print(f" Skipping sheet '{sheet_name}' due to error: {e}")
            continue

    # Step 4: Build PDF
    try:
        pdf.build(elements)
        print(f" All valid sheets from '{excel_file}' have been written to '{pdf_file}'")
    except PermissionError:
        print(f" Error: Permission denied while writing to '{pdf_file}'.")
    except Exception as e:
        print(f" Failed to generate PDF: {e}")


# Example usage
excel_to_pdf_reportlab_multisheet_safe("AI Bootcamp LangChain and LangGraph.xlsx", "output.pdf")
