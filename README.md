

````markdown
# Voice of the Customer (VoC) Fashion Analytics Pipeline

A Python-based data collection and analytics pipeline for analyzing publicly available customer feedback on fashion brands. The project collects reviews and comments from multiple online platforms, standardizes them into a common schema, performs sentiment and intent analysis, and prepares analytics-ready datasets for Microsoft Power BI dashboards.

---

## Quick Start

```bash
git clone https://github.com/rohannes220/ABB_VOIF.git
cd ABB_VOIF

pip install -r requirements.txt
playwright install chromium

python3 main.py --platform all
````

> **Note:** The Google Reviews scraper uses Playwright to automate a Chromium browser and may take several minutes to complete.
> YouTube collection uses the YouTube Data API v3 and requires the `YOUTUBE_API_KEY` environment variable to be set before running YouTube or `--platform all`.

---

# Project Overview

Voice of the Customer (VoC) is a customer analytics initiative focused on understanding how consumers perceive fashion brands across multiple public platforms.

The project analyzes customer sentiment, purchase intent, complaints, and key customer experience drivers using publicly available reviews and comments. The processed data is transformed into dashboard-ready datasets that help identify trends, compare brand performance, and uncover actionable business insights.

---

# Project Objective

The objective of this project is to analyze external customer sentiment, intent, and key experience drivers for Aditya Birla Lifestyle Brands Limited (ABLBL) using publicly available customer feedback.

The project integrates customer feedback from multiple platforms to answer questions surrounding:

* Brand perception
* Customer satisfaction
* Product quality
* Pricing and value
* Store experience
* Customer service
* Purchase intent
* Emerging customer issues

---

# Business Questions

This project helps answer questions such as:

* How do customers perceive different ABLBL brands across platforms?
* What are the primary drivers of positive and negative sentiment?
* How does customer sentiment differ between retail stores, review platforms, and social/video platforms?
* Which customer intents are expressed most frequently?
* Are there emerging issues requiring business attention?

---

# Brands in Scope

The project currently analyzes customer feedback for:

* Allen Solly
* Louis Philippe
* Van Heusen
* Peter England
* American Eagle
* Reebok

---

# Data Sources

The current implementation supports automated customer feedback collection from:

* Google Reviews
* MouthShut
* YouTube Comments

YouTube comments are collected using the official YouTube Data API v3 and normalized into the same shared review schema used by the other sources.

To supplement the automated pipeline, manually curated datasets from platforms such as Myntra, Twitter/X, and Instagram are included where automated extraction was not feasible because of platform restrictions or anti-bot protections.

---

# System Architecture

```text
Data Collection
       │
       ▼
Google Reviews
MouthShut
YouTube Comments
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

```text
docs/architecture.png
```

---

# Repository Structure

```text
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
│   └── youtube.py
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
    └── voc_fashion_final_sample.csv
```

---

# Features

* Automated multi-platform customer feedback collection
* Google Reviews scraping using Playwright
* MouthShut review collection
* YouTube comment collection using the YouTube Data API v3
* Standardized review schema
* Dataset merging
* Duplicate detection
* Sentiment analysis
* Intent classification
* Dashboard-ready datasets
* CSV export

---

# Installation

Clone the repository:

```bash
git clone https://github.com/rohannes220/ABB_VOIF.git
cd ABB_VOIF
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the Playwright Chromium browser:

```bash
playwright install chromium
```

---

# YouTube API Configuration

YouTube comment collection requires access to the official YouTube Data API v3.

Set your API key as an environment variable before running the YouTube scraper.

macOS / Linux:

```bash
export YOUTUBE_API_KEY="YOUR_API_KEY"
```

Windows PowerShell:

```powershell
$env:YOUTUBE_API_KEY="YOUR_API_KEY"
```

Do not hard-code or commit the API key into the repository.

---

# Usage

Run all supported automated sources:

```bash
python3 main.py --platform all
```

Run an individual source:

```bash
python3 main.py --platform google
python3 main.py --platform mouthshut
python3 main.py --platform youtube
```

For a small YouTube test:

```bash
export YOUTUBE_MAX_VIDEOS_PER_BRAND=1
export YOUTUBE_MAX_COMMENTS_PER_VIDEO=10

python3 main.py --platform youtube --output output/youtube_test.csv
```

For a larger YouTube collection:

```bash
python3 main.py --platform youtube
```

Optional YouTube limits:

* `YOUTUBE_MAX_VIDEOS_PER_BRAND` — default: `5`
* `YOUTUBE_MAX_COMMENTS_PER_VIDEO` — default: `100`

Brand-specific YouTube search queries can be updated in `config.py`.

By default, executions generate datasets in the `output/` directory.

Example:

```text
output/
voc_fashion_raw_2026-07-24_18-45-12.csv
```

You can also specify a custom output file:

```bash
python3 main.py --output output/my_reviews.csv
```

---

# Reproducibility

This repository includes the complete source code, dependency list, documentation, sample output datasets, and execution instructions required to reproduce the analytics workflow.

To reproduce the project:

1. Clone the repository.
2. Install the required dependencies.
3. Install the Playwright Chromium browser.
4. Set the YouTube API key if YouTube data collection is required.
5. Configure platform-specific settings in `config.py`.
6. Run the desired scraper or scrapers.
7. Merge and label the collected customer feedback.
8. Generate the final analytics dataset.
9. Open the Power BI dashboard to explore the results.

---

# Data Processing Pipeline

The workflow consists of the following stages:

1. Collect publicly available customer reviews and comments.
2. Convert all feedback into a common schema.
3. Merge feedback from multiple sources.
4. Remove duplicate records.
5. Perform sentiment analysis.
6. Classify customer intent.
7. Export the processed dataset.
8. Visualize insights using Microsoft Power BI.

---

# Output

The `output/` directory contains both sample datasets and intermediate datasets generated during development.

| File                                      | Description                                                                                  |
| ----------------------------------------- | -------------------------------------------------------------------------------------------- |
| `abb_cleaned_google_mouthshut_only.csv`   | Cleaned dataset combining Google Reviews and MouthShut reviews used during data preparation. |
| `abb_manual_myntra_twitter_instagram.csv` | Manually compiled customer feedback collected from Myntra, Twitter/X, and Instagram.         |
| `voc_fashion_raw_sample.csv`              | Sample raw customer feedback dataset generated by the collection pipeline.                   |
| `voc_fashion_labeled_sample.csv`          | Sample dataset after sentiment, intent, and review type classification.                      |
| `voc_fashion_final_sample.csv`            | Sample analytics-ready dataset used for dashboard visualization.                             |

Each execution can generate a new timestamped raw dataset to preserve previous runs.

---

# Sentiment Analysis

Customer feedback is classified into:

* Positive
* Neutral
* Negative

These labels enable comparisons across brands, platforms, and customer experience categories.

---

# Intent Classification

Customer feedback is categorized into intents including:

* Purchase Intent
* Complaint
* Recommendation
* Product Comparison
* Information Seeking
* General Feedback

These labels help identify customer motivations and recurring discussion themes.

---

# Dashboard

The processed datasets are visualized using Microsoft Power BI.

The repository includes:

* `dashboards/dashboard.pbix`
* `dashboards/dashboard.pdf`

The dashboard provides:

* Sentiment by brand
* Sentiment by platform
* Intent distribution
* Customer experience drivers
* Brand comparison
* Review volume by source

---

# Project Documentation

Additional project documentation is included in:

```text
docs/
├── architecture.png
└── VoC_Fashion_Final_Presentation.pdf
```

These documents describe the project architecture, analytical methodology, and business insights.

---

# Technologies Used

* Python
* Pandas
* Playwright
* BeautifulSoup
* Requests
* YouTube Data API v3
* VADER Sentiment Analysis
* Microsoft Power BI
* Git
* GitHub

---

# Known Limitations

* Automated review extraction depends on publicly accessible webpages and may require updates if website structures change.
* Some platforms employ anti-bot protections that limit automated data collection.
* YouTube comment availability depends on whether comments are enabled for individual videos and on YouTube Data API quotas.
* Search-based YouTube collection may occasionally return videos that are loosely related to the intended brand or product.
* Intent classification is based on predefined keyword rules and may not capture every linguistic nuance.
* Sentiment analysis performance depends on the quality and language of the available feedback.

---

# License

This project is intended for academic and portfolio purposes.

---

# Author

**Rohan Kumar**

````

The API key **is not supposed to be written into the README**. The README just tells someone to set their own key using:

```bash
export YOUTUBE_API_KEY="YOUR_API_KEY"
````

That’s why you saw the API key section even though the code already works on your machine.
