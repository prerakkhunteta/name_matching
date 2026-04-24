# Healthcare Identity Verification System with AI-Based Duplicate Detection

## Project Overview
Build a comprehensive healthcare patient registration system that integrates government ID verification with AI-powered duplicate detection to eliminate data redundancy and improve patient record accuracy in hospital databases.

## Core Problem Statement
Hospitals maintain patient databases where the same person often appears multiple times with different name spellings, abbreviations, or formats. This happens because:
- Patients registered before Aadhaar system had manual data entry with human errors
- Name variations across different government IDs (Mohammad vs Mohammed, Ramesh K vs Ramesh Kumar)
- Spelling mistakes during manual registration
- Different staff members entering data inconsistently

This leads to:
- Duplicate medical records for the same patient
- Fragmented medical history
- Billing errors and insurance claim issues
- Inefficient hospital operations

## Solution Architecture

### Part 1: Government ID Verification System
Create a patient registration interface that:
1. Allows healthcare staff to select ID type (Aadhaar, PAN Card, or Voter ID)
2. Enter only the ID number
3. Automatically fetch complete patient details from respective government databases
4. Auto-populate registration form with verified data (name, DOB, address, phone, email)
5. Eliminate manual typing errors

### Part 2: AI-Based Duplicate Detection
Implement intelligent name matching that:
1. Compares new registration against existing old patient records
2. Uses multiple fuzzy matching algorithms:
   - Levenshtein Distance (character-level differences)
   - Jaro-Winkler Similarity (phonetic matching)
   - Sequence Matcher (pattern recognition)
   - Cosine Similarity (vector-based comparison)
3. Calculates similarity scores for:
   - Name matching (handles spelling variations)
   - Date of birth matching
   - Address matching
4. Provides overall confidence percentage
5. Shows visual warning when potential duplicate found

## Technical Stack

### Frontend
- **Technology**: Single-page HTML5 application
- **Styling**: Modular CSS with modern design
- **JavaScript**: Vanilla JS for dynamic interactions
- **Features**:
  - Multi-page navigation (Home, Registration, About, Dashboard)
  - ID type selector with visual cards
  - Auto-fetch functionality
  - Duplicate warning modal with similarity scores
  - Existing patient record viewer
  - Responsive design

### Backend
- **Framework**: FastAPI (Python)
- **Libraries**:
  - pandas (data processing)
  - RapidFuzz (fuzzy matching)
  - uvicorn (ASGI server)
- **API Endpoints**:
  - `POST /match` - Duplicate detection across datasets
  - `POST /verify` - Identity verification by ID
  - `POST /check-duplicate` - Check new patient against old records
  - `GET /stats` - System statistics
  - `GET /health` - Health check

### Data Architecture
**Government Databases (CSV format):**
1. `aadhaar_db.csv` - 12-digit Aadhaar numbers
2. `pan_db.csv` - Alphanumeric PAN cards (ABCDE1234F format)
3. `voter_db.csv` - State code + numbers (RJ1234567890 format)

**Hospital Databases:**
1. `old_patients.csv` - Pre-Aadhaar era patient records
2. `users.csv` - Current registered users
3. `schemes.csv` - Government scheme enrollments

### Core Algorithms

**Preprocessing Module** (`preprocess.py`):
- Remove special characters
- Normalize text (lowercase, trim spaces)
- Standardize column names

**Blocking Module** (`blocking.py`):
- Group similar names using phonetic encoding (Metaphone)
- Reduce unnecessary comparisons
- Optimize performance for large datasets

**Scoring Module** (`scoring.py`):
- Levenshtein Distance: Character-level edit distance
- Jaro-Winkler: Phonetic similarity with prefix weighting
- Sequence Matcher: Pattern-based matching
- Cosine Similarity: Vector space comparison
- Hybrid Scoring: Weighted average of all algorithms

**Pipeline Module** (`pipeline.py`):
- Orchestrates entire matching workflow
- Handles CSV file processing
- Manages blocking and scoring
- Returns ranked match results

## Key Features

### 1. Multi-ID Support
- Aadhaar (12-digit numeric)
- PAN Card (10-character alphanumeric)
- Voter ID (state code + numeric)

### 2. Auto-Fetch Functionality
- One-click data retrieval
- Zero manual typing
- Instant verification
- Visual confirmation tags

### 3. Intelligent Duplicate Detection
- Real-time comparison against old records
- Multiple similarity metrics
- Visual progress bars for each metric
- Confidence level classification (High/Medium/Low)

### 4. User-Friendly Interface
- Clean, modern hospital theme
- Color-coded status indicators
- Sample IDs for testing
- Modal popups for detailed views
- Dashboard with statistics

### 5. Decision Support
- Shows existing patient record details
- Provides merge or register-as-new options
- Displays registration history
- Shows last visit information

## Implementation Details

### Frontend Flow
1. User selects ID type (Aadhaar/PAN/Voter)
2. Enters ID number or clicks sample ID
3. Clicks "Fetch Patient Details"
4. System queries respective database
5. Form auto-populates with verified data
6. Backend checks for duplicates
7. If match found (>70% confidence):
   - Display warning card
   - Show similarity scores with progress bars
   - Provide "View Existing Record" button
   - Offer "Merge" or "Register as New" options

### Backend Flow
1. Receive ID verification request
2. Query appropriate database (Aadhaar/PAN/Voter)
3. Return patient data if found
4. Receive duplicate check request
5. Load old_patients.csv
6. For each old patient:
   - Calculate name similarity
   - Calculate DOB match
   - Calculate address similarity
   - Compute weighted overall confidence
7. Return matches above 70% threshold
8. Sort by confidence (highest first)

### Matching Algorithm Weights
- Name similarity: 50%
- Date of birth: 30%
- Address similarity: 20%

### Confidence Levels
- 90-100%: Very High - Almost certainly same person
- 80-89%: High - Likely same person
- 70-79%: Medium - Possibly same person
- Below 70%: No duplicate warning shown

## Sample Data Characteristics

### Name Variations (for testing duplicate detection)
- "Mohammad Ali Khan" vs "Md. Ali Khan" vs "Mohammed Ali Khan"
- "Ramesh Kumar Sharma" vs "Ramesh K Sharma" vs "R Kumar Sharma"
- "Priya Nair" vs "Priya Nayr" (spelling variation)
- "Arjun Singh Mehta" vs "Arjun S Mehta" vs "Arjun Mehta"

### Realistic Indian Data
- Proper Indian names with regional diversity
- Realistic addresses with city and state
- Valid phone numbers (10-digit)
- Email addresses
- Date of births spanning 1978-1995
- Multiple states represented (Rajasthan, Kerala, UP, Bihar, Gujarat, etc.)

## Dashboard Features
- Total patients registered: 1,247
- Duplicates detected: 89
- Pending review: 23
- Match accuracy: 92.8%
- Recent activity table
- Database statistics by ID type
- Visual progress bars

## Use Cases

### Use Case 1: New Patient with Aadhaar
1. Patient arrives with Aadhaar card
2. Staff enters 12-digit Aadhaar number
3. System fetches verified details from Aadhaar database
4. System checks against old patient records
5. No duplicate found → Register as new patient

### Use Case 2: Duplicate Detection
1. Patient "Mohammad Ali Khan" registers with Aadhaar
2. System finds old record "Md. Ali Khan" from 2019
3. Shows 89% confidence match
4. Staff views existing record with medical history
5. Staff merges records to preserve medical history

### Use Case 3: Multiple ID Verification
1. Patient has PAN card but no Aadhaar
2. Staff selects PAN option
3. Enters PAN number (ABCDE1234F format)
4. System fetches from PAN database
5. Proceeds with registration

## Project Structure
```
name-matching-project/
├── index.html                 # Main HTML structure
├── css/
│   └── styles.css            # All styling
├── js/
│   └── app.js                # All JavaScript logic
├── backend/
│   ├── app.py                # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── data/
│   │   ├── aadhaar_db.csv   # Aadhaar database
│   │   ├── pan_db.csv       # PAN database
│   │   ├── voter_db.csv     # Voter ID database
│   │   ├── old_patients.csv # Pre-Aadhaar records
│   │   ├── users.csv        # Current users
│   │   └── schemes.csv      # Government schemes
│   └── src/
│       ├── __init__.py
│       ├── pipeline.py       # Main matching pipeline
│       ├── preprocess.py     # Data preprocessing
│       ├── blocking.py       # Blocking strategy
│       └── scoring.py        # Similarity algorithms
```

## Setup Instructions

### Backend Setup
```bash
cd name-matching-project/backend
pip install -r requirements.txt
python app.py
# Backend runs on http://localhost:8000
```

### Frontend Setup
```bash
cd name-matching-project
# Open index.html in browser or use live server
# Frontend runs on http://localhost:8080
```

## API Testing

### Test Duplicate Detection
```bash
curl -X POST "http://localhost:8000/check-duplicate" \
  -F "name=Mohammad Ali Khan" \
  -F "dob=1978-11-05" \
  -F "address=Plot 7 Civil Lines, Lucknow"
```

### Test ID Verification
```bash
curl -X POST "http://localhost:8000/verify" \
  -F "aadhaar=234567890123"
```

## Success Metrics
- 100% accurate data from government databases
- 92.8% duplicate detection accuracy
- 89 duplicates detected and prevented
- Zero manual typing errors
- Instant verification (< 1 second)
- Reduced registration time from 5 minutes to 30 seconds

## Future Enhancements
1. Multi-language support (Hindi, Tamil, Telugu, etc.)
2. Photo verification using face recognition
3. Biometric integration (fingerprint)
4. Real-time government database API integration
5. Mobile app for patient self-registration
6. SMS/Email OTP verification
7. Medical history integration
8. Insurance claim automation
9. Appointment scheduling
10. Prescription management

## Security Considerations
- Government ID data should be encrypted
- HTTPS for all API communications
- Role-based access control
- Audit logs for all data access
- GDPR/Data privacy compliance
- Secure database connections
- Input validation and sanitization

## Performance Optimization
- Blocking strategy reduces comparisons by 90%
- In-memory processing for speed
- Efficient pandas operations
- Batch processing for large datasets
- Caching for frequently accessed data
- Lazy loading for frontend

## Testing Strategy
1. Unit tests for each algorithm
2. Integration tests for API endpoints
3. UI tests for user workflows
4. Performance tests with large datasets
5. Edge case testing (special characters, empty fields)
6. Cross-browser compatibility testing

## Documentation Requirements
1. API documentation (Swagger/OpenAPI)
2. User manual for hospital staff
3. Technical documentation for developers
4. Database schema documentation
5. Deployment guide
6. Troubleshooting guide

## Deployment Considerations
- Backend: Deploy on cloud (AWS, Azure, GCP)
- Frontend: Static hosting (Netlify, Vercel)
- Database: PostgreSQL or MongoDB for production
- Load balancing for high traffic
- Auto-scaling configuration
- Backup and disaster recovery
- Monitoring and alerting

## Project Deliverables
1. Fully functional web application
2. Backend API with all endpoints
3. Complete source code with comments
4. Database files with sample data
5. Technical documentation
6. User guide
7. Deployment scripts
8. Test cases and results
9. Project report
10. Presentation slides

## Learning Outcomes
- FastAPI backend development
- RESTful API design
- Fuzzy string matching algorithms
- Data preprocessing techniques
- Frontend-backend integration
- CSV data handling with pandas
- Modern web UI/UX design
- Healthcare domain knowledge
- Government ID systems understanding
- Duplicate detection strategies

---

## Quick Start Guide

### For Developers
1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Start backend: `python backend/app.py`
4. Open `index.html` in browser
5. Test with sample IDs provided in the interface

### For Users (Hospital Staff)
1. Open the application in web browser
2. Click "Patient Registration"
3. Select ID type (Aadhaar/PAN/Voter)
4. Enter ID number or click sample ID
5. Click "Fetch Patient Details"
6. Review auto-filled information
7. If duplicate warning appears, review existing record
8. Choose to merge or register as new patient

---

**Project Type**: Healthcare Management System  
**Domain**: Healthcare IT, Identity Verification, Data Deduplication  
**Complexity**: Intermediate to Advanced  
**Estimated Development Time**: 4-6 weeks  
**Team Size**: 2-4 developers  
**Technologies**: Python, FastAPI, HTML5, CSS3, JavaScript, Pandas, Machine Learning (Fuzzy Matching)
