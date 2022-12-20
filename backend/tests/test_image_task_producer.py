import json
import time
import unittest

from apps.inferimages.produce import ImageTaskProducer


class TestImageTaskProducer(unittest.TestCase):
    ImageTaskProducer.publish(json.dumps({"task_id": 1, "message": "test"}))
