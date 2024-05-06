from rest_framework.pagination import PageNumberPagination


def paginate(request, listing, Serializer):
    paginator = PageNumberPagination()
    paginated_results = paginator.paginate_queryset(listing, request=request)
    serializer = Serializer(paginated_results, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)
