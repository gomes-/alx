__author__ = 'Alex Gomes'

import unittest
import os, sys

path_file = os.path.abspath(__file__)
dir_path = os.path.dirname(path_file)
dir_top = os.path.split(dir_path)[0]
dir_alxlib = os.path.join(dir_top, 'alxlib')


if os.path.isdir(dir_alxlib):
    sys.path.insert(0, dir_top)

from alxlib.cloud.azure import Azure


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_connect_sqs(self):
        az=Azure()
        result = az.connect_sqs()
        self.assertIsNotNone(result)


    def test_base64(self):
        az=Azure()
        dict={"test":"test", "test2":"blah"}
        result = az.msg_decode(az.msg_encode(dict))
        self.assertDictEqual(result, dict)

if __name__ == '__main__':
    unittest.main()
