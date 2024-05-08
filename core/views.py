from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from accounts import models as accounts_models
from . import serializers
from utils import main


@api_view(["GET", "POST"])
def innovation_list(request):
    """
    List all innovations, or create a new innovation
    """
    if request.method == "GET":
        innovations = models.Innovation.objects.all()
        paginated_response = main.paginate(request, innovations, serializers.Innovation)
        return paginated_response

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    serializer = serializers.Innovation(data=request.data, context={"request": request})

    if serializer.is_valid():
        serializer.validated_data["author"] = request.user.user_profile
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
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
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user != innovation.author.user:
            return Response(
                {"detail:" "Cannot update"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.Innovation(
            innovation, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user != innovation.author.user:
            return Response(
                {"detail": "Cannot update"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.Innovation(
            innovation, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user != innovation.author.user:
            return Response(
                {"detail:" "Cannot delete"}, status=status.HTTP_400_BAD_REQUEST
            )
        innovation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
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
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
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
def innovation_comment_detail(request, pk):
    """
    Contains methods for updating an innovation comment (either partially or entirely) and deleting an innovation comment
    """
    try:
        innovation_comment = models.InnovationComment.objects.get(pk=pk)
    except models.InnovationComment.DoesNotExist:
        return Response({"detail": "Comment does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializers.InnovationComment(
            innovation_comment, context={"request": request}
        )
        return Response(serializer.data)

    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user != innovation_comment.author.user:
            return Response(
                {"detail:" "Cannot update"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.InnovationComment(
            innovation_comment, data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user != innovation_comment.author.user:
            return Response(
                {"detail": "Cannot update"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.InnovationComment(
            innovation_comment,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user != innovation_comment.author.user:
            return Response(
                {"detail:" "Cannot delete"}, status=status.HTTP_400_BAD_REQUEST
            )
        innovation_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
