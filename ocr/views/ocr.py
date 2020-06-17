import json
import os
import uuid

import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_sso import claims
from rest_framework_sso.authentication import JWTAuthentication

from ocr.tasks.recognize import recognize

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = f"{BASE_DIR}/temp/"


class OcrView(APIView):
    """
    API endpoint that allows to pass session beetwen subdomains.
    """

    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid", "")
        print("UID:", uid)
        status = redis_instance.get(f"status_{uid}")
        result = ""
        print(status, type(status))
        if status == b"done":
            result = redis_instance.get(uid)
            print(result)
        return Response({"result": result, "status": status})

    def post(self, request, *args, **kwargs):
        uid = str(uuid.uuid4())
        uid = f"ocr_{uid}"
        if request.FILES["file"]:
            path = f"{TEMP_DIR}{uid}.pdf"
            with open(path, "ab+") as destination:
                for chunk in request.FILES["file"].chunks():
                    destination.write(chunk)
            redis_instance.set(f"status_{uid}", "init")
            recognize.delay(path, uid)
        else:
            redis_instance.set(uid, "File is not an Image")
            redis_instance.set(f"status_{uid}", f"done")
        return Response({"uid": uid})
