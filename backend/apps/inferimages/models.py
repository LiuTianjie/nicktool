from django.db import models


class ImageTask(models.Model):
    task_id = models.CharField(max_length=255, null=True, blank=True)
    infer_time = models.DateTimeField(null=True, blank=True)
    task_status = models.BooleanField(default=False)
    image_content = models.ImageField()
    image_after = models.ImageField(null=True)
