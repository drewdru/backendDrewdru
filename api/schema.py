# schema.py
import graphene

from graphene_django import DjangoObjectType

from .models import PostModel
from .models import UserModel

class Post(DjangoObjectType):
    class Meta:
        model = PostModel
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return Post.objects.get(id=id)

class User(DjangoObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)

        posts = graphene.List(Post)

    def resolve_users(self, info):
        return Post.objects.filter(user=self)

    @classmethod
    def get_node(cls, info, id):
        return User.objects.get(id=id)

class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return UserModel.objects.all()

schema = graphene.Schema(query=Query)

query = '''
    query {
      users {
        name,
        lastName
      }
    }
'''
results = schema.execute(query)
print(results)