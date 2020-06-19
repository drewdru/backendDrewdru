import json
import os
import uuid

import magic
import redis
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
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


class MissingParameterException(APIException):
    status_code = 400
    default_detail = "MISSING_PARAMETER"


class WrongParameterTypeException(APIException):
    status_code = 400
    default_detail = "WRONG_VALUE_TYPE"


class WrongFileTypeException(WrongParameterTypeException):
    default_detail = "WRONG_FILE_TYPE"


from django import forms

class PdfForOcrForm(forms.Form):
    lang = forms.CharField(label=_('Language'), max_length=100)
    file = forms.FileField(label=_('File'), )


class OcrView(APIView):
    """
    API endpoint that allows to pass session beetwen subdomains.
    """

    def get(self, request, *args, **kwargs):
        uid = request.GET.get("uid", "")
        status = redis_instance.get(f"status_{uid}")
        progress = redis_instance.get(f"progress_{uid}")
        if progress is None:
            progress = 0
        else:
            progress = float(progress)
        result = ""
        if status == b"done":
            result = redis_instance.get(uid)
        return Response(
            {"result": result, "status": status, "progress": progress}
        )

    def post(self, request, *args, **kwargs):
        uid = str(uuid.uuid4())
        uid = f"ocr_{uid}"
        form = PdfForOcrForm(request.POST, request.FILES)
        if form.is_valid():
            form_file = form.cleaned_data.get('file')
            mime = form_file.content_type
            
            document_type = magic.from_buffer(
                form_file.read(2048)
            ).upper()
            form_file.seek(0)
            
            if mime != 'application/pdf' or not "PDF" in document_type:
                raise WrongFileTypeException
            
            path = f"{TEMP_DIR}{uid}.pdf"
            with open(path, "ab+") as destination:
                for chunk in form_file.chunks():
                    destination.write(chunk)

            lang = form.cleaned_data.get("lang", "ru_kz")

            redis_instance.set(f"status_{uid}", "init")            
            recognize.delay(path, uid, lang)
        else:
            raise MissingParameterException

        return Response({"uid": uid})
