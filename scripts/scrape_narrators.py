import sys
import os
import datetime
import json
import argparse
from loguru import logger
from alminasascrapper.common import make_request
from alminasascrapper.narrators import search_commentary, search_narrators
from alminasascrapper.constants import MSG_TIME
from typing import Dict, Any

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments to configure the script's behavior.
    
    :return: Namespace object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Scrape narrators' data and commentary.")
    
    parser.add_argument('--max-id', type=int, default=150000, help="Maximum narrator ID to search for.")
    parser.add_argument('--total-available', type=int, default=11189, help="Total number of available narrators.")
    parser.add_argument('--data-dir', type=str, default="data/narrator_data", help="Directory to store scraped data.")
    parser.add_argument('--log-dir', type=str, default="logs/", help="Directory to store log files.")
    
    return parser.parse_args()

def scrpe(max_id_to_search: int, total_available: int, data_dir: str) -> None:
    """
    Scrape data for narrators up to the maximum ID specified by max_id_to_search.
    It retrieves narrators' information and commentary, then stores them in individual JSON files.

    :param max_id_to_search: Maximum narrator ID to search for.
    :param total_available: Total number of narrators to scrape.
    :param data_dir: Directory to save the scraped data.
    
    :return: None
    """
    data_count = 1
    narrator_id = 1
    while narrator_id < max_id_to_search:
        SUCCESS = False
        narrators_result = search_narrators(narrator_id)
        try:
            # Check if data was found for the narrator
            if len(narrators_result["responses"][0]["hits"]["hits"]) > 0:
                SUCCESS = True
            else:
                logger.warning(f"Excluding Narrator as no data found: {narrator_id}")
                narrator_id += 1
            
            if SUCCESS:
                commentary_result = search_commentary(narrator_id)
                results = {narrator_id: {"about": narrators_result["responses"][0]["hits"]["hits"][0], 
                                         "commentary": commentary_result["responses"][0]["hits"]["hits"]}}
                
                # Save results to JSON file
                with open(os.path.join(data_dir, f"{narrator_id}.json"), "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Data Retrieved for narrator id: {narrator_id}, data count: {data_count}")
                data_count += 1
                narrator_id += 1

                if data_count >= total_available:
                    logger.info("Reached Max Narrators. Finished")
                    break
        except Exception as e:
            logger.error(f"Error: {narrator_id} details:{e}")

def configure_logger(log_dir: str) -> None:
    """
    Configure logging for the script, including setting up file and console logging.

    :param log_dir: Directory where the log files will be saved.
    
    :return: None
    """
    now = datetime.datetime.now()
    today_yyyymmdd = now.strftime('%Y_%m_%d')
    log_file = os.path.join(log_dir, "scrapper_" + str(today_yyyymmdd) + ".log")
    
    logger.add(log_file)
    logger.configure(
        handlers=[
            {"sink": sys.stderr, "level": "WARNING"},
            {"sink": sys.stdout, "level": "INFO"}
        ]
    )


if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Configure logger with the specified log directory
    configure_logger(args.log_dir)

    # Log the current time when the script starts
    now = datetime.datetime.now()
    logger.info(MSG_TIME.format(now))

    # Ensure data directory exists
    os.makedirs(args.data_dir, exist_ok=True)

    # Start the scraping process with the provided arguments
    scrpe(args.max_id, args.total_available, args.data_dir)
