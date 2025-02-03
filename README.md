# AlminasaScrapper

## Environment Creation

* create conda environment: ```conda create -n alminasa python=3.9```
* activate environment: ```conda activate alminasa```
* installation : **(linux only)**: ```bash install.sh```

## Execution:

### Scrapping Narrators data: 
* execute: ```python scripts/scrape_narrators.py```

```bash
usage: scrape_narrators.py [-h] [--max-id MAX_ID] [--total-available TOTAL_AVAILABLE] [--data-dir DATA_DIR] [--log-dir LOG_DIR]

Scrape narrators' data and commentary.

optional arguments:
  -h, --help            show this help message and exit
  --max-id MAX_ID       Maximum narrator ID to search for.
  --total-available TOTAL_AVAILABLE
                        Total number of available narrators.
  --data-dir DATA_DIR   Directory to store scraped data.
  --log-dir LOG_DIR     Directory to store log files.
```