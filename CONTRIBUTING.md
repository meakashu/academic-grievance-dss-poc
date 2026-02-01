# Contributing to Academic Grievance DSS

Thank you for your interest in contributing to this academic research project!

## 🎓 Project Nature

This is an **academic research project** by Akash Kumar Singh (2026). The primary goal is to validate research contributions in governance-focused decision support systems, not to build a production-ready commercial product.

## ✅ Welcome Contributions

We welcome contributions in the following areas:

### 1. Bug Fixes
- Fix issues in existing code
- Improve error handling
- Resolve edge cases

### 2. Documentation
- Improve README clarity
- Add code comments
- Enhance API documentation
- Fix typos and formatting

### 3. Test Coverage
- Add new test cases
- Improve existing tests
- Add edge case tests
- Increase code coverage

### 4. Research Extensions
- Implement additional rule types
- Add new fairness metrics
- Enhance LLM prompts
- Improve conflict resolution algorithms

## ❌ Not Accepting

- Commercial features
- Performance optimizations that compromise explainability
- Changes to core architecture (Drools, FastAPI, GPT-4, PostgreSQL)
- Removal of tracing/auditability features
- Proprietary integrations

## 📋 Contribution Process

### 1. Fork the Repository

```bash
git clone https://github.com/akashsingh/academic-grievance-dss-poc.git
cd academic-grievance-dss-poc
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-improvement
```

Use descriptive branch names:
- `fix/issue-description` for bug fixes
- `docs/improvement-description` for documentation
- `test/test-description` for test additions
- `research/feature-description` for research extensions

### 3. Make Your Changes

- Follow existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Test Your Changes

```bash
# Run backend tests
cd backend
python3 -m pytest tests/ -v

# Run frontend tests
cd frontend
npm test
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Commit Message Format:**
```
[Category] Brief description

Detailed explanation of what changed and why.

Fixes #issue-number (if applicable)
```

Categories: `Fix`, `Docs`, `Test`, `Research`, `Refactor`

### 6. Push and Create Pull Request

```bash
git push origin feature/your-improvement
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what and why
- Reference to any related issues
- Screenshots (if UI changes)

## 🔍 Code Review Process

1. **Automated Checks:** Tests must pass
2. **Code Review:** Maintainer will review within 7 days
3. **Feedback:** Address any requested changes
4. **Merge:** Once approved, changes will be merged

## 📝 Code Style Guidelines

### Python (Backend)
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Maximum line length: 100 characters

```python
def example_function(param: str) -> Dict[str, Any]:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    pass
```

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Add JSDoc comments

```typescript
/**
 * Brief description of component
 */
const ExampleComponent: React.FC<Props> = ({ prop }) => {
  // Component logic
};
```

### Drools Rules
- Include complete metadata
- Add comments explaining rule logic
- Follow naming convention: `Authority_Category_Description`

```drools
rule "UGC_Attendance_75Percent_Minimum"
    salience 1500
    metadata {
        level: "L1_National",
        authority: "UGC",
        source: "UGC Regulations 2018, Section 4.2"
    }
    when
        // Conditions
    then
        // Actions
end
```

## 🧪 Testing Requirements

All contributions must include tests:

- **Bug Fixes:** Add test reproducing the bug
- **New Features:** Add unit tests with >80% coverage
- **Documentation:** No tests required
- **Research Extensions:** Add integration tests

## 📧 Questions?

If you have questions about contributing:

- **Email:** meakash22dotin@gmail.com
- **GitHub Issues:** Open an issue with `[Question]` tag
- **Phone:** +91 7255003131 (for significant contributions)

## 🙏 Recognition

Contributors will be acknowledged in:
- `CONTRIBUTORS.md` file
- Research paper acknowledgments (for significant contributions)
- GitHub contributors page

## ⚖️ License Agreement

By contributing, you agree that your contributions will be licensed under the same Educational and Research Use License as the project.

---

**Thank you for helping advance academic research in governance-safe AI!**

© 2026 Akash Kumar Singh | Educational Use Only
