import requests
import json
import gzip
from typing import Dict, Any, Optional
from loguru import logger

BASE_URL = "https://alminasa.ai/api/reactivesearchproxy/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-ndjson",
    "Origin": "https://alminasa.ai",
    "Referer": "https://alminasa.ai/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

def make_request(endpoint: str, 
                 preference: str, 
                 query: Dict[str, Any], 
                 size: int, 
                 extra_params: Optional[Dict[str, Any]] = None,
                 meta:Dict={}) -> Dict[str, Any]:
    """
    Sends a request to the specified Elasticsearch endpoint with the given parameters.
    
    Args:
        endpoint (str): The API endpoint to send the request to.
        preference (str): A preference string used for request handling.
        query (Dict[str, Any]): The query payload to search for.
        size (int): The maximum number of results to return.
        extra_params (Optional[Dict[str, Any]], optional): Additional parameters to include in the request.
        meta (dict) : additional infomation for logging and debugging

    Returns:
        Dict[str, Any]: The parsed JSON response from the API.
    """
    url = f"{BASE_URL}{endpoint}/_msearch?"
    
    # Construct the request body in NDJSON format
    body = [{"preference": preference}, {"query": query, "size": size}]
    if extra_params:
        body[1].update(extra_params)
    
    data = "\n".join(json.dumps(d, separators=(",", ":")) for d in body)
    
    # Send the request
    response = requests.post(url, headers=HEADERS, data=data)
    
    logger.debug(f"meta: {meta},Status Code: {response.status_code}")
    
    # Handle potential gzip compression in the response
    content = response.content
    if content.startswith(b'\x1f\x8b'):  # Gzip magic number
        try:
            content = gzip.decompress(content)
            logger.debug(f"meta: {meta}, Decompressed response successfully ")
        except Exception as e:
            logger.error(f"meta:{meta},Gzip decompression failed:{e}", e)
            return -1
            
    
    # Parse JSON response
    try:
        return json.loads(content.decode('utf-8'))
    except json.JSONDecodeError:
        logger.error(f"meta:{meta},Raw Response (first 200 bytes):{content[:200]}", )
        return -1 
        
