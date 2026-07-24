## Quick Start

```bash
git clone https://github.com/rohannes220/ABB_VOIF.git
cd ABB_VOIF

pip install -r requirements.txt
playwright install chromium

python main.py --platform all
```


# Voice of the Customer (VoC) Fashion Analytics Pipeline

A Python-based data collection and analytics pipeline for analyzing publicly available customer feedback on fashion brands. The project collects reviews from multiple online platforms, standardizes them into a common schema, performs sentiment and intent analysis, and prepares analytics-ready datasets for Microsoft Power BI dashboards.

---

# Project Overview

Voice of the Customer (VoC) is a customer analytics initiative focused on understanding how consumers perceive fashion brands across multiple public platforms.

The project analyzes customer sentiment, purchase intent, complaints, and key customer experience drivers using publicly available reviews. The processed data is transformed into dashboard-ready datasets that help identify trends, compare brand performance, and uncover actionable business insights.

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

This project helps answer questions such as:

- How do customers perceive different ABLBL brands across platforms?
- What are the primary drivers of positive and negative sentiment?
- How does customer sentiment differ between retail stores and online review platforms?
- Which customer intents are expressed most frequently?
- Are there emerging issues requiring business attention?

---

# Brands in Scope

The project currently analyzes reviews for:

- Allen Solly
- Louis Philippe
- Van Heusen
- Peter England
- American Eagle
- Reebok

---

# Data Sources

The current implementation supports automated review collection from:

- Google Reviews
- MouthShut
- Reviews.io

To supplement the automated pipeline, manually curated datasets from platforms such as Myntra, Twitter, and Instagram are included where automated extraction was not feasible because of platform restrictions or anti-bot protections.

# System Architecture

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

The complete architecture diagram is available in:

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
├── .gitignore
├── config.py
├── main.py
├── merge.py
├── label.py
├── schema.py
│
├── scrapers/
│   ├── google_reviews.py
│   ├── mouthshut.py
│   └── reviewsio.py
│
├── dashboards/
│   ├── dashboard.pbix
│   └── dashboard.pdf
│
├── docs/
│   ├── architecture.png
│   └── VoC_Fashion_Final_Presentation.pdf
│
└── output/
    ├── abb_cleaned_google_mouthshut_only.csv
    ├── abb_manual_myntra_twitter_instagram.csv
    ├── voc_fashion_raw_sample.csv
    ├── voc_fashion_labeled_sample.csv
    ├── voc_fashion_final_sample.csv
```

---

# Features

- Automated review collection
- Multi-platform web scraping
- Standardized review schema
- Dataset merging
- Duplicate detection
- Sentiment analysis
- Intent classification
- Dashboard-ready datasets
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

This repository includes the complete source code, dependency list, project documentation, sample output datasets, and execution instructions required to reproduce the analytics workflow.

To reproduce the project:

1. Clone the repository.
2. Install all required dependencies.
3. Install the Playwright browser.
4. Configure platform-specific settings in `config.py`.
5. Run the desired scraper(s). Each execution automatically generates a new timestamped dataset in the `output/` directory.
6. Merge and label the collected reviews.
7. Generate the final analytics dataset.
8. Open the Power BI dashboard to explore the results.

---

# Usage
By default, each execution automatically generates a new timestamped raw dataset in the `output/` directory.

```bash
python main.py --platform all
```

Example:

```text
output/
voc_fashion_raw_2026-07-24_18-45-12.csv
```

Optionally, specify a custom output filename:

```bash
python main.py --output output/my_reviews.csv
```


# Data Processing Pipeline

The workflow consists of the following stages:

1. Collect publicly available customer reviews.
2. Convert all reviews into a common schema.
3. Merge reviews from multiple sources.
4. Remove duplicate reviews.
5. Perform sentiment analysis.
6. Classify customer intent.
7. Export the processed dataset.
8. Visualize insights using Microsoft Power BI.

---

# Output

The `output/` directory contains both sample datasets and intermediate datasets generated during development.

| File | Description |
|------|-------------|
| abb_cleaned_google_mouthshut_only.csv | Cleaned dataset combining Google Reviews and MouthShut reviews used during data preparation. |
| abb_manual_myntra_twitter_instagram.csv | Manually compiled customer feedback collected from Myntra, Twitter, and Instagram. |
| voc_fashion_raw_sample.csv | Sample raw review dataset generated by the scraping pipeline. |
| voc_fashion_labeled_sample.csv | Sample dataset after sentiment, intent, and review type classification. |
| voc_fashion_final_sample.csv | Sample analytics-ready dataset used for dashboard visualization. |

Each execution of the pipeline automatically generates a new timestamped raw dataset. For example:

```text
output/
voc_fashion_raw_2026-07-24_18-45-12.csv
```

This preserves previous runs while preventing existing datasets from being overwritten.

---

# Sentiment Analysis

Customer reviews are classified into:

- Positive
- Neutral
- Negative

These labels enable comparisons across brands, review platforms, and customer experience categories.

---

# Intent Classification

Customer reviews are categorized into intents including:

- Purchase Intent
- Complaint
- Recommendation
- Product Comparison
- Information Seeking
- General Feedback

These labels help identify customer motivations and recurring discussion themes.

---

# Dashboard

The processed datasets are visualized using Microsoft Power BI.

The repository includes:

- `dashboards/dashboard.pbix`
- `dashboards/dashboard.pdf`

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
└── VoC_Fashion_Final_Presentation.pdf
```

These documents describe the project architecture, analytical methodology, and business insights.

#Technologies Used 
---
- Python
- Pandas
- Playwright
- BeautifulSoup
- Requests
- VADER Sentiment Analysis
- Microsoft Power BI
- Git
- GitHub
---

# Known Limitations

- Automated review extraction depends on publicly accessible webpages and may require updates if website structures or anti-bot protections change over time.
- Some platforms employ anti-bot protections that limit automated data collection.
- Intent classification is based on predefined keyword rules and may not capture every linguistic nuance.
- Sentiment analysis performance depends on the quality and language of the available review text.

---

# License

This project is intended for academic and portfolio purposes.

---

# Author

**Rohan Kumar**
