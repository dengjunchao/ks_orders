"""
    订单退订模块
"""
from bson import ObjectId
from config import Config, Status


class BackOrder(object):

    def __init__(self, orders_type, orders_id):
        """
        初始化
        :param data_type: 数据类型
        :param order_id: 数据
        """
        self.orders_type = orders_type
        self.orders_id = orders_id
        self.ks_database = Config.KS_HOST

    def __update_other_order(self, query_data, mongodb_link):
        photo_id = query_data["photo_id"]

        # 查询itme_id 列表
        item_id_all_order = mongodb_link.find({"photo_id": photo_id})

        for item_id_order in item_id_all_order:

            if item_id_order["orders_date"] > query_data["orders_date"]:

                item_id_order["start_number"] -= query_data["orders_counts"]
                mongodb_link.update_one({"_id": item_id_order["_id"]},
                                        {"$set": {"start_number": item_id_order["start_number"]}})

    def back_order(self):
        """
        订单退订
        根据传入的数据进行查询
        如果是空值就判断订单不存在
        如果是已经退订就，返回重复退订
        :return:状态信息
        """

        query_data = self.ks_database.find_one({'_id': ObjectId(self.orders_id)})

        if query_data is None:
            return {'status': Status.FAILED, 'msg': "订单号不存在"}
        else:

            # 状态为等待退单
            if query_data["sign"] == 2:
                return {'status': 2, 'msg': "wait for robot quit"}

            elif query_data["sign"] == 3:
                self.__update_other_order(query_data, self.ks_database)
                self.ks_database.update_many({"_id": query_data["_id"]}, {"$set": {"sign": 4}})
                return {"status": 0, "msg": query_data["orders_counts"]}

                # 订单已经完成
            elif query_data["sign"] == 1:
                if query_data["orders_state"] == 2 or query_data["orders_counts"] <= query_data["robots_number"]:
                    return {"status": 1, "msg": "order is done!"}

                # 订单状态未开始
                if query_data["orders_state"] == 0:
                    self.__update_other_order(query_data, self.ks_database)
                    self.ks_database.update_many({"_id": query_data["_id"]}, {"$set": {"sign": 3}})
                    return {"status": Status.SUCCEED, "msg": query_data["orders_counts"]}

                # 修改订单状态为等待退单
                self.ks_database.update_many({"_id": query_data["_id"]}, {"$set": {"sign": 2}})
                return {'status': 2, 'msg': "wait for robot quit"}
            elif query_data["sign"] == 4:
                return {'status': 404, 'msg': "if you want know more info, please say fcky!"}
