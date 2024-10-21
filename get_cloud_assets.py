import requests
import csv
import argparse
import sys


#set up argparse to handle token and csv file name
parser = argparse.ArgumentParser(description="trend micro xdr api request for attack surface devices")
parser.add_argument('--token', required=True, help="your api token")
parser.add_argument('--output', default='attack_surface_data.csv', help="output csv file")

#parse the arguments
args = parser.parse_args()

url_base = 'https://api.xdr.trendmicro.com'
url_path = '/v3.0/asrm/attackSurfaceCloudAssets'

#headers for the api request
headers = {
    'Authorization': 'Bearer ' + args.token
}

#query parameters for fetching 500 records per page
query_params = {
    'top': 500  #fetch 500 records per page
}

#function to fetch a page of data
def fetch_page(url):
    response = requests.get(url, headers=headers, params=query_params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"error: received status code {response.status_code}")
        return None

#simple progress bar
def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

#write the data to a csv file
csv_columns = [
    "id", "latestRiskScore", "assetName", "assetType", "criticality",
    "provider", "assetCategory", "service", "location", "region",
    "cloudAccountName", "firstSeenDateTime", "lastDetectedDateTime", "protectionStatus"
]

#initialize the csv file with a header
with open(args.output, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    next_url = url_base + url_path
    total_pages = current_page = 1  #initialize the page count (unknown pages)

    while next_url:
        response_data = fetch_page(next_url)
        
        if not response_data:
            break

        #write data to csv
        for item in response_data.get('items', []):
            writer.writerow({key: item.get(key, "") for key in csv_columns})

        #check if `nextLink` exists for pagination
        next_url = response_data.get('nextLink')

        #increment total_pages if nextLink exists
        if next_url:
            total_pages += 1

        #update the progress bar
        print_progress_bar(current_page, total_pages, prefix='progress', suffix='complete')
        current_page += 1

print(f"\ndata saved to {args.output}")
