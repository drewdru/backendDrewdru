import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.dispatch import receiver

import api.schema

User = get_user_model()

from graphql_jwt.refresh_token.signals import (  # token_issued,; token_refreshed,
    refresh_token_revoked,
    refresh_token_rotated,
)


class Query(api.schema.TaskQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


# class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
#     user = graphene.Field(User)

#     @classmethod
#     def resolve(cls, root, info, **kwargs):
#         return cls(user=info.context.user)


class Mutation(api.schema.TaskMutations, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    # delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    # delete_refresh_token_cookie = (
    #     graphql_jwt.refresh_token.DeleteRefreshTokenCookie.Field()
    # )


schema = graphene.Schema(query=Query, mutation=Mutation)

# signals
# @receiver(token_issued)
# def on_user_authenticated(sender, request, user, **kwargs):
#     # Sent when a user authenticates successfully
#     pass
# @receiver(token_refreshed)
# def on_user_token_refreshed(sender, request, user, **kwargs):
#     # Sent when a single token has been refreshed.
#     pass
# @receiver(refresh_token_rotated)
# def on_refresh_token_rotated(sender, request, refresh_token, refresh_token_issued, **kwargs):
#     # Sent when a long running refresh token has been rotated
#     pass
# @receiver(refresh_token_revoked)
# def on_refresh_token_revoked(sender, request, refresh_token, refresh_token_issued, **kwargs):
#     # Sent when a long running refresh token has been revoked
#     pass
