# Get Cloud ASRM Assets

## Overview
This Python script fetches attack surface data from the Trend Micro XDR API in batches of 500 records per page and saves it to a CSV file. It shows a progress bar to track data retrieval.

## Prerequisites
- Python 3.x
- Trend Micro XDR API token
- Internet access

## Installation & Usage
1. Clone or download the script.

   ```bash
   git clone https://github.com/jmlake569/v1-asrm-cloud-assets.git
   ```

2. Navigate to project folder:
   
   ```bash
   cd v1-asrm-cloud-assets
   ```

2. Install dependencies:
   
   ```bash
   pip install requests
   ```
   
3. Run this script (name your file using the --output flag):

   ```bash
   python get_cloud_assets.py --token YOUR_API_TOKEN --output OUTPUT_FILE.csv
   ```
