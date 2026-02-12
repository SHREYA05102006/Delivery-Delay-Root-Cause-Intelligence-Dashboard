# Delivery Delay Root Cause Intelligence Dashboard

This is an interactive Streamlit application designed to analyze and explain the root causes of delivery delays. It leverages machine learning insights to identify risk factors and provides actionable recommendations to mitigate future delays.

## Features

- **Interactive Dashboard:** Visualize delivery data and delay risks.
- **Root Cause Analysis:** Understand the primary reasons behind delays (e.g., Traffic, Weather, Warehouse issues).
- **Risk Scoring:** AI-driven risk scores to prioritize high-risk deliveries.
- **Detailed Explanations:** Order-level insights with ML-generated explanations.
- **Actionable Recommendations:** Suggested actions to prevent or mitigate delays.
- **Filtering:** Filter data by Traffic Level, Weather Conditions, and Risk Category.

## Tech Stack

- **Python:** The core programming language.
- **Streamlit:** For building the interactive web application.
- **Pandas:** For data manipulation and analysis.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/SHREYA05102006/Delivery-Delay-Root-Cause-Intelligence-Dashboard.git
    cd Delivery-Delay-Root-Cause-Intelligence-Dashboard
    ```

2.  Install the required dependencies:
    ```bash
    pip install streamlit pandas
    ```

## Usage

1.  Run the Streamlit app:
    ```bash
    streamlit run dashboard.py
    ```

2.  Open your web browser and navigate to the URL provided in the terminal (usually `http://localhost:8501`).

## Data Source

The application uses `data/final_intelligence_output.csv` as its data source. Ensure this file is present in the `data` directory for the dashboard to function correctly.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
