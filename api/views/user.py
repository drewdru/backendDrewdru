from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_sso import claims
from rest_framework_sso.authentication import JWTAuthentication

from api.models.user import UserProfile

User = get_user_model()


class SessionViewSet(APIView):
    """
    API endpoint that allows to pass session beetwen subdomains.
    """

    def get(self, request):
        print(request.session.__dict__)
        print(request.COOKIES)
        print(request.GET)
        return Response(status=HTTP_202_ACCEPTED)


class UserSerializer(serializers.Serializer):
    profile = serializers.HyperlinkedRelatedField(
        queryset=UserProfile.objects.all(),
        required=True,
        view_name="api:profile-detail",
    )

    class Meta:
        fields = ["profile"]


class UserViewSet(ModelViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    queryset = User.objects.none().prefetch_related("user_profile")
    serializer_class = UserSerializer
    # permission_classes = (IsAdminOrReadOnly,)

    def get(self, request):
        if not request.user.is_authenticated or not request.auth:
            return self.none()
        return User.objects.filter(
            service=request.auth.get(claims.ISSUER),
            external_id=request.auth.get(claims.USER_ID),
        )
