from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel, Field, field_validator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json

app = FastAPI(title="Home Loan Interest Calculator API")
#Error Handling
@app.exception_handler(json.JSONDecodeError)
async def json_decode_error_handler(request: Request, exc: json.JSONDecodeError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid JSON format",
            "detail": "Please send a valid JSON body with integers only for loan_amount and tenure_years."
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in err["loc"]),
            "error": err["msg"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "detail": errors
        },
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP error", "detail": exc.detail},
    )

#Base Models
class LoanRequest(BaseModel):
    loan_amount: int = Field(..., gt=0, description="Loan amount in INR (must be integer)")
    tenure_years: int = Field(..., gt=0, description="Tenure in years (must be integer)")

    # Enforce integer-only inputs
    @field_validator("loan_amount", "tenure_years", mode="before")
    def must_be_integer(cls, v, info):
        if not isinstance(v, int):
            raise ValueError(f"{info.field_name} must be an integer")
        return v

class LoanResponse(BaseModel):
    total_interest: float
    total_amount: float

#Functions

def get_interest_rate(amount: int) -> float:
    if amount <= 3000000:   # 30 lac
        return 6.5
    elif amount <= 5000000: # 50 lac
        return 7.5
    elif amount <= 9000000: # 90 lac
        return 9.0
    else:
        raise ValueError("Loan amount exceeds supported range (max 90 lac).")

# Endpoints
@app.post("/getLoanDetails", response_model=LoanResponse)
def get_loan_details(request: LoanRequest):
    try:
        rate = get_interest_rate(request.loan_amount)
        total_interest = (request.loan_amount * rate * request.tenure_years) / 100
        total_amount = request.loan_amount + total_interest
        return LoanResponse(total_interest=round(total_interest, 2),
                            total_amount=round(total_amount, 2))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error in loan calculation: {e}")

@app.post("/getLoanDetailsPDF")
def get_loan_details_pdf(request: LoanRequest):
    try:
        rate = get_interest_rate(request.loan_amount)
        total_interest = (request.loan_amount * rate * request.tenure_years) / 100
        total_amount = request.loan_amount + total_interest

        try:
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, "Home Loan Interest Calculator Report")
            c.drawString(100, 700, f"Loan Amount: {request.loan_amount}")
            c.drawString(100, 680, f"Tenure (years): {request.tenure_years}")
            c.drawString(100, 660, f"Interest Rate: {rate}%")
            c.drawString(100, 640, f"Total Interest: {round(total_interest, 2)}")
            c.drawString(100, 620, f"Total Amount: {round(total_amount, 2)}")
            c.save()
            buffer.seek(0)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=loan_details.pdf"}
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error in PDF generation: {e}")
