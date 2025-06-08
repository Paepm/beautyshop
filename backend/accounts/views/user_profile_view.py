from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from devtools import debug
from django_countries import countries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.services.user_profile_service import UserProfileService


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        debug("[PROFILEVIEW GET] request.user", request.user)
        user_data = UserProfileService.get_user_profile(request.user)
        debug("[PROFILEVIEW GET]", user_data)
        return Response(user_data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer, success = UserProfileService.update_user_profile(
            request.user, request.data
        )
        if success:
            debug("[PROFILEVIEW PATCH] success get", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        debug("[PROFILEVIEW PATCH] error", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # this is just a soft delete, the user will be marked as deleted not deleted in db
        user = request.user
        user.is_active = False
        user.email = f"deleted_{user.id}@example.com"
        user.set_unusable_password()
        user.save()

        return Response(
            {"message": "User marked as deleted"}, status=status.HTTP_200_OK
        )


class CountryListView(APIView):
    def get(self, request):
        country_list = [{"code": code, "name": name} for code, name in list(countries)]
        return Response(country_list, status=status.HTTP_200_OK)
