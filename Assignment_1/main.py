import textwrap
import pandas as pd
from tabulate import tabulate
from openpyxl import load_workbook

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

input_file = "AI Bootcamp LangChain and LangGraph.xlsx"
output_file = "output.xlsx"

def wrap_text(val, width=40):
    if pd.isna(val):
        return ""
    return "\n".join(textwrap.wrap(str(val), width))

try:
    # Read Excel file
    df = pd.read_excel(input_file)

    # Replace 'Unnamed' columns with empty string or custom names
    df = df.rename(columns=lambda x: x if not x.startswith("Unnamed") else "")

    # Apply wrapping
    df_wrapped = df.applymap(lambda x: wrap_text(x, 20))

    print("Input data from excel:")
    print(tabulate(df, headers="keys", tablefmt="", showindex=False))

    # Write to new Excel file
    df.to_excel(output_file, sheet_name='UpdatedSheet', index=False)
    print(f"Data has been successfully written to {output_file}")

    # Adjust column widths
    wb = load_workbook(output_file)
    ws = wb["UpdatedSheet"]

    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except Exception as e:
                print(f"Error processing cell {cell.coordinate}: {e}")
        adjusted_width = max_length + 2
        ws.column_dimensions[col_letter].width = adjusted_width    

    wb.save(output_file)
    print("Column widths adjusted successfully.")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
except PermissionError:
    print(f"Error: Permission denied while accessing '{output_file}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
