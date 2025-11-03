from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from src.pipeline import NameMatchingPipeline
import pandas as pd
import uvicorn
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Duplicate Detection API", description="API for detecting duplicate records across CSV files")

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Duplicate Detection API is running!",
        "endpoints": {
            "POST /match": "Upload and detect duplicates across all columns",
            "GET /health": "Check API health",
            "GET /docs": "Interactive API documentation"
        },
        "usage": "Use POST /match to upload CSV files for duplicate detection across all columns"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running successfully"}

@app.post("/match")
async def detect_duplicates(
    db1_file: UploadFile = File(...),
    db2_file: UploadFile = File(...),
    threshold: float = Form(80.0),
    blocking: str = Form("metaphone")
):
    """Detect duplicate records between two CSV files by comparing all columns"""
    try:
        # Save uploaded files temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w+b') as temp1, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode='w+b') as temp2:
            
            temp1.write(await db1_file.read())
            temp2.write(await db2_file.read())
            
            temp1_name = temp1.name
            temp2_name = temp2.name

        pipeline = NameMatchingPipeline(
            blocking_strategy=blocking,
            threshold=threshold
        )
        results_df = pipeline.process_csv_files([temp1_name, temp2_name])
        return {"matches": results_df.to_dict(orient="records"), "total": len(results_df)}

    except Exception as e:
        logging.error(f"Error during duplicate detection: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
