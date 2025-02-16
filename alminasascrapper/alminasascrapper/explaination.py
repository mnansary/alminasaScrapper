from alminasascrapper.common import make_request
from typing import Dict,Any

def search_explanation(hadith_id: str, size: int = 5000) -> Dict[str, Any]:
    """
    Searches for Hadith explanations in Elasticsearch.

    Args:
        hadith_id (str): The Hadith ID to search for.
        size (int, optional): The number of explanations to return. Defaults to 100.

    Returns:
        Dict[str, Any]: The search results containing explanations.
    """
    query = {
        "bool": {
            "must": [
                {"terms": {"hadith.hadith_id": [hadith_id]}}
            ]
        }
    }
    
    extra_params = {
        "_source": ["explanation"],  # Only fetch explanations
        "track_total_hits": True,
        "sort": [
            {"hadith.explanation_authenticity_order": {"order": "asc"}},
            {"hadith.hadith_serial_id": {"order": "asc"}}
        ]
    }
    
    return make_request("es-prod-euw1-hadith-explanation-12-read", "expl_result", query, size, extra_params, meta={"query": "hadith_explanation"})