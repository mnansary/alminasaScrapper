from typing import Dict, Any
from alminasascrapper.common import make_request
def search_narrators(narrator_id: str, size: int = 50) -> Dict[str, Any]:
    """
    Searches for narrators based on the given narrator ID.
    
    Args:
        narrator_id (str): The ID of the narrator to search for.
        size (int, optional): The maximum number of results to return. Defaults to 5.

    Returns:
        Dict[str, Any]: The search results containing narrator details.
    """
    query = {
        "bool": {
            "must": [
                {"bool": {"must": [{"match": {"id": narrator_id}}, {"match_all": {}}]}}
            ]
        }
    }
    
    extra_params = {
        "_source": {
            "includes": [
                "full_name", "extended_full_name", "nickname", "origin", "level", "born_on", "died_on",
                "lived_in", "died_in", "grade", "book_titles", "top_students", "top_scholars"
            ],
            "excludes": []
        },
        "track_total_hits": True
    }
    
    return make_request("es-prod-euw1-narrators-12-read", "result", query, size, extra_params,meta={"narrator":narrator_id})

def search_commentary(narrator_id: str, size: int = 2000) -> Dict[str, Any]:
    """
    Searches for commentary related to a specific narrator based on their ID.
    
    Args:
        narrator_id (str): The ID of the narrator to search for.
        size (int, optional): The maximum number of results to return. Defaults to 20.

    Returns:
        Dict[str, Any]: The search results containing commentary details.
    """
    query = {
        "bool": {
            "must": [
                {"bool": {"must": [{"match": {"id": narrator_id}}]}}
            ]
        }
    }
    
    extra_params = {
        "_source": {
            "includes": [
                "author", "commenter", "comments", "book", "name", "page", "volume"
            ],
            "excludes": []
        },
        "track_total_hits": True,
        "aggs": {"unique_commentators": {"cardinality": {"field": "commenter"}}},
        "sort": [
            {"commenter_dod": {"order": "asc"}},  # Sort by date of death of the commenter (ascending)
            {"commenter": {"order": "asc"}},  # Sort alphabetically by commenter name
            {"book_order": {"order": "asc"}}  # Sort by book order
        ]
    }
    
    return make_request("es-prod-euw1-narrator-commentary-12-read", "hadith_narr_comm_result", query, size, extra_params,meta={"narrator":narrator_id})
