# O*NET Occupational Database Integration

This directory contains occupational datasets sourced from and standardized against the **O*NET 28+ / 29+ Content Model** (U.S. Department of Labor / Employment and Training Administration).

Official Reference: https://www.onetcenter.org/database.html

## Content Model Elements Included:
1. **Occupation Titles & Codes**: Standard O*NET-SOC 2019 / 2020 taxonomy (e.g. `15-2051.00 Data Scientists`, `15-1252.00 Software Developers`).
2. **Descriptions & Summary**: Official occupational summary definitions.
3. **Job Zones**: Level of education, training, and experience required (Job Zone 1 to 5).
4. **Skills & Knowledge**: O*NET Content Model cognitive, technical, and resource management skill elements.
5. **Technology Skills (In-Demand Tools)**: Hot Technologies mapped to each occupation (Python, Docker, SQL, TensorFlow, AWS, Kubernetes, etc.).
6. **Work Activities & Abilities**: Analytical, engineering, and problem-solving elements.
7. **Related Occupations**: Cross-walk mapping between adjacent engineering and computing professions.

## Directory Structure:
- `raw/`: Raw downloaded tables or delta exports.
- `processed/onet_occupations.json`: Cleaned, validated, structured dataset for runtime agent querying.
- `processed/onet_occupations.csv`: Tabular export for pandas and scikit-learn matching.
- `processed/courses_catalog.json`: Verified repository of top-tier courses, free certifications, and official documentation.
