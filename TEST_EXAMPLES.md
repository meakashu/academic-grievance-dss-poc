# Test Examples - Academic Grievance DSS

## Comprehensive Test Cases

This file contains various test cases for different grievance scenarios.

---

## Test Case 1: Attendance Shortage - Below Threshold (REJECT)

**Scenario:** Student has 70% attendance, below UGC 75% minimum

**Request:**
```json
{
  "student_id": "STU2024001",
  "grievance_type": "ATTENDANCE_SHORTAGE",
  "narrative": "I have 70% attendance due to personal reasons",
  "parameters": {
    "attendance_percentage": 70.0,
    "has_medical_certificate": false,
    "days_absent": 15
  }
}
```

**Expected Outcome:** REJECT  
**Expected Rule:** UGC_Attendance_75Percent_Minimum  
**Expected Level:** L1_National

**cURL Command:**
```bash
curl -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024001",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "I have 70% attendance due to personal reasons",
    "parameters": {
      "attendance_percentage": 70.0,
      "has_medical_certificate": false,
      "days_absent": 15
    }
  }'
```

---

## Test Case 2: Attendance with Medical Certificate (REJECT)

**Scenario:** Student has 72.5% attendance with valid medical certificate

**Request:**
```json
{
  "student_id": "STU2024002",
  "grievance_type": "ATTENDANCE_SHORTAGE",
  "narrative": "I was absent for 10 days due to medical reasons. I have a valid medical certificate from a recognized hospital.",
  "parameters": {
    "attendance_percentage": 72.5,
    "has_medical_certificate": true,
    "medical_certificate_valid": true,
    "medical_certificate_from_recognized_authority": true,
    "days_absent": 10
  }
}
```

**Expected Outcome:** REJECT  
**Expected Rule:** UGC_Attendance_75Percent_Minimum  
**Expected Level:** L1_National  
**Note:** L1 National rule takes precedence over university medical excuse policy

---

## Test Case 3: Examination Revaluation - Within Timeline (ACCEPT)

**Scenario:** Student requests revaluation within 15-day window

**Request:**
```json
{
  "student_id": "STU2024003",
  "grievance_type": "EXAMINATION_REEVAL",
  "narrative": "I request revaluation for CS101. My marks seem lower than expected.",
  "parameters": {
    "course_code": "CS101",
    "marks_obtained": 45,
    "days_since_result_declaration": 10,
    "revaluation_fee_paid": true,
    "exam_semester": "Fall 2025"
  }
}
```

**Expected Outcome:** ACCEPT  
**Expected Rule:** UGC_Revaluation_15Days  
**Expected Level:** L1_National

---

## Test Case 4: Examination Revaluation - Late Request (REJECT)

**Scenario:** Student requests revaluation after 15-day deadline

**Request:**
```json
{
  "student_id": "STU2024004",
  "grievance_type": "EXAMINATION_REEVAL",
  "narrative": "I request revaluation for MATH201",
  "parameters": {
    "course_code": "MATH201",
    "marks_obtained": 42,
    "days_since_result_declaration": 20,
    "revaluation_fee_paid": true
  }
}
```

**Expected Outcome:** REJECT  
**Expected Rule:** UGC_Revaluation_15Days  
**Reason:** Request submitted after 15-day deadline

---

## Test Case 5: Fee Waiver - SC Category (ACCEPT)

**Scenario:** SC student requests fee waiver with valid certificates

**Request:**
```json
{
  "student_id": "STU2024005",
  "grievance_type": "FEE_WAIVER",
  "narrative": "I am from SC category and request fee waiver as per government policy",
  "parameters": {
    "student_category": "SC",
    "family_income": 500000,
    "has_income_certificate": true,
    "has_category_certificate": true,
    "fee_amount": 50000
  }
}
```

**Expected Outcome:** ACCEPT  
**Expected Rule:** GOI_SC_ST_Fee_Waiver  
**Expected Level:** L1_National

---

## Test Case 6: Fee Waiver - ST Category (ACCEPT)

**Scenario:** ST student requests fee waiver

**Request:**
```json
{
  "student_id": "STU2024006",
  "grievance_type": "FEE_WAIVER",
  "narrative": "I belong to ST category and need financial assistance",
  "parameters": {
    "student_category": "ST",
    "family_income": 400000,
    "has_income_certificate": true,
    "has_category_certificate": true,
    "fee_amount": 45000
  }
}
```

**Expected Outcome:** ACCEPT  
**Expected Rule:** GOI_SC_ST_Fee_Waiver

---

## Test Case 7: Fee Waiver - General Category (REJECT)

**Scenario:** General category student without meeting criteria

**Request:**
```json
{
  "student_id": "STU2024007",
  "grievance_type": "FEE_WAIVER",
  "narrative": "I request fee waiver due to financial difficulties",
  "parameters": {
    "student_category": "GENERAL",
    "family_income": 1000000,
    "has_income_certificate": false,
    "has_category_certificate": false
  }
}
```

**Expected Outcome:** REJECT  
**Reason:** Does not meet fee waiver criteria

---

## Test Case 8: Fee Waiver - OBC with Low Income (ACCEPT)

**Scenario:** OBC student with family income below threshold

**Request:**
```json
{
  "student_id": "STU2024008",
  "grievance_type": "FEE_WAIVER",
  "narrative": "I am from OBC category with low family income",
  "parameters": {
    "student_category": "OBC",
    "family_income": 200000,
    "has_income_certificate": true,
    "has_category_certificate": true,
    "fee_amount": 40000
  }
}
```

**Expected Outcome:** ACCEPT (if income < 300000)  
**Expected Rule:** University_OBC_Fee_Waiver

---

## Test Case 9: Grade Dispute

**Scenario:** Student disputes grade calculation

**Request:**
```json
{
  "student_id": "STU2024009",
  "grievance_type": "GRADE_DISPUTE",
  "narrative": "My final grade doesn't match my internal and external marks",
  "parameters": {
    "course_code": "PHY301",
    "internal_marks": 18,
    "external_marks": 65,
    "final_grade": "B",
    "expected_grade": "A"
  }
}
```

---

## Test Case 10: Administrative Delay

**Scenario:** Student complains about delayed certificate issuance

**Request:**
```json
{
  "student_id": "STU2024010",
  "grievance_type": "ADMINISTRATIVE_DELAY",
  "narrative": "I applied for my degree certificate 3 months ago but haven't received it",
  "parameters": {
    "document_type": "DEGREE_CERTIFICATE",
    "application_date": "2025-11-01",
    "days_pending": 90,
    "follow_ups_made": 5
  }
}
```

---

## Batch Testing Script

Save as `test_all_cases.sh`:

```bash
#!/bin/bash

echo "Running All Test Cases..."
echo "========================="

# Test Case 1
echo -e "\nTest 1: Attendance 70% (REJECT)"
curl -s -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024001",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "I have 70% attendance",
    "parameters": {
      "attendance_percentage": 70.0,
      "has_medical_certificate": false
    }
  }' | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"Outcome: {r['decision']['outcome']}\")"

# Test Case 2
echo -e "\nTest 2: Medical Cert 72.5% (REJECT)"
curl -s -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024002",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "Medical certificate",
    "parameters": {
      "attendance_percentage": 72.5,
      "has_medical_certificate": true
    }
  }' | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"Outcome: {r['decision']['outcome']}\")"

# Test Case 3
echo -e "\nTest 3: Exam Reeval (ACCEPT)"
curl -s -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024003",
    "grievance_type": "EXAMINATION_REEVAL",
    "narrative": "Request revaluation",
    "parameters": {
      "course_code": "CS101",
      "marks_obtained": 45,
      "days_since_result_declaration": 10,
      "revaluation_fee_paid": true
    }
  }' | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"Outcome: {r['decision']['outcome']}\")"

# Test Case 5
echo -e "\nTest 4: Fee Waiver SC (ACCEPT)"
curl -s -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024005",
    "grievance_type": "FEE_WAIVER",
    "narrative": "SC category fee waiver",
    "parameters": {
      "student_category": "SC",
      "family_income": 500000,
      "has_income_certificate": true,
      "has_category_certificate": true
    }
  }' | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"Outcome: {r['decision']['outcome']}\")"

# Test Case 7
echo -e "\nTest 5: Fee Waiver General (REJECT)"
curl -s -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024007",
    "grievance_type": "FEE_WAIVER",
    "narrative": "General category",
    "parameters": {
      "student_category": "GENERAL",
      "family_income": 1000000,
      "has_income_certificate": false
    }
  }' | python3 -c "import sys, json; r=json.load(sys.stdin); print(f\"Outcome: {r['decision']['outcome']}\")"

echo -e "\n========================="
echo "All tests completed!"
```

**Make executable and run:**
```bash
chmod +x test_all_cases.sh
./test_all_cases.sh
```

---

## Python Test Script

Save as `test_api.py`:

```python
#!/usr/bin/env python3
import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")

def test_attendance_reject():
    """Test attendance shortage - should REJECT"""
    payload = {
        "student_id": "STU2024001",
        "grievance_type": "ATTENDANCE_SHORTAGE",
        "narrative": "I have 70% attendance",
        "parameters": {
            "attendance_percentage": 70.0,
            "has_medical_certificate": False
        }
    }
    response = requests.post(f"{API_URL}/api/grievances", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["decision"]["outcome"] == "REJECT"
    print("✓ Attendance rejection test passed")

def test_exam_reeval_accept():
    """Test exam revaluation - should ACCEPT"""
    payload = {
        "student_id": "STU2024003",
        "grievance_type": "EXAMINATION_REEVAL",
        "narrative": "Request revaluation",
        "parameters": {
            "course_code": "CS101",
            "marks_obtained": 45,
            "days_since_result_declaration": 10,
            "revaluation_fee_paid": True
        }
    }
    response = requests.post(f"{API_URL}/api/grievances", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["decision"]["outcome"] == "ACCEPT"
    print("✓ Exam revaluation test passed")

def test_fee_waiver_sc():
    """Test fee waiver for SC - should ACCEPT"""
    payload = {
        "student_id": "STU2024005",
        "grievance_type": "FEE_WAIVER",
        "narrative": "SC category fee waiver",
        "parameters": {
            "student_category": "SC",
            "family_income": 500000,
            "has_income_certificate": True,
            "has_category_certificate": True
        }
    }
    response = requests.post(f"{API_URL}/api/grievances", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    assert data["decision"]["outcome"] == "ACCEPT"
    print("✓ Fee waiver SC test passed")

if __name__ == "__main__":
    print("Running API Tests...")
    print("=" * 50)
    
    try:
        test_health()
        test_attendance_reject()
        test_exam_reeval_accept()
        test_fee_waiver_sc()
        
        print("=" * 50)
        print("All tests passed! ✓")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
```

**Run:**
```bash
chmod +x test_api.py
python3 test_api.py
```

---

## Expected Results Summary

| Test Case | Grievance Type | Expected Outcome | Rule Level |
|-----------|----------------|------------------|------------|
| 1 | Attendance 70% | REJECT | L1_National |
| 2 | Attendance 72.5% + Med Cert | REJECT | L1_National |
| 3 | Exam Reeval (10 days) | ACCEPT | L1_National |
| 4 | Exam Reeval (20 days) | REJECT | L1_National |
| 5 | Fee Waiver SC | ACCEPT | L1_National |
| 6 | Fee Waiver ST | ACCEPT | L1_National |
| 7 | Fee Waiver General | REJECT | - |
| 8 | Fee Waiver OBC (low income) | ACCEPT | L3_University |
| 9 | Grade Dispute | PENDING_REVIEW | - |
| 10 | Admin Delay | PENDING_REVIEW | - |

---

**All test files are ready to use with the running backend!**
