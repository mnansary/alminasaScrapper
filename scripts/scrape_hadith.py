import sys
import os
import datetime
import json
import argparse
from loguru import logger
from alminasascrapper.common import make_request
from alminasascrapper.hadith import search_hadith 
from alminasascrapper.constants import MSG_TIME
from typing import Dict, Any

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments to configure the script's behavior.
    
    :return: Namespace object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Scrape narrators' data and commentary.")
    
    parser.add_argument('--total_available', type=int, default=82596, help="Total number of available hadiths.")
    parser.add_argument('--scrape_size', type=int, default=1000, help="Total number of hadiths to scrape")
    parser.add_argument('--data_dir', type=str, default="data/hadith_data", help="Directory to store scraped data.")
    parser.add_argument('--log_dir', type=str, default="logs/", help="Directory to store log files.")

    
    return parser.parse_args()

def scrpe(total_available: int, data_dir: str,scrape_size:int) -> None:
    """
    Scrape data for hadiths up to the maximum ID specified by total_available
    
    :param total_available: Total number of hadith to scrape.
    :param data_dir: Directory to save the scraped data.
    :param scrape_size : Number of hadith to scrape at a time.
    
    :return: None
    """
    search_after=[1,1,1]
    collected_data =1 
    while collected_data!=total_available:
        try:
            data=search_hadith(size=int(scrape_size),search_after=search_after)
                
            for _data in data['responses'][0]['hits']['hits']:
                # Save results to JSON file
                with open(os.path.join(data_dir, f"{_data['_source']['hadith_id']}.json"), "w", encoding="utf-8") as f:
                    json.dump(_data, f, indent=2, ensure_ascii=False)
                collected_data+=1
            
            logger.info(f"Data Retrieved for sorted index: {search_after}, data count: {collected_data}")
            search_after=data['responses'][0]['hits']['hits'][-1]['sort']

        except Exception as e:
            logger.error(f"Error: {search_after} details:{e}")


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Configure logger with the specified log directory
    now = datetime.datetime.now()
    today_yyyymmdd = now.strftime('%Y_%m_%d')
    log_file = os.path.join(args.log_dir, "scrapper_" + str(today_yyyymmdd) + ".log")
    
    logger.add(log_file)
    logger.configure(
    handlers=[
        {"sink": sys.stderr, "level": "WARNING"},
        {"sink": sys.stdout, "level": "INFO"},
        {"sink": log_file, "level": "INFO"},  # Ensure logs go to file
    ]
    )

    # Log the current time when the script starts
    now = datetime.datetime.now()
    logger.info(MSG_TIME.format(now))

    # Ensure data directory exists
    os.makedirs(args.data_dir, exist_ok=True)

    # Start the scraping process with the provided arguments
    scrpe(args.total_available, args.data_dir,args.scrape_size)
