from alminasascrapper.common import make_request
from typing import Dict,Any

def search_chain( hadith_id: str ,size: int = 500,) -> Dict[str, Any]:
    """
    Searches for chain records in Elasticsearch.
    
    Args:
        hadith_id (str): Hadith ID to search for.
        size (int, optional): The number of results to return. Defaults to 500.
        

    Returns:
        Dict[str, Any]: The search results containing chain details.
    """
    query = {
        "bool": {
            "must": [
                {"bool": {"must": [{"terms": {"hadith_id": [hadith_id]}}]}}
            ]
        }
    }
    
    extra_params = {
        "_source": {
            "includes": ["hadith_id", "nodes", "links", "chain_text"],
            "excludes": []
        },
        "track_total_hits": True,
        "aggs": {
            "unique_hadith_ids": {"terms": {"field": "hadith_id", "size": 500}},
            "unique_narrators": {"cardinality": {"field": "hadith.narrators_full_names"}},
            "unique_chapters": {"cardinality": {"field": "hadith.chapter"}},
            "unique_sub_chapters": {"cardinality": {"field": "hadith.sub_chapter"}}
        },
        "size": size
    }
    
    return make_request("es-prod-euw1-chains-graph-12-read", "result", query, size, extra_params, meta={"query": "chain_search"})
