from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from src.pipeline import NameMatchingPipeline
from src.scoring import NameScorer
import pandas as pd
import uvicorn
import logging
import os
from typing import Optional, List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Identity Verification & Duplicate Detection API", description="API for identity verification and duplicate detection")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Identity Verification & Duplicate Detection API is running!",
        "endpoints": {
            "POST /match": "Upload and detect duplicates across all columns",
            "GET /health": "Check API health",
            "GET /stats": "Get system statistics",
            "POST /verify": "Verify identity by ID or details",
            "GET /docs": "Interactive API documentation"
        },
        "usage": "Use POST /match to upload CSV files for duplicate detection"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

@app.post("/match")
async def detect_duplicates(
    db1_file: UploadFile = File(...),
    db2_file: UploadFile = File(...),
    threshold: float = Form(80.0),
    blocking: str = Form("metaphone")
):
    try:
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


@app.get("/stats")
async def get_stats():
    try:
        users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
        schemes_df = pd.read_csv(os.path.join(DATA_DIR, "schemes.csv"))
        
        return {
            "total_records": len(users_df),
            "total_schemes": len(schemes_df),
            "unique_users": users_df['aadhaar'].nunique(),
            "active_schemes": len(schemes_df[schemes_df['status'] == 'Active'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify")
async def verify_identity(
    aadhaar: Optional[str] = Form(None),
    pan: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    dob: Optional[str] = Form(None)
):
    try:
        users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
        schemes_df = pd.read_csv(os.path.join(DATA_DIR, "schemes.csv"))
        
        if aadhaar:
            user = users_df[users_df['aadhaar'] == aadhaar]
            if not user.empty:
                user_data = user.iloc[0].to_dict()
                user_schemes = schemes_df[schemes_df['aadhaar'] == aadhaar]
                
                return {
                    "found": True,
                    "user": user_data,
                    "schemes": user_schemes.to_dict(orient="records"),
                    "match_type": "exact",
                    "confidence": 100
                }
        
        if pan:
            user = users_df[users_df['pan'] == pan]
            if not user.empty:
                user_data = user.iloc[0].to_dict()
                user_schemes = schemes_df[schemes_df['aadhaar'] == user_data['aadhaar']]
                
                return {
                    "found": True,
                    "user": user_data,
                    "schemes": user_schemes.to_dict(orient="records"),
                    "match_type": "exact",
                    "confidence": 100
                }
        
        if name and dob:
            scorer = NameScorer()
            matches = []
            
            for idx, row in users_df.iterrows():
                name_score = scorer.calculate_similarity(name.lower(), row['name'].lower())
                dob_match = str(row['dob']) == dob
                
                if dob_match:
                    dob_score = 100
                else:
                    dob_score = 0
                
                overall_score = (name_score * 0.7) + (dob_score * 0.3)
                
                if overall_score >= 60:
                    user_schemes = schemes_df[schemes_df['aadhaar'] == row['aadhaar']]
                    matches.append({
                        "user": row.to_dict(),
                        "schemes": user_schemes.to_dict(orient="records"),
                        "confidence": round(overall_score, 2),
                        "name_score": round(name_score, 2),
                        "dob_match": dob_match
                    })
            
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            
            if matches:
                return {
                    "found": True,
                    "match_type": "fuzzy",
                    "top_match": matches[0],
                    "all_matches": matches[:5]
                }
        
        return {
            "found": False,
            "message": "No matching records found"
        }
        
    except Exception as e:
        logging.error(f"Error during verification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/check-duplicate")
async def check_duplicate(
    name: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...)
):
    """
    Check if a new patient matches any existing old patient records
    Uses fuzzy name matching algorithms
    """
    try:
        # Load old patients database
        old_patients_df = pd.read_csv(os.path.join(DATA_DIR, "old_patients.csv"))
        scorer = NameScorer()
        
        matches = []
        
        for idx, old_patient in old_patients_df.iterrows():
            # Calculate name similarity
            name_score = scorer.calculate_similarity(name.lower(), old_patient['name'].lower())
            
            # Calculate DOB match
            if str(old_patient['dob']) == dob:
                dob_score = 100.0
            else:
                dob_score = 0.0
            
            # Calculate address similarity
            address_score = scorer.calculate_similarity(
                address.lower().replace(',', ''),
                old_patient['address'].lower().replace(',', '')
            )
            
            # Overall confidence: weighted average
            overall_confidence = (name_score * 0.5) + (dob_score * 0.3) + (address_score * 0.2)
            
            # Only consider matches above 70% confidence
            if overall_confidence >= 70:
                matches.append({
                    "patient_id": old_patient['patient_id'],
                    "name": old_patient['name'],
                    "dob": old_patient['dob'],
                    "address": old_patient['address'],
                    "city": old_patient['city'],
                    "state": old_patient['state'],
                    "registration_date": old_patient['registration_date'],
                    "last_visit": old_patient['last_visit'],
                    "name_score": round(name_score, 1),
                    "dob_score": round(dob_score, 1),
                    "address_score": round(address_score, 1),
                    "overall_confidence": round(overall_confidence, 1)
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x['overall_confidence'], reverse=True)
        
        if matches:
            return {
                "duplicate_found": True,
                "top_match": matches[0],
                "all_matches": matches[:3]  # Return top 3 matches
            }
        else:
            return {
                "duplicate_found": False,
                "message": "No existing patient records found"
            }
            
    except Exception as e:
        logging.error(f"Error during duplicate check: {e}")
        raise HTTPException(status_code=500, detail=str(e))
