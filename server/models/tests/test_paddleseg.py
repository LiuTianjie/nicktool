import unittest

from server.models.PaddleSeg.Matting.main import test


class TestPaddleSeg(unittest.TestCase):

    def test_single(self):
        test()
