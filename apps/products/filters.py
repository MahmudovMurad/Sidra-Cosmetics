from django.db.models import Q, QuerySet


def filter_products(queryset, query_params) -> (QuerySet, dict):
    search_query_params = {}
    filter_ = Q()


    category = query_params.get("category", None)
    if category:
        filter_.add(
            Q(category_id=category), Q.AND
        )
        search_query_params["category"] = category


    min_price = query_params.get("min_price", None)
    if min_price:
        filter_.add(
            Q(final_price__gte=min_price), Q.AND
        )
        search_query_params["min_price"] = min_price

    max_price = query_params.get("max_price", None)
    if max_price:
        filter_.add(
            Q(final_price__lte=max_price), Q.AND
        )
        search_query_params["max_price"] = max_price

    search = query_params.get("search", None)
    if search:
        filter_.add(
            Q(name__icontains=search), Q.AND
        )
        search_query_params["search"] = search

    return queryset.filter(filter_), search_query_params