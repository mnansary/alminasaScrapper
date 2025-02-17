import sys
import os
import datetime
import json
import argparse
import pandas as pd 
from tqdm import tqdm
tqdm.pandas()
from loguru import logger
from alminasascrapper.common import make_request
from alminasascrapper.explaination import search_explanation 
from alminasascrapper.constants import MSG_TIME
from typing import Dict, Any

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments to configure the script's behavior.
    
    :return: Namespace object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Scrape explaination data")
    parser.add_argument('--data_csv', type=str, default="data/hadith_data_iden_bookwise.csv", help="Path of bookwise hadth iden data")
    parser.add_argument('--data_dir', type=str, default="data/explaination_data", help="Directory to store scraped data.")
    parser.add_argument('--log_dir', type=str, default="logs/", help="Directory to store log files.")

    
    return parser.parse_args()

def scrpe(data_dir: str,data_csv:str) -> None:
    """
    Scrape data for hadiths up to the maximum ID specified by total_available
    
    :param data_dir: Directory to save the scraped data.
    
    :return: None
    """
    df=pd.read_csv(data_csv)
    for book in df.book_number.unique():
        bdf=df.loc[df.book_number==book]
        save_dir=os.path.join(data_dir,f"{book}")
        os.makedirs(save_dir,exist_ok=True)
        bdf.reset_index(drop=True,inplace=True)
        logger.info(f"Scariping explainations of Hadith book:{book}")
        for idx in tqdm(range(len(bdf))):
            hadith=bdf.iloc[idx,1]
            _save_data_json=os.path.join(save_dir, f"{hadith}.json")
            if not os.path.exists(_save_data_json):
                data=search_explanation(hadith)
                try:
                    _data=data["responses"][0]["hits"]["hits"]
                    if len(_data)>0:
                        with open(_save_data_json, "w", encoding="utf-8") as f:
                            json.dump({f"{hadith}":_data}, f, indent=2, ensure_ascii=False)
                    else:
                        logger.info(f"No data found for:{hadith}")
                except Exception as e:
                    logger.error(f"Error scraping explaination for hadith {hadith}: {e}")


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
    scrpe(args.data_dir,args.data_csv)
