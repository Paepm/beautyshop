from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from devtools import debug

from accounts.serializer.user_serializer import UserSerializer


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Handles viewing and editing the authenticated user's profile.
    """
    if request.method == "GET":
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == "PATCH":
        debug("[PATCH] Incoming data:", request.data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            debug("[PATCH] Successfully saved.")
            serializer.save()
            return Response(serializer.data)
        else:
            debug("[PATCH] Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
