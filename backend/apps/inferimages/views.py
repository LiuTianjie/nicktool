from django.shortcuts import render

# Create your views here.

from django.db import models
from django.template.defaultfilters import filesizeformat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from apps.inferimages.models import ImageTask


# class LimitImageField(models.ImageField):
#     def __init__(self, *args, **kwargs):
#         self.max_upload_size = kwargs.pop("max_upload_size", [])
#         super().__init__(*args, **kwargs)
#
#     def clean(self, *args, **kwargs):
#         data = super().clean(*args, **kwargs)
#         file = data.file
#         try:
#             if file.size > self.max_upload_size:
#                 raise forms.ValidationError("上传图片大小不能超过：{}, 当前大小：{}".format(
#                     filesizeformat(self.max_upload_size), filesizeformat(file.size)))
#         except AttributeError:
#             pass
#         return data


class ImageTaskSerializers(serializers.ModelSerializer):
    image_content = serializers.ImageField()

    def validate_image_content(self, data):
        max_upload_size = 5242880
        try:
            if data.size > max_upload_size:
                raise serializers.ValidationError("上传图片大小不能超过：{}, 当前大小：{}".format(
                    filesizeformat(max_upload_size), filesizeformat(data.size)))
        except AttributeError:
            pass
        return data

    class Meta:
        model = ImageTask
        fields = ['image_content']


# 生产者，获取任务，上传到消息队列，数据库中存储相关状态
@api_view(['POST'])
def create_infer_task(request):
    serializer = ImageTaskSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 根据任务id查询已完成的任务
@api_view(['GET'])
def get_infer_image(request):
    task_id = request.query_params.get("task_id", None)
    if task_id:
        # TODO: Search image by id and return.
        return Response("success", status=status.HTTP_200_OK)
    else:
        return Response("Missing Parameter task_id!", status=status.HTTP_400_BAD_REQUEST)
