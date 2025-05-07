# US10Y-Dashboard
REAL-TIME US 10-YEAR TREASURY YIELD DASHBOARD
=============================================

This project displays live data from the US 10-Year Treasury Yield,
scraped from CNBC using a Bash script with regex, and visualized on a web dashboard
built with Python Dash.

--------------------------------------------------------------------------------
🔗 LIVE DASHBOARD: http://16.16.68.145:8050/
📈 DATA SOURCE: https://www.cnbc.com/quotes/US10Y
--------------------------------------------------------------------------------

PROJECT FEATURES
----------------
- Bash-only scraper using curl, grep, sed, and regex (NO Python used for scraping)
- Data saved to a CSV file with timestamped entries
- Live dashboard built using Dash (Python)
- Time series graph displaying yield over time
- Daily summary report generated at 8PM with:
  - Open and close yields
  - Min, max, volatility and average
- Automatic updates every 5 minutes using cron
- Hosted on a Linux virtual machine running 24/7
- Version control with Git and GitHub

PROJECT STRUCTURE
-----------------
us10y-yield-dashboard/
├── Templates/
│   └── index.html            # HTML, CSS, and Javascript code
├── dashboard.py               # python code to treat the data and to display the page
├── scrap.sh     # sh code to scrap the datas
├── yield.csv           # csv where we scrap stock the data
├── README.md                       # This file

USAGE
-----------------------
Go to this link to see the Dashboard: http://16.16.68.145:8050/

REQUIREMENTS
------------
- Python 3.8 or higher
- Dash
- Pandas
- Plotly

TEAM
----
- DIALLO Mouhamed
- CHERIF Eya
NOTES
-----
- This project is part of an academic assignment to demonstrate live web scraping,
  automation, and dashboarding using only Bash and Python.
- All scraping is done in Bash without using external libraries.
- Data is processed and displayed using Python Dash.
- The entire system is versioned with Git and hosted on GitHub.
- Dashboard is hosted on a virtual machine and runs continuously.

WHY THIS PROJECT?
-----------------
This end-to-end project simulates a real-time data pipeline, useful in finance and operations.
It strengthens skills in shell scripting, web scraping, data visualization, and cloud deployment.

ENJOY!
