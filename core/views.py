from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from accounts import models as accounts_models
from utils import main
from . import models
from . import serializers
from . import permissions


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def innovation_list(request):
    """
    List all innovations, or create a new innovation
    """
    if request.method == "GET":
        innovations = models.Innovation.objects.all()
        paginated_response = main.paginate(request, innovations, serializers.Innovation)
        return paginated_response

    elif request.method == "POST":
        serializer = serializers.Innovation(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.validated_data["author"] = request.user.user_profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([permissions.IsInnovationAuthorOrModOrReadOnly])
def innovation_detail(request, pk):
    """
    Contains methods for updating an innovation (either partially or entirely) and deleting an innovation
    """
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializers.Innovation(innovation, context={"request": request})
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = serializers.Innovation(
            innovation, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = serializers.Innovation(
            innovation, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        innovation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def innovation_comment_list(request, pk):
    """
    List all comments for a specific innovation, or create a comment for an innovation
    """
    if request.method == "GET":
        innovation_comments = models.InnovationComment.objects.filter(innovation_id=pk)
        serializer = serializers.InnovationComment(
            innovation_comments, many=True, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "POST":
        request.data["innovation"] = models.Innovation.objects.get(id=pk).pk

        serializer = serializers.InnovationComment(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.validated_data["author"] = request.user.user_profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes(
[permissions.IsInnovationAuthorOrCommentAuthorOrModOrStaffOrReadOnly]
)
def innovation_comment_detail(request, pk):
    """
    Contains methods for updating an innovation comment (either partially or entirely) and deleting an innovation comment
    """
    try:
        innovation_comment = models.InnovationComment.objects.get(pk=pk)
    except models.InnovationComment.DoesNotExist:
        return Response(
            {"detail": "Comment does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = serializers.InnovationComment(
            innovation_comment, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = serializers.InnovationComment(
            innovation_comment,
            data=request.data,
            partial=request.method == "PATCH",
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.validated_data["is_edited"] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        innovation_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
