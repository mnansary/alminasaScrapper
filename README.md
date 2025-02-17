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

* formatting narrator data bookwise: notebooks/format_narrator_data.ipynb

### Scrapping Hadith data:

* execute: ```python scripts/scrape_hadith.py```

```bash
usage: scrape_hadith.py [-h] [--total_available TOTAL_AVAILABLE] [--scrape_size SCRAPE_SIZE] [--data_dir DATA_DIR] [--log_dir LOG_DIR]

Scrape narrators' data and commentary.

optional arguments:
  -h, --help            show this help message and exit
  --total_available TOTAL_AVAILABLE
                        Total number of available hadiths.
  --scrape_size SCRAPE_SIZE
                        Total number of hadiths to scrape
  --data_dir DATA_DIR   Directory to store scraped data.
  --log_dir LOG_DIR     Directory to store log files.
```

* formatting bookwise: notebooks/format_hadith_data.ipynb

### Scrapping Sharh Data:

* execute: ```python scripts/scrape_explaination.py```

```bash
usage: scrape_explaination.py [-h] [--data_csv DATA_CSV] [--data_dir DATA_DIR] [--log_dir LOG_DIR]

Scrape explaination data

optional arguments:
  -h, --help           show this help message and exit
  --data_csv DATA_CSV  Path of bookwise hadth iden data
  --data_dir DATA_DIR  Directory to store scraped data.
  --log_dir LOG_DIR    Directory to store log files
```