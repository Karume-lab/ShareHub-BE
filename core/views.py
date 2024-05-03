from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers


@api_view(["GET", "POST"])
def innovation_list(request):
    """
    List all innovations, or create a new innovation
    """
    if request.method == "GET":
        innovation = models.Innovation.objects.all()
        serializer = serializers.Innovation(innovation, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = serializers.Innovation(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def innovation_detail(request, slug):
    """
    Contains methods for updating an innovation (either partially or entirely) and deleting an innovation
    """
    try:
        innovation = models.Innovation.objects.get(slug=slug)
    except innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializers.Innovation(innovation)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = serializers.Innovation(serializers, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = serializers.Innovation(
            serializers, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        innovation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
