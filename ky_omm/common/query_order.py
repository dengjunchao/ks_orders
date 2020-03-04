"""
    查询订单
"""
import json
from bson import ObjectId
from ky_omm.common.conversion_data import Conversion, JSONEncoder
from config import Config, Status, OrderType


class QueryOrder(object):
    def __init__(self, orders_id):
        """
        初始化
        :param data_type:数据类型
        :param data:数据
        """
        self.orders_id = orders_id
        self.mo_ky_omm = Config.KS_HOST

    def conversion_data(self, query_data, data_list):

        dumps_result = json.dumps(query_data, cls=JSONEncoder)
        # json 转化
        json_result = json.loads(dumps_result)
        # 数据类型转换
        Conversion(json_result).data_conversion()
        data_list.append(json_result)

        return data_list

    def find_data(self, query_data):
        count = 0
        data_list = []
        list_res = []
        data_tmp = self.mo_ky_omm.find(query_data)
        count_data = data_tmp.count()

        if count_data == 0:
            return {'status': Status.FAILED, 'msg': "订单不存在"}
        # 循环转化数据
        for i in data_tmp:
            list_res = self.conversion_data(i, data_list)
            count += 1
        return {'status': 200, 'count': count, 'data': list_res}

    def query_order(self):
        """

        :return:
        """
        count = 0
        data_list = []
        data_len = len(self.orders_id)
        list_res = []

        if data_len == OrderType.ORDER_ID_LEN:
            # 根据条件查询数据库
            query_data = self.mo_ky_omm.find_one(
                {'_id': ObjectId(self.orders_id)})

            if query_data is None:
                return {'status': Status.FAILED, 'msg': "订单不存在"}
            count = 1
            list_res = self.conversion_data(query_data, data_list)
            return {'count': count, 'data': list_res}

        if data_len > 11 and data_len < 20 :
            query_data = {"photo_name": str(self.orders_id)}
            return self.find_data(query_data)

        if data_len <= 11:
            query_data = {"photo_id": str(self.orders_id)}
            find_data = self.find_data(query_data)

            if find_data.get("status") == 200:
                return find_data
            else:
                query_data = {"user_id": str(self.orders_id)}
                return self.find_data(query_data)

        return {'status': Status.FAILED, 'msg': "订单不存在"}
