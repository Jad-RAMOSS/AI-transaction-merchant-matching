from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import tempfile
import os
from pipeline import process_file
import uvicorn

app = FastAPI(title="Transaction Matching API", version="1.0.0")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Accept an Excel/CSV file, run the ML pipeline, export to Oracle, and return a summary."""
    # Validate file type
    if not file.filename.lower().endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Only Excel or CSV files are supported.")

    # Save upload to a temporary file
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Run pipeline
        result_df: pd.DataFrame = process_file(tmp_path)
        rows_inserted = len(result_df)
        return JSONResponse({
            "status": "success",
            "rows": rows_inserted,
            "Predictions": result_df.to_dict(orient="records")
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp file
        os.remove(tmp_path)

