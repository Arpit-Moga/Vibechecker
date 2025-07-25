# Improvement Checklist

## Patterns & Opportunities
- Inefficient algorithms or data structures
- Repeated code that could be abstracted
- Lack of modularity
- Poor performance (slow functions, high memory usage)
- Unoptimized database queries
- Missing documentation for public APIs
- Inconsistent error handling
- Lack of input validation
- Unused or redundant dependencies
- Opportunities for automation (CI/CD, testing)
- Outdated or missing architecture diagrams

## Severity Levels
- Low: Minor improvement, nice-to-have
- Medium: Noticeable impact on maintainability or performance
- High: Major improvement opportunity, significant impact

## Remediation Steps
- Refactor for modularity
- Optimize algorithms and queries
- Add or update documentation
- Improve error handling and validation
- Remove redundant dependencies
- Automate repetitive tasks

## Example Issues
- Function `sort_items` in `items.py` uses bubble sort (high severity)
- API endpoint `/get_user` lacks documentation (medium severity)
- Redundant dependency `six` in `requirements.txt` (low severity)

---

*All checklist items must be used by the Improvement Agent. Outputs must match the pydantic schema in architecture.md.*
