import json
import unittest
from manager import manager
from config import Config
from ky_omm.common.conversion_data import JSONEncoder


class FlaskTest(unittest.TestCase):
    """测试案例"""

    def setUp(self):
        manager.testing = True  # 开启测试模式
        self.client = manager.test_client()

    def test_add_order(self):
        """post测试函数"""
        data = {
            "video_type": "5",
            "video_id": "5x96pdd6dc84tgc",
            "num": "120",
            "comment_nums": "123"
        }

        resp = self.client.post("/add_order", json=data)
        resp = json.loads(resp.data)
        print(resp)
        self.assertEqual(resp["status"], 200)

    def test_back_order(self):
        """
        退单测试
        :return:
        """
        query_data = {
            "order_type": 5,
            "comment_id": "5x96pdd6dc84tgc"
        }

        res = Config.KS_HOST.find_one(query_data)
        dumps_result = json.dumps(res, cls=JSONEncoder)
        json_result = json.loads(dumps_result)

        data = {
            "video_type": json_result.get("order_type"),
            "order_id": json_result.get("_id")
        }

        resp = self.client.post("/back_order", json=data)
        resp = json.loads(resp.data)
        print(resp)
        self.assertEqual(resp["status"], 200)

    def test_query_order(self):
        """
            查询接口测试
        """
        res = Config.KS_HOST.aggregate([{'$sample': {'size': 1}}])

        uid = ""
        order_type = ""
        for i in res:
            dumps_result = json.dumps(i, cls=JSONEncoder)
            # json 转化
            json_result = json.loads(dumps_result)
            order_type = json_result.get("order_type")
            uid = json_result.get("_id")

        data = {
            "video_type": order_type,
            "order_id": uid
        }

        resp = self.client.post("/query_order", json=data)
        resp = json.loads(resp.data)
        print(resp)
        self.assertEqual(resp["status"], 200)


if __name__ == '__main__':
    # 启动所有测试
    unittest.main()
