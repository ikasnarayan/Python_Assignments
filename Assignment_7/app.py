from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import io

app = FastAPI(title="Dynamic Form Data to PDF API")
templates = Jinja2Templates(directory="templates")

# Header/Footer for PDF
def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(100, 800, "Company XYZ - Form Submission Report")
    canvas.setFont('Helvetica', 10)
    page_num = canvas.getPageNumber()
    canvas.drawRightString(550, 30, f"Page {page_num}")
    canvas.restoreState()
#HTML Form
@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    try:
        return templates.TemplateResponse("form.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load form page: {e}")
#Export to PDF
@app.post("/exportFormPDF")
async def export_form_pdf(request: Request):
    try:
        # Step 1: Parse form data
        try:
            form = await request.form()
            form_data = dict(form)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid form submission: {e}")

        if not form_data:
            raise HTTPException(status_code=400, detail="No form data provided")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Dynamic Form Submission Report", styles['Title']))
        elements.append(Spacer(1, 20))

        # Step 2: Build table data
        try:
            data = [["Field", "Value"]]
            for k, v in form_data.items():
                if k.startswith("label_"):
                    suffix = k.split("_")[1]
                    label = v
                    value = form_data.get(f"value_{suffix}", "")
                    data.append([label, value])
                elif not k.startswith("value_"):
                    # Static fields like Name, Email
                    data.append([k.capitalize(), v])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing form fields: {e}")

        # Step 3: Create styled table
        try:
            table = Table(data, colWidths=[150, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))
            elements.append(table)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating PDF table: {e}")

        # Step 4: Build PDF
        try:
            doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
            buffer.seek(0)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=form_data.pdf"}
        )

    except HTTPException as he:
        # Re-raise known HTTP errors
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
