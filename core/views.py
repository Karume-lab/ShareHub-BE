from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from utils import main
from . import models
from . import serializers


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
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
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = serializers.Innovation(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.validated_data["author"] = request.user.user_profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def innovation_zip(request, pk):
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.InnovationZipFile(innovation, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
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

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not (
        request.user.is_staff
        or request.user.is_site_mod
        or request.user.user_profile == innovation.author
    ):
        return Response(
            {"detail": "You do not have permission to access this resource."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method in ["PUT", "PATCH"]:
        serializer = serializers.Innovation(
            innovation,
            data=request.data,
            partial=request.method == "PATCH",
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        innovation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def innovation_like_list(request, pk):
    """
    List all likes for an innovation, or like an innovation
    """
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        likes = models.Like.objects.filter(innovation=innovation)
        paginated_response = main.paginate(request, likes, serializers.Like)
        return paginated_response

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if innovation.get_is_liked(request.user.user_profile):
            return Response(
                {"detail": "You already liked this innovation"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            innovation.likes_number += 1
            serializer = serializers.Like(
                data=request.data, context={"request": request}
            )

            if serializer.is_valid():
                serializer.validated_data["author"] = request.user.user_profile
                serializer.validated_data["innovation"] = innovation
                serializer.save()
                innovation.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_innovation_like_list(request):
    pass


@api_view(["DELETE"])
def unlike_innovation(request, pk):
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if innovation.get_is_liked(request.user.user_profile):
        try:
            innovation.likes_number -= 1
            innovation.save()
            like = innovation.likes.get(author=request.user.user_profile)
            like.delete()
            return Response(
                {"detail": "Unliked innovation"}, status=status.HTTP_204_NO_CONTENT
            )
        except models.Like.DoesNotExist:
            return Response(
                {"detail": "Like does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"detail": "You already unliked this innovation"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def bookmark_innovation(request, pk):
    """
    Bookmark an innovation
    """
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if innovation.get_is_bookmarked(request.user.user_profile):
        return Response(
            {"detail": "You already bookmarked this innovation"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        serializer = serializers.Bookmark(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.validated_data["user"] = request.user.user_profile
            serializer.validated_data["innovation"] = innovation
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_bookmarks(request):
    bookmarks = models.Bookmark.objects.filter(user=request.user.user_profile)
    paginated_response = main.paginate(request, bookmarks, serializers.Bookmark)
    return paginated_response


@api_view(["DELETE"])
def unbookmark_innovation(request, pk):
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if innovation.get_is_bookmarked(request.user.user_profile):
        try:
            bookmark = innovation.user_bookmarks.get(user=request.user.user_profile)
            bookmark.delete()
            return Response(
                {"detail": "Deleted bookmark"}, status=status.HTTP_204_NO_CONTENT
            )
        except models.Bookmark.DoesNotExist:
            return Response(
                {"detail": "Bookmark does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"detail": "You have not bookmarked this innovation"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def innovation_comment_list(request, pk):
    """
    List all comments for a specific innovation, or create a comment for an innovation
    """
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(
            {"detail": "Innovation does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        innovation_comments = models.InnovationComment.objects.filter(innovation_id=pk)
        paginated_response = main.paginate(
            request, innovation_comments, serializers.InnovationComment
        )
        return paginated_response

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        request.data["innovation"] = models.Innovation.objects.get(id=pk).pk

        serializer = serializers.InnovationComment(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.validated_data["author"] = request.user.user_profile
            innovation.comments_number += 1
            innovation.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def innovation_comment_detail(request, pk, cpk):
    """
    Contains methods for updating an innovation comment (either partially or entirely) and deleting an innovation comment
    """
    try:
        innovation = models.Innovation.objects.get(pk=pk)
    except models.Innovation.DoesNotExist:
        return Response(
            {"detail": "Innovation does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        innovation_comment = models.InnovationComment.objects.get(pk=cpk)
    except models.InnovationComment.DoesNotExist:
        return Response(
            {"detail": "Comment does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = serializers.InnovationComment(
            innovation_comment, context={"request": request}
        )
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not (
        request.user.is_staff
        or request.user.is_site_mod
        or request.user.user_profile == innovation_comment.author
    ):
        return Response(
            {"detail": "You do not have permission to access this resource."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method in ["PUT", "PATCH"]:
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
        innovation.comments_number -= 1
        innovation.save()
        innovation_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
