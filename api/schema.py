# schema.py
import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from api.models import Post, Task

User = get_user_model()


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        return PostNode.objects.get(id=id)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)

        posts = graphene.List(PostNode)

    def resolve_users(self, info):
        return PostNode.objects.filter(user=self)

    @classmethod
    def get_node(cls, info, id):
        return User.objects.get(id=id)


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserNode)

    def resolve_users(self, info):
        return UserNode.objects.all()


# schema = graphene.Schema(query=Query)

# query = '''
#     query {
#       users {
#         first_name,
#         last_name
#       }
#     }
# '''
# results = schema.execute(query)
# print(results)


class TaskNode(DjangoObjectType):
    class Meta:
        model = Task


class CreateTask(graphene.Mutation):
    ok = graphene.Boolean()
    task = graphene.Field(lambda: TaskNode)

    class Arguments:
        name = graphene.String()
        description = graphene.String()

    @login_required
    def mutate(self, info, name, description):
        task = Task(name=name, description=description, is_done=False)
        task.save()
        ok = True
        return CreateTask(task=task, ok=ok)


class UpdateTask(graphene.Mutation):
    task = graphene.Field(lambda: TaskNode)
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.String()
        is_done = graphene.Boolean()

    # @login_required
    # @staff_member_required
    # @superuser_required
    # @user_passes_test(lambda user: user.email.contains('@staff'))
    # @permission_required('auth.change_user')
    def mutate(self, info, id, is_done):
        task = Task.objects.get(pk=id)
        task.is_done = is_done
        task.save()
        ok = True
        return UpdateTask(task=task, ok=ok)


class TaskQuery(graphene.ObjectType):
    tasks = graphene.List(TaskNode)  # , token=graphene.String(required=True))

    def resolve_tasks(self, info):
        return Task.objects.all()


class TaskMutations(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
