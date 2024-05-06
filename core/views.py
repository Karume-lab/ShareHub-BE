from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models
from accounts import models as accounts_models
from . import serializers
from . import utils



@api_view(["GET", "POST"])
def innovation_list(request):
    """
    List all innovations, or create a new innovation
    """
    if request.method == "GET":
        innovations = models.Innovation.objects.all()
        paginated_response = utils.paginate(request, innovations, serializers.Innovation)
        return paginated_response

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        data = request.data.copy()
        user_profile = accounts_models.UserProfile.objects.get(
            pk=request.user.user_profile.pk
        )
        data["author"] = user_profile.pk
        serializer = serializers.Innovation(data=data, context={"request": request})
        if serializer.is_valid():
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
