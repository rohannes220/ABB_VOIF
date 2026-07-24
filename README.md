# Voice of the Customer (VoC) Fashion Analytics Pipeline

A Python-based data collection and analytics pipeline for analyzing publicly available customer feedback on fashion brands. This project collects reviews from multiple online platforms, standardizes them into a common schema, performs sentiment and intent analysis, and prepares the data for business intelligence dashboards.

---

# Project Overview

Voice of the Customer (VoC) is a customer analytics initiative focused on understanding how consumers perceive fashion brands across multiple public platforms.

The project analyzes customer sentiment, purchase intent, complaints, and key experience drivers using publicly available reviews and comments. The processed data is transformed into dashboard-ready datasets that enable business users to identify trends, compare brand performance, and uncover actionable customer insights.

---

# Project Objective

The objective of this project is to analyze external customer sentiment, intent, and key experience drivers for Aditya Birla Lifestyle Brands Limited (ABLBL) using publicly available customer feedback.

The project integrates review data from multiple platforms to answer questions surrounding:

- Brand perception
- Customer satisfaction
- Product quality
- Pricing and value
- Store experience
- Customer service
- Purchase intent
- Emerging customer issues

---

# Business Questions

This project aims to answer questions such as:

- How do customers perceive different ABLBL brands across platforms?
- What are the primary drivers of positive and negative sentiment?
- How does customer sentiment differ between retail stores and online review platforms?
- Which customer intents are expressed most frequently?
- Are there emerging issues that require business attention?

---

# Brands in Scope

The analysis includes reviews for brands such as:

- Allen Solly
- Louis Philippe
- Van Heusen
- Peter England
- American Eagle
- Reebok

---

# Data Sources

The current implementation supports automated data collection from:

- Google Reviews
- MouthShut
- Reviews.io

Additional manually collected datasets may be included for platforms where automated extraction was not feasible because of platform restrictions or anti-bot protections.

---

# System Architecture

The overall workflow is shown in the architecture diagram included in the repository.

```
Data Collection
       │
       ▼
Google Reviews
MouthShut
Reviews.io
Manual Review Sources
       │
       ▼
Review Standardization
       │
       ▼
Dataset Merge
       │
       ▼
Duplicate Removal
       │
       ▼
Sentiment Analysis
       │
       ▼
Intent Classification
       │
       ▼
Final Analytics Dataset
       │
       ▼
Power BI Dashboard
```

The full architecture diagram is available in:

```
docs/architecture.png
```

---

# Repository Structure

```
ABB_VOIF/

├── README.md
├── LICENSE
├── requirements.txt
├── config.py
├── main.py
├── merge.py
├── label.py
├── schema.py

├── scrapers/
│   ├── google_reviews.py
│   ├── mouthshut.py
│   └── reviewsio.py

├── dashboard/
│   ├── dashboard.pbix
│   └── dashboard.pdf

├── docs/
│   ├── architecture.png
│   └── VoC_Fashion_Final_Presentation.pdf

└── output/
    ├── voc_fashion_raw.csv
    ├── voc_fashion_labeled.csv
    └── voc_fashion_final.csv
```

---

# Features

- Automated review collection
- Multi-platform support
- Standardized review schema
- Duplicate detection
- Dataset merging
- Sentiment analysis
- Intent classification
- Dashboard-ready output
- CSV export

---

# Installation

Clone the repository.

```bash
git clone https://github.com/rohannes220/ABB_VOIF.git

cd ABB_VOIF
```

Install the required Python packages.

```bash
pip install -r requirements.txt
```

Install the Playwright browser.

```bash
playwright install chromium
```

---

# Reproducibility

This repository includes the source code, dependency list, project documentation, sample output datasets, and execution instructions necessary to reproduce the analytics workflow.

To reproduce the project:

1. Clone the repository.
2. Install all required dependencies.
3. Install the Playwright browser.
4. Configure platform-specific settings in `config.py`.
5. Run the desired scraper(s).
6. Merge and label the collected reviews.
7. Generate the final analytics dataset.
8. Open the Power BI dashboard to explore the results.

---

# Usage

Run an individual scraper:

```bash
python main.py --platform google
```

```bash
python main.py --platform mouthshut
```

```bash
python main.py --platform reviewsio
```

Run all implemented scrapers:

```bash
python main.py --platform all
```

Specify an output location:

```bash
python main.py --output output/voc_fashion_raw.csv
```

---

# Data Processing Pipeline

The workflow consists of the following stages:

1. Collect publicly available customer reviews.
2. Convert all reviews into a common schema.
3. Merge reviews from multiple sources.
4. Remove duplicate reviews.
5. Perform sentiment analysis.
6. Classify customer intent.
7. Export the processed dataset.
8. Visualize insights using Power BI.

---

# Output

The repository includes sample outputs produced by the pipeline.

| File | Description |
|------|-------------|
| voc_fashion_raw.csv | Raw collected reviews |
| voc_fashion_labeled.csv | Reviews with sentiment and intent labels |
| voc_fashion_final.csv | Final processed dataset |

---

# Sentiment Analysis

The project classifies reviews into:

- Positive
- Neutral
- Negative

The labeled sentiment enables comparison across brands, review platforms, and customer experience categories.

---

# Intent Classification

Customer reviews are categorized into intents such as:

- Purchase Intent
- Complaint
- Recommendation
- Product Comparison
- Information Seeking
- General Feedback

These labels help identify customer motivations and common discussion themes.

---

# Dashboard

The processed datasets are visualized using Microsoft Power BI.

The repository includes:

- `dashboard/dashboard.pbix`
- `dashboard/dashboard.pdf`

The dashboard provides:

- Sentiment by brand
- Sentiment by platform
- Intent distribution
- Customer experience drivers
- Brand comparison
- Review volume by source

---

# Project Documentation

Additional project documentation is included in the repository.

```
docs/
├── architecture.png
└── VoC_Fashion_Final_Presentation.pptx
```

These documents describe the project architecture, analytical approach, and business insights.

---

# Technologies Used

- Python
- Pandas
- Playwright
- BeautifulSoup
- Requests
- VADER Sentiment Analysis
- Power BI
- Git
- GitHub

---

# Known Limitations

- Automated review extraction depends on publicly accessible webpages and may require updates if website structures change.
- Some platforms employ anti-bot protections that limit automated data collection.
- Intent classification is based on predefined keyword rules and may not capture every linguistic nuance.
- Sentiment analysis performance depends on the quality and language of the available review text.

---

# License

This project is intended for academic and portfolio purposes.

---

# Author

**Rohan Kumar**


