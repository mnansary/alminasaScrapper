from alminasascrapper.common import make_request
from typing import Dict, Any, Optional,List

def search_hadith(size: int = 10, search_after:List=[1,1,1]) -> Dict[str, Any]:
    """
    Searches for Hadith records in Elasticsearch.
    
    Args:
        size (int, optional): The number of results to return. Defaults to 10.
        search_after (list[int,int,int]) : The data to search from

    Returns:
        Dict[str, Any]: The search results containing Hadith details.
    """
    query = {
        "bool": {
            "must": [
                {"bool": {"must": [{"match_all": {}}]}}
            ]
        }
    }
    
    extra_params = {
        "_source": {
            "includes": [
                "hadith_id", "hadith_serial_id", "number", "book_name", "type", "narrators", "extended_narrations",
                "raw_narrations", "narrations_numbers", "hasExplanation", "hasExtendedExplanation", "hasCommentary",
                "hasRuling", "hasExtendedRuling", "chapter", "sub_chapter", "page", "volume", "matn_with_tashkeel",
                "rulings", "rulings.ruler.keyword", "rulings.ruling.keyword", "rulings.book_name", "rulings.page",
                "rulings.volume", "ambiguous", "editions", "hadith", "hadith.tokenized", "hadith.exact"
            ],
            "excludes": []
        },
        "track_total_hits": True,
        "highlight": {
            "fields": {
                "hadith": {"pre_tags": ["<highlight>"], "post_tags": ["</highlight>"]},
                "hadith.tokenized": {"pre_tags": ["<highlight-light>"], "post_tags": ["</highlight-light>"]}
            },
            "number_of_fragments": 0
        },
        "sort": ["_score", {"authenticity_order": {"order": "asc"}}, {"hadith_serial_id": {"order": "asc"}}],
        "size":size,
        "search_after":search_after
    }
    
    return make_request("es-prod-euw1-hadith-12-read", "result", query, size, extra_params, meta={"query": "hadith_search"})