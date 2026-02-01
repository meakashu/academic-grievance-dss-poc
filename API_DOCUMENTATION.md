# API Documentation - Academic Grievance DSS

## Base URL
```
http://localhost:8000
```

---

## Authentication
Currently no authentication required (development mode).

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check system health and service status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "mock (in-memory)",
    "llm": "configured",
    "drools": "mock"
  },
  "debug_mode": true,
  "message": "All services operational"
}
```

---

### 2. Root Endpoint

**GET** `/`

Get API information.

**Response:**
```json
{
  "message": "Academic Grievance Decision Support System API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 3. Submit Grievance

**POST** `/api/grievances`

Submit a new grievance for evaluation.

**Request Body:**
```json
{
  "student_id": "STU2024001",
  "grievance_type": "ATTENDANCE_SHORTAGE",
  "narrative": "Detailed description of the grievance",
  "parameters": {
    "attendance_percentage": 70.0,
    "has_medical_certificate": false
  }
}
```

**Grievance Types:**
- `ATTENDANCE_SHORTAGE`
- `EXAMINATION_REEVAL`
- `FEE_WAIVER`
- `GRADE_DISPUTE`
- `ADMINISTRATIVE_DELAY`

**Response:**
```json
{
  "success": true,
  "message": "Grievance evaluated successfully",
  "grievance_id": "uuid",
  "decision": {
    "outcome": "REJECT",
    "applicable_rule": "UGC_Attendance_75Percent_Minimum",
    "regulatory_source": "UGC Regulations 2018, Section 4.2",
    "hierarchy_level": "L1_National",
    "salience": 1500,
    "reason": "Attendance 70% is below UGC-mandated 75% minimum",
    "explanation": "Detailed explanation...",
    "action_required": null,
    "human_review_required": false
  },
  "trace": {
    "trace_id": "uuid",
    "rules_fired": 2,
    "conflicts_detected": 1,
    "processing_time_ms": 0
  },
  "ambiguity": {
    "requires_human_review": false,
    "ambiguous_terms_count": 0,
    "clarification_questions": []
  },
  "fairness": {
    "consistency_score": 1.0,
    "meets_threshold": true,
    "anomaly_detected": false,
    "recommendation": "✓ CONSISTENT"
  }
}
```

---

### 4. Get Grievance by ID

**GET** `/api/grievances/{grievance_id}`

Retrieve a specific grievance.

**Response:**
```json
{
  "success": true,
  "grievance": {
    "id": "uuid",
    "student_id": "STU2024001",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "...",
    "parameters": {},
    "status": "RESOLVED",
    "created_at": "2026-02-01T12:00:00Z"
  }
}
```

---

### 5. Get Student Grievances

**GET** `/api/grievances/student/{student_id}`

Get all grievances for a student.

**Response:**
```json
{
  "success": true,
  "count": 2,
  "grievances": [...]
}
```

---

### 6. Get Decision by ID

**GET** `/api/decisions/{decision_id}`

Retrieve a specific decision.

**Response:**
```json
{
  "success": true,
  "decision": {
    "id": "uuid",
    "grievance_id": "uuid",
    "outcome": "REJECT",
    "applicable_rule": "...",
    "reason": "...",
    "created_at": "2026-02-01T12:00:00Z"
  }
}
```

---

### 7. Get Decisions by Grievance

**GET** `/api/decisions/grievance/{grievance_id}`

Get all decisions for a grievance.

**Response:**
```json
{
  "success": true,
  "count": 1,
  "decisions": [...]
}
```

---

### 8. Get Rule Trace

**GET** `/api/trace/{trace_id}`

Get detailed rule execution trace.

**Response:**
```json
{
  "success": true,
  "trace": {
    "id": "uuid",
    "grievance_id": "uuid",
    "decision_id": "uuid",
    "rules_evaluated": [
      {
        "rule_name": "UGC_Attendance_75Percent_Minimum",
        "hierarchy_level": "L1_National",
        "salience": 1500,
        "fired": true,
        "timestamp": "2026-02-01T12:00:00Z"
      }
    ],
    "conflicts_detected": [
      {
        "rule1": "UGC_Attendance_75Percent_Minimum",
        "rule2": "University_Medical_Excuse",
        "resolution": "L1_National takes precedence",
        "timestamp": "2026-02-01T12:00:00Z"
      }
    ],
    "processing_time_ms": 0
  }
}
```

---

## Example Requests

### Example 1: Attendance Shortage (REJECT)
```bash
curl -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024001",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "I have 70% attendance due to illness",
    "parameters": {
      "attendance_percentage": 70.0,
      "has_medical_certificate": false
    }
  }'
```

### Example 2: Examination Revaluation (ACCEPT)
```bash
curl -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024002",
    "grievance_type": "EXAMINATION_REEVAL",
    "narrative": "Request revaluation for CS101",
    "parameters": {
      "course_code": "CS101",
      "marks_obtained": 45,
      "days_since_result_declaration": 10,
      "revaluation_fee_paid": true
    }
  }'
```

### Example 3: Fee Waiver (ACCEPT)
```bash
curl -X POST http://localhost:8000/api/grievances \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024003",
    "grievance_type": "FEE_WAIVER",
    "narrative": "Request fee waiver as SC student",
    "parameters": {
      "student_category": "SC",
      "family_income": 500000,
      "has_income_certificate": true,
      "has_category_certificate": true
    }
  }'
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid request",
  "status_code": 400
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Resource not found",
  "status_code": 404
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "detail": "Error details (in debug mode)",
  "status_code": 500
}
```

---

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

Visit http://localhost:8000/redoc for ReDoc documentation.
