# NAUKRI AUTOMATION TOOL


## Description:
------------
This tool automates the process of logging into Naukri.com and updating your resume.
It uses Selenium WebDriver to simulate human-like behavior to avoid detection.

## Quick Start:
-----------
1. Install dependencies: pip install -r requirements.txt
2. Set environment variables for NAUKRI_USERNAME and NAUKRI_PASSWORD
3. Place your resume in the resume directory or configure ORIGINAL_RESUME_PATH
4. Run the script: python naukri.py

## Docker Usage:
------------
1. Build: docker build -t naukri-automation .
2. Run: docker run -it -v $(pwd)/resume:/app/resume -e NAUKRI_USERNAME="username" -e NAUKRI_PASSWORD="password" naukri-automation

## Requirements:
------------
- Python 3.6+
- Chrome browser
- Selenium
- WebDriver Manager

## Contact:
-------
For issues or contributions, please refer to the repository documentation.