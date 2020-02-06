# schema.py
import graphene

from graphene_django import DjangoObjectType
from graphql_relay.node.node import from_global_id

from api.models import PostModel
from api.models import UserModel
from api.models import TaskModel

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

class UserQuery(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        return UserModel.objects.all()

# schema = graphene.Schema(query=Query)

# query = '''
#     query {
#       users {
#         name,
#         lastName
#       }
#     }
# '''
# results = schema.execute(query)
# print(results)




class TaskModelType(DjangoObjectType):
    class Meta:
        model = TaskModel


class CreateTask(graphene.Mutation):
    ok = graphene.Boolean()
    task = graphene.Field(lambda: TaskModelType)

    class Arguments:
      	name = graphene.String()
      	description = graphene.String()

    def mutate(self, info, name, description):
      	task = TaskModel(name = name, description = description, isDone = False)
      	task.save()
      	ok = True
      	return CreateTask(task=task,ok=ok)


class UpdateTask(graphene.Mutation):
    task = graphene.Field(lambda: TaskModelType)
    ok =  graphene.Boolean()

    class Arguments:
        id = graphene.String()
        IsDone = graphene.Boolean()
    
    def mutate(self, info, id, IsDone):
        task = TaskModel.objects.get(pk=id)
        task.isDone = IsDone
        task.save()
        ok = True
        return UpdateTask(task=task,ok=ok)


class TaskQuery(graphene.ObjectType):
    tasks = graphene.List(TaskModelType)

    def resolve_tasks(self, info):
        return TaskModel.objects.all()


class TaskMutations(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()

