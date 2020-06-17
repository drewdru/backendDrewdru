from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_sso import claims, views

from api.models.user import UserProfile

User = get_user_model()


def create_authorization_payload(session_token, user, profile, **kwargs):
    return {
        claims.TOKEN: claims.TOKEN_AUTHORIZATION,
        claims.SESSION_ID: session_token.pk,
        claims.USER_ID: user.pk,
        claims.EMAIL: user.email,
        "profile": profile.pk,
    }


def authenticate_payload(payload):
    user, created = User.objects.get_or_create(
        service=payload.get(claims.ISSUER),
        external_id=payload.get(claims.USER_ID),
    )
    if not user.is_active:
        raise exceptions.AuthenticationFailed(_("User inactive or deleted."))
    return user


class ObtainAuthorizationTokenView(views.ObtainAuthorizationTokenView):
    """
    Returns a JSON Web Token that can be used for authenticated requests.
    """

    serializer_class = AuthorizationTokenSerializer


class AuthorizationTokenSerializer(serializers.Serializer):
    profile = serializers.HyperlinkedRelatedField(
        queryset=UserProfile.objects.all(),
        required=True,
        view_name="api:profile-detail",
    )

    class Meta:
        fields = ["profile"]
