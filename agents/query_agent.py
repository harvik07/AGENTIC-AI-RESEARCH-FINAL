
def generate_queries(topic):
    """
    Generate diverse research queries for broader search coverage.
    Works for any topic globally.
    """

    queries = [
        f"{topic} overview research report",
        f"{topic} market size statistics",
        f"{topic} major companies organizations",
        f"{topic} industry trends future outlook",
        f"{topic} challenges limitations issues"
    ]

    # limit queries to avoid Tavily API overuse
    return queries[:3]