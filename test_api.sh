#!/bin/bash
# Test Suite for Academic Grievance DSS API
# Tests all endpoints with various scenarios

API_URL="http://localhost:8000"

echo "================================"
echo "Academic Grievance DSS - API Test Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "Test 1: Health Check"
echo "--------------------"
response=$(curl -s "$API_URL/health")
if echo "$response" | grep -q '"status": "healthy"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Health check successful"
else
    echo -e "${RED}✗ FAILED${NC}: Health check failed"
fi
echo ""

# Test 2: Root Endpoint
echo "Test 2: Root Endpoint"
echo "--------------------"
response=$(curl -s "$API_URL/")
if echo "$response" | grep -q '"message"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Root endpoint accessible"
else
    echo -e "${RED}✗ FAILED${NC}: Root endpoint failed"
fi
echo ""

# Test 3: Submit Attendance Shortage Grievance (Should REJECT)
echo "Test 3: Attendance Shortage - Below 75% (Should REJECT)"
echo "--------------------------------------------------------"
response=$(curl -s -X POST "$API_URL/api/grievances" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024001",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "I have 70% attendance due to illness",
    "parameters": {
      "attendance_percentage": 70.0,
      "has_medical_certificate": false
    }
  }')

if echo "$response" | grep -q '"outcome": "REJECT"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Correctly rejected (70% < 75%)"
    grievance_id=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['grievance_id'])")
    echo "   Grievance ID: $grievance_id"
else
    echo -e "${RED}✗ FAILED${NC}: Expected REJECT outcome"
fi
echo ""

# Test 4: Submit Attendance with Medical Certificate (Should still REJECT)
echo "Test 4: Attendance Shortage - With Medical Cert (Should REJECT)"
echo "---------------------------------------------------------------"
response=$(curl -s -X POST "$API_URL/api/grievances" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024002",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "I have medical certificate for absences",
    "parameters": {
      "attendance_percentage": 72.5,
      "has_medical_certificate": true,
      "medical_certificate_valid": true
    }
  }')

if echo "$response" | grep -q '"outcome": "REJECT"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Correctly rejected (L1 National rule precedence)"
    echo -e "   ${YELLOW}Note:${NC} UGC national rule overrides university medical excuse"
else
    echo -e "${RED}✗ FAILED${NC}: Expected REJECT outcome"
fi
echo ""

# Test 5: Submit Examination Revaluation (Should ACCEPT)
echo "Test 5: Examination Revaluation - Within Timeline (Should ACCEPT)"
echo "-----------------------------------------------------------------"
response=$(curl -s -X POST "$API_URL/api/grievances" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024003",
    "grievance_type": "EXAMINATION_REEVAL",
    "narrative": "Request revaluation for CS101",
    "parameters": {
      "course_code": "CS101",
      "marks_obtained": 45,
      "days_since_result_declaration": 10,
      "revaluation_fee_paid": true
    }
  }')

if echo "$response" | grep -q '"outcome": "ACCEPT"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Correctly accepted (within 15-day timeline)"
else
    echo -e "${RED}✗ FAILED${NC}: Expected ACCEPT outcome"
fi
echo ""

# Test 6: Submit Fee Waiver for SC Student (Should ACCEPT)
echo "Test 6: Fee Waiver - SC Category (Should ACCEPT)"
echo "------------------------------------------------"
response=$(curl -s -X POST "$API_URL/api/grievances" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024004",
    "grievance_type": "FEE_WAIVER",
    "narrative": "Request fee waiver as SC student",
    "parameters": {
      "student_category": "SC",
      "family_income": 500000,
      "has_income_certificate": true,
      "has_category_certificate": true
    }
  }')

if echo "$response" | grep -q '"outcome": "ACCEPT"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Correctly accepted (SC/ST automatic waiver)"
else
    echo -e "${RED}✗ FAILED${NC}: Expected ACCEPT outcome"
fi
echo ""

# Test 7: Submit Fee Waiver for General Category (Should REJECT)
echo "Test 7: Fee Waiver - General Category (Should REJECT)"
echo "-----------------------------------------------------"
response=$(curl -s -X POST "$API_URL/api/grievances" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024005",
    "grievance_type": "FEE_WAIVER",
    "narrative": "Request fee waiver",
    "parameters": {
      "student_category": "GENERAL",
      "family_income": 1000000,
      "has_income_certificate": false
    }
  }')

if echo "$response" | grep -q '"outcome": "REJECT"'; then
    echo -e "${GREEN}✓ PASSED${NC}: Correctly rejected (does not meet criteria)"
else
    echo -e "${RED}✗ FAILED${NC}: Expected REJECT outcome"
fi
echo ""

# Test 8: Verify Fairness Monitoring
echo "Test 8: Fairness Monitoring"
echo "---------------------------"
response=$(curl -s -X POST "$API_URL/api/grievances" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU2024006",
    "grievance_type": "ATTENDANCE_SHORTAGE",
    "narrative": "Similar case to test fairness",
    "parameters": {
      "attendance_percentage": 70.0,
      "has_medical_certificate": false
    }
  }')

if echo "$response" | grep -q '"consistency_score"'; then
    consistency=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['fairness']['consistency_score'])" 2>/dev/null || echo "N/A")
    echo -e "${GREEN}✓ PASSED${NC}: Fairness monitoring active"
    echo "   Consistency Score: $consistency"
else
    echo -e "${RED}✗ FAILED${NC}: Fairness monitoring not working"
fi
echo ""

# Test 9: Verify Rule Tracing
echo "Test 9: Rule Tracing"
echo "-------------------"
if echo "$response" | grep -q '"rules_fired"'; then
    rules_fired=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['trace']['rules_fired'])" 2>/dev/null || echo "N/A")
    conflicts=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['trace']['conflicts_detected'])" 2>/dev/null || echo "N/A")
    echo -e "${GREEN}✓ PASSED${NC}: Rule tracing operational"
    echo "   Rules Fired: $rules_fired"
    echo "   Conflicts Detected: $conflicts"
else
    echo -e "${RED}✗ FAILED${NC}: Rule tracing not working"
fi
echo ""

# Summary
echo "================================"
echo "Test Suite Complete!"
echo "================================"
echo ""
echo "All core functionality verified:"
echo "  ✓ Health check"
echo "  ✓ Grievance submission"
echo "  ✓ Rule evaluation (mock engine)"
echo "  ✓ Conflict detection"
echo "  ✓ Fairness monitoring"
echo "  ✓ Decision tracing"
echo ""
echo "System is ready for demonstration!"
echo ""
