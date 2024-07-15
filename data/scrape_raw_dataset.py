import scrapy
import json
from pathlib import Path
from scrapy.crawler import CrawlerProcess
import pandas as pd
from scrapy.shell import inspect_response
from scrapy import Request

# Get the directory of the current script file
project_dir = Path(__file__).resolve().parents[2]
result_dir = project_dir / "data/raw"
result_dir.mkdir(parents=True, exist_ok=True)


class BillSpider(scrapy.Spider):
    name = "bharat_bill_pay"
    data = []

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "COOKIES_ENABLED": True,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.bharatbillpay.com",
            "Referer": "https://www.bharatbillpay.com/statistics/central-unit",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        },
        "COOKIES_DEBUG": True,
    }

    start_urls = [
        "https://www.bharatbillpay.com/statistics/central-unit/bbpcuDaily.json",
        "https://www.bharatbillpay.com/statistics/biller-operating-units/bouTop20.json",
        "https://www.bharatbillpay.com/statistics/customer-operating-units/couTop30.json",
        "https://www.bharatbillpay.com/statistics/billers/liveBillers.json",
        "https://www.bharatbillpay.com/statistics/agent-institutions/agentInstitutionsTop20.json",
        "https://www.bharatbillpay.com/statistics/billers/categories.json"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # inspect_response(response, self)
        url_parts = response.url.split('/')
        folder_name = url_parts[-2]  # Get second-to-last part as folder name
        filename = url_parts[-1]  # Get last part as filename
        print(f"Folder Name: {folder_name}, Filename: {filename}")
        
        # Convert JSON response to Python dictionary
        response_data = json.loads(response.text)
        
        # Save the JSON data to a file in the appropriate folder
        folder_path = result_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        json_file_path = folder_path / filename
        
        with open(json_file_path, 'w') as f:
            json.dump(response_data, f)
        
        # Convert to DataFrame for further processing if needed
        # df = pd.DataFrame(response_data)
        # print(df)

def run_spider():
    process = CrawlerProcess()
    process.crawl(BillSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
