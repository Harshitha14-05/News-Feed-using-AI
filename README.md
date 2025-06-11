# News-Feed-using-AI

# Police-Relevant Daily News Digest MVP

## Overview

The Police-Relevant Daily News Digest MVP is a streamlined solution developed to automatically produce a comprehensive daily digest of news articles with a focus on police-relevant content. By harnessing AI-driven analysis, the system filters, groups, and cross-references English-language news articles based on district-specific relevance as defined by senior officers. The digest not only highlights current events but also provides comparative insights across various news sources, enriched by historical context from the previous seven days.

## Project Objective

The primary goal of this project is to enable police officers to stay well-informed through a user-friendly dashboard or PDF report. The system efficiently consolidates and organizes news content so that officers can:
- Quickly understand the landscape of news relevant to their respective police districts.
- Compare how different news sources report on the same events.
- Access historical trends and context by linking related articles from the preceding week.

## Scope

The MVP is designed to cover the following functionalities:

- **Daily Batch Process:**  
  Accepts date-based input from a news API, processing only articles published in English.

- **District-Relevant Filtering:**  
  Utilizes GenAI components to automatically filter articles to ensure they are relevant to specific police districts, as designated by guidelines provided by senior officers.

- **Topic Clustering and Comparative Summaries:**  
  Clusters articles into coherent topics and generates comparative summaries that juxtapose the reporting from various news outlets. These summaries are aligned with police directives and district priorities.

- **Historical Context Attachment:**  
  For each identified topic, the system attaches the top related articles from the previous seven days. This historical context enhances situational awareness and aids in well-informed decision-making.

- **Output Formats:**  
  The final digest is rendered into a PDF report for easy consumption, alongside a simple, interactive dashboard.

- **Exclusions:**  
  The MVP intentionally excludes the following to streamline development:
  - Real-time news alerts.
  - Multilingual capabilities.
  - User authentication.
  - Extended archival searches beyond the past week.
  - Mobile application interfaces.

## Features

- **Automated Data Ingestion:**  
  Fetch news articles from a designated API based on a given date.

- **AI-Powered Filtering:**  
  Leverage advanced machine learning models to filter and prioritize articles that are pertinent to defined police districts.

- **Content Clustering:**  
  Group articles into topics to ensure coherent and organized presentation of information.

- **Comparative Analysis:**  
  Generate insights that show how multiple news sources cover the same events, highlighting differences and similarities.

- **Historical Integration:**  
  Enrich each topic with related articles from the past week to offer broader context.

- **User-Friendly Output:**  
  Deliver information via an easy-to-navigate dashboard and as an exportable PDF report for offline viewing.

## Architecture and Workflow

1. **Data Collection:**  
   - Integrate with a news API to ingest daily articles.
   - Filter for English-language content.

2. **Data Processing:**  
   - Use GenAI components to filter articles based on district relevance.
   - Apply clustering algorithms to group similar news topics.
   - Run comparative analysis algorithms to highlight nuances among sources.

3. **Historical Context Integration:**  
   - Query historical data to attach relevant news from the preceding seven days for each topic.

4. **Output Generation:**  
   - Format and render the digest in PDF format.
   - Provide a dashboard interface for real-time interaction with the digest.

## Installation and Setup

1. **Prerequisites:**
   - A development environment with Python 3.8 or higher.
   - Access to the chosen news API (API key required).
   - Necessary dependencies (refer to `requirements.txt` for the complete list).

2. **Steps to Install:**
   - Clone the repository:
     ```bash
     git clone https://github.com/your-repo/police-news-digest-mvp.git
     cd police-news-digest-mvp
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure API keys and environment variables as needed.

3. **Running the Application:**
   - For development, execute:
     ```bash
     python run.py --date YYYY-MM-DD
     ```
   - The output digest will be available as a PDF and through the dashboard at the specified local URL.

## Usage

- **User Input:**  
  Input the desired date for the digest via command-line argument or through the dashboard interface.

- **Processing:**  
  The system will automatically:
  - Fetch relevant news articles.
  - Filter and group articles based on district relevance.
  - Generate comparative insights and attach historical context.

- **Output:**  
  The final digest is viewable on a dashboard and can be downloaded as a PDF for distribution and offline review.

## Future Enhancements

While the current MVP is focused on core functionality, future iterations may include:
- Real-time news alerts and notifications.
- Multilingual support to cover non-English news articles.
- User authentication for personalized experiences.
- Expanded archival searches for deeper historical context.
- Mobile-friendly interfaces for on-the-go access.

## Contributing

Contributions to enhance and extend this project are welcome. Please submit pull requests or report issues on the [GitHub repository](https://github.com/your-repo/police-news-digest-mvp).


## Contact

For any inquiries or further information, please contact (mailto:your.lukkaharshitha@gmail.com).



This README aims to provide a comprehensive overview of the Police-Relevant Daily News Digest MVP, its objectives, scope, functionalities, and roadmap for future development.
