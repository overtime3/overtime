"""
Miscellaneous tools related to centrality.
"""
from operator import itemgetter


def order_centrality(centralities):
    """
    Returns a view of a dictionary which relates nodes to centrality values so that items are ordered by centrality
    value.
    """
    ordered_centralities = sorted(centralities.items(), key=itemgetter(1), reverse=True)
    return ordered_centralities
