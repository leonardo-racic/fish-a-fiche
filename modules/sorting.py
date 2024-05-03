def sort_results_by_keywords(cs: list, keywords: str = "") -> list:
    if keywords == "":
        return cs
    

    def sort_func(current_cs: dict) -> tuple:
        current_context: str = current_cs["context"]
        index: int = 0
        for k in keywords.split():
            if k in current_context.split():
                index += 1
        dislikes: int = len(current_cs["dislikes"])
        likes: int = len(current_cs["likes"])
        difference: int = likes - dislikes
        return index, difference
    

    results: list = sorted(cs, key=sort_func, reverse=True)
    return results


def sort_results_by_likes(cs: list) -> list:
    def sort_func(current_cs: dict) -> int:
        dislikes: int = len(current_cs["dislikes"])
        likes: int = len(current_cs["likes"])
        difference: int = likes - dislikes
        return difference
    results: list = sorted(cs, key=sort_func, reverse=True)
    return results