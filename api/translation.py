from modeltranslation.translator import TranslationOptions, translator

from api.models.task import Task


class TaskTranslation(TranslationOptions):
    fields = ("name", "description")


translator.register(Task, TaskTranslation)
