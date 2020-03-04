"""
    数据类型转化
"""
import time
import json
from bson import ObjectId


class Conversion(object):

    def __init__(self, data):
        """
        :param data: 数据库查询到数据
        """
        self.data = data

    def data_conversion(self):
        """
        时间戳数据转化，数据类型转化中文数据类型
        :return: 无返回
        """
        time_stamp = self.data.get('orders_date', None)
        time_array = time.localtime(int(time_stamp * 0.001))
        other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

        self.data['orders_date'] = other_style_time

        if self.data.get('orders_type', None) == 1:
            self.data['orders_type'] = "点赞"

        if self.data.get('orders_type', None) == 2:
            self.data['orders_type'] = "关注"

        if self.data.get('orders_type', None) == 3:
            self.data['orders_type'] = "评论"

        if self.data.get('orders_type', None) == 4:
            self.data['orders_type'] = "播放量"

        if self.data.get('orders_type', None) == 5:
            self.data['orders_type'] = "评论赞"

        if self.data.get('sign', None) == 1:
            self.data['sign'] = "正常"

        if self.data.get('sign', None) == 2:
            self.data['sign'] = "退单"

        if self.data.get('sign', None) == 3:
            self.data['sign'] = "操作完成"

        if self.data.get('sign', None) == 4:
            self.data['sign'] = "异常"

        if self.data.get('orders_state', None) == 0:
            self.data['orders_state'] = "未开始"

        if self.data.get('orders_state', None) == 1:
            self.data['orders_state'] = "进行中"

        if self.data.get('orders_state', None) == 2:
            self.data['orders_state'] = "操作完成"


class JSONEncoder(json.JSONEncoder):
    """
    转化 ObjectId
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
