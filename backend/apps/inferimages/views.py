import json
import uuid

from django.shortcuts import render

# Create your views here.

from django.db import models
from django.template.defaultfilters import filesizeformat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from apps.inferimages.models import ImageTask
from apps.inferimages.produce import ImageTaskProducer


class ImageTaskSerializers(serializers.ModelSerializer):
    image_content = serializers.ImageField()
    task_id = serializers.CharField(required=False)
    task_status = serializers.BooleanField(required=False, default=False)

    def validate_image_content(self, data):
        # 校验文件大小
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
        fields = ['image_content', 'task_id', 'task_status']


# 生产者，获取任务，上传到消息队列，数据库中存储相关状态
@api_view(['POST'])
def create_infer_task(request):
    serializer = ImageTaskSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # TODO: 先校验文件的hash值是否已经在redis中，如果是，表示该任务已经创建过，返回已创建的task_id即可
        task_id = uuid.uuid4()
        serializer.save(task_id=task_id, task_status=False)
        image = ImageTask.objects.filter(task_id=task_id).first()
        ImageTaskProducer.publish(json.dumps(ImageTaskSerializers(image).data))
        return Response({"code": 200, "message": "上传成功！", "task_id": task_id}, status=status.HTTP_201_CREATED)


# 根据任务id查询已完成的任务
@api_view(['GET'])
def get_infer_image(request):
    task_id = request.query_params.get("task_id", None)
    if task_id:
        image = ImageTask.objects.filter(task_id=task_id).first()
        if image:
            return Response({"msg": "success", "code": 200, "image": ImageTaskSerializers(image).data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"msg": "没有查询到任务", "code": 400, "task_id": task_id},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"msg": "缺少task_id参数！", "code": 400}, status=status.HTTP_400_BAD_REQUEST)
