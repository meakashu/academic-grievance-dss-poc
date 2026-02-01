# Academic Grievance Decision Support System

[![License: Educational Use Only](https://img.shields.io/badge/License-Educational%20Use%20Only-blue.svg)](LICENSE)
[![Research Paper](https://img.shields.io/badge/Research-2026-green.svg)](https://github.com/akashsingh/academic-grievance-dss-poc)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Drools 8.44](https://img.shields.io/badge/drools-8.44.0-orange.svg)](https://www.drools.org/)

> **A Rule-Based, Hierarchy-Aware, Explainable Decision Support System for Academic Grievance Resolution in Higher Education Institutions**

---

## 📚 Research Attribution

**Author:** Akash Kumar Singh  
**Year:** 2026  
**Research Paper:** *A Rule-Based Decision Support System for Automated Academic Grievance Resolution*  
**Institution:** [Your Institution Name]  
**Contact:** meakash22dotin@gmail.com | +91 7255003131

**⚠️ IMPORTANT NOTICE:**
- This software is part of academic research and is **NOT FOR SALE**
- **Educational and Research Use Only**
- If you use this work, please cite the original research paper
- Commercial use is strictly prohibited without explicit written permission

---

## 🎯 Overview

This proof-of-concept demonstrates a governance-focused Decision Support System that addresses the critical challenge of fair, transparent, and consistent academic grievance resolution in Indian higher education institutions.

### Key Features

✅ **3-Tier Hierarchical Governance**
- L1 (National): UGC, MHRD regulations
- L2 (Accreditation): NAAC, NBA standards  
- L3 (University): Institutional policies

✅ **Rule-Based Reasoning with Drools**
- 14 production rules across 3 hierarchy levels
- Complete metadata for regulatory provenance
- Automatic conflict detection and resolution

✅ **LLM-Assisted Ambiguity Detection**
- GPT-4 integration for identifying discretionary language
- Flags subjective, permissive, and context-dependent terms
- Human review escalation for ambiguous cases

✅ **Complete Auditability**
- Full rule execution traces
- Regulatory citation for every decision
- Conflict resolution explanations

✅ **Fairness Monitoring**
- Consistency scoring across similar cases
- Anomaly detection (threshold: 0.85)
- Demographic parity analysis

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web UI (React)                          │
│  - Grievance Input Form                                     │
│  - Decision Display with Explanations                       │
│  - Rule Trace Visualization                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│              Backend API (FastAPI + Python)                 │
│  - Grievance Submission Endpoint                            │
│  - Rule Engine Orchestration                                │
│  - LLM Integration Layer                                    │
│  - Fairness Monitoring Module                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼────────┐ ┌──▼──────────┐ ┌▼──────────────┐
│  Drools Engine  │ │ LLM Service │ │  PostgreSQL   │
│  (Rule Engine)  │ │  (GPT-4)    │ │  (Database)   │
│                 │ │             │ │               │
│ - L1 National   │ │ - Ambiguity │ │ - Grievances  │
│ - L2 Accredit.  │ │   Detection │ │ - Decisions   │
│ - L3 University │ │ - Discretion│ │ - Rule Traces │
│ - Conflict Res. │ │   Flagging  │ │ - History     │
└─────────────────┘ └─────────────┘ └───────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.11 or higher ([Download](https://www.python.org/downloads/))
- **Java** 17 or higher ([Download OpenJDK](https://openjdk.org/install/))
- **Node.js** 18 or higher ([Download](https://nodejs.org/))
- **Docker** 20.10+ ([Download](https://docs.docker.com/get-docker/))
- **Maven** 3.8+ ([Download](https://maven.apache.org/install.html))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/akashsingh/academic-grievance-dss-poc.git
cd academic-grievance-dss-poc

# 2. Install Python dependencies
cd backend
pip3 install -r requirements.txt
cd ..

# 3. Install Node.js dependencies
cd frontend
npm install
cd ..

# 4. Build Java bridge for Drools
cd java-bridge
mvn clean package
cd ..

# 5. Configure environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here

# 6. Start PostgreSQL database
docker-compose up -d postgres
```

### Running the System

```bash
# Terminal 1: Start Backend API
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Frontend
cd frontend
npm start

# Terminal 3: View Database Logs (optional)
docker-compose logs -f postgres
```

**Access Points:**
- 🌐 **Web UI:** http://localhost:3000
- 📚 **API Docs:** http://localhost:8000/docs
- 🗄️ **Database:** localhost:5432 (user: `grievance_user`, db: `grievance_db`)

---

## 📦 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Rule Engine** | Drools | 8.44.0.Final | Industry-standard BRMS |
| **Backend** | Python + FastAPI | 3.11 + 0.109.0 | RESTful API server |
| **LLM** | OpenAI GPT-4 | gpt-4-turbo | Ambiguity detection |
| **Database** | PostgreSQL | 15.x | Data persistence |
| **Frontend** | React + TypeScript | 18.x | User interface |
| **Java Runtime** | OpenJDK | 17 | Drools execution |
| **Python-Java Bridge** | JPype1 | 1.5.0 | Drools integration |
| **Testing** | pytest + Jest | Latest | Automated testing |

---

## 🧪 Testing

### Run All Tests

```bash
# Backend unit tests (73 test functions)
cd backend
python3 -m pytest tests/ -v --cov=. --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage

# View coverage report
open backend/htmlcov/index.html
```

### Test Coverage

- **Unit Tests:** 73 test functions across 8 files
- **Integration Tests:** 60 test cases from `data/test_cases.json`
- **Overall Coverage:** 85%
- **Critical Paths:** Rule engine (92%), LLM service (88%), Fairness (85%)

**Test Categories:**
- ✅ Rule engine evaluation (10 tests)
- ✅ LLM ambiguity detection (8 tests)
- ✅ Fairness monitoring (8 tests)
- ✅ Conflict resolution (8 tests)
- ✅ Database operations (10 tests)
- ✅ API routes (11 tests)
- ✅ Edge cases (12 tests)

---

## 📖 Documentation

### Core Documentation
- **[API Documentation](API_DOCUMENTATION.md)** - Complete REST API reference
- **[System Summary](SYSTEM_SUMMARY.md)** - Architecture and design decisions
- **[Quick Start Guide](QUICKSTART.md)** - Step-by-step setup instructions
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Test Examples](TEST_EXAMPLES.md)** - Sample test cases and expected outputs

### Rule Documentation
- **[L1 National Laws](rules/L1_national_laws.drl)** - UGC, MHRD regulations (4 rules)
- **[L2 Accreditation Standards](rules/L2_accreditation_standards.drl)** - NAAC, NBA (5 rules)
- **[L3 University Statutes](rules/L3_university_statutes.drl)** - Institutional policies (5 rules)

---

## 🎓 Research Contributions

This proof-of-concept validates the following research contributions:

1. **Novel 3-Tier Hierarchical Governance Model**
   - Formalizes Indian higher education regulatory hierarchy
   - Implements authority-based conflict resolution (L1 > L2 > L3)

2. **LLM-Assisted Rule-Based DSS**
   - First system to combine Drools rule engine with GPT-4 for governance
   - Detects discretionary language requiring human judgment

3. **Complete Auditability Framework**
   - Full rule execution traces with regulatory citations
   - Explainable AI for governance-critical decisions

4. **Fairness Monitoring Mechanism**
   - Consistency scoring across similar historical cases
   - Demographic parity analysis for bias detection

5. **Reproducible Academic Software Artifact**
   - 85% test coverage with 73 unit tests
   - Docker-based reproducible environment
   - Complete documentation for reviewer validation

---

## 📊 Project Structure

```
academic-grievance-dss-poc/
├── backend/                 # Python FastAPI backend
│   ├── api/                # REST API routes
│   ├── services/           # Business logic (rule engine, LLM, fairness)
│   ├── models/             # Pydantic data models
│   ├── tests/              # 73 unit tests (pytest)
│   └── main.py             # Application entry point
├── frontend/                # React TypeScript UI
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API client
│   └── public/
├── rules/                   # Drools .drl files (14 rules)
│   ├── L1_national_laws.drl
│   ├── L2_accreditation_standards.drl
│   └── L3_university_statutes.drl
├── java-bridge/             # Java-Python integration
│   ├── src/                # Java source code
│   └── pom.xml             # Maven configuration
├── database/                # PostgreSQL schema and seeds
│   ├── schema.sql
│   └── seed.sql
├── data/                    # Test cases and samples
│   └── test_cases.json     # 60 integration test cases
├── docs/                    # Additional documentation
├── scripts/                 # Utility scripts
├── docker-compose.yml       # Docker services
├── .env.example             # Environment template
└── README.md                # This file
```

---

## 🔬 Research Paper Citation

If you use this work in your research, please cite:

```bibtex
@article{singh2026grievance,
  title={A Rule-Based Decision Support System for Automated Academic Grievance Resolution},
  author={Singh, Akash Kumar},
  year={2026},
  institution={[Your Institution]},
  url={https://github.com/akashsingh/academic-grievance-dss-poc}
}
```

---

## 📄 License

**Educational and Research Use Only**

Copyright © 2026 Akash Kumar Singh

This software is provided for **educational and research purposes only**. 

**Permissions:**
- ✅ Use for academic research and education
- ✅ Modify and extend for research purposes
- ✅ Cite in academic publications

**Restrictions:**
- ❌ Commercial use is strictly prohibited
- ❌ Redistribution for profit is not allowed
- ❌ Use in production systems without permission

For commercial licensing inquiries, contact: meakash22dotin@gmail.com

See [LICENSE](LICENSE) file for full terms.

---

## 👤 Author & Contact

**Akash Kumar Singh**  
📧 Email: meakash22dotin@gmail.com  
📱 Phone: +91 7255003131  
🔗 GitHub: [@akashsingh](https://github.com/akashsingh)  
🎓 Research Focus: Governance-Safe AI, Decision Support Systems, Higher Education Technology

**Research Supervision:** [Supervisor Name, if applicable]  
**Institution:** [Your Institution Name]  
**Year:** 2026

---

## 🤝 Contributing

This is an academic research project. Contributions are welcome for:
- Bug fixes
- Documentation improvements
- Test case additions
- Research extensions

**Please:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

**Note:** All contributions must maintain the educational/research focus and cannot introduce commercial features.

---

## 🐛 Troubleshooting

### Common Issues

**Java not found:**
```bash
# macOS
brew install openjdk@17

# Ubuntu/Debian
sudo apt install openjdk-17-jdk

# Verify installation
java -version
```

**Database connection failed:**
```bash
# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

**LLM API errors:**
```bash
# Verify API key
echo $OPENAI_API_KEY

# Check rate limits
# Visit: https://platform.openai.com/usage
```

**Frontend build errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🙏 Acknowledgments

This research was conducted as part of academic work on governance-focused decision support systems in higher education. Special thanks to:

- **University Grants Commission (UGC)** for regulatory framework documentation
- **NAAC/NBA** for accreditation standards
- **OpenAI** for GPT-4 API access
- **Drools Community** for rule engine support
- **Open Source Community** for FastAPI, React, and PostgreSQL

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/akashsingh/academic-grievance-dss-poc/issues)
- **Email:** meakash22dotin@gmail.com
- **Phone:** +91 7255003131

**For Academic Collaboration:**
If you're interested in collaborating on this research or extending this work, please reach out via email.

---

## ⚖️ Disclaimer

This is a **proof-of-concept** implementation for academic research purposes. It is not intended for production use in actual grievance resolution systems without proper validation, legal review, and institutional approval.

The rules and regulations referenced are based on publicly available UGC, NAAC, and NBA documentation. Users should verify current regulations with official sources.

---

**Built with ❤️ for transparent, fair, and accountable academic governance**

**© 2026 Akash Kumar Singh | Educational Use Only | Not For Sale**
