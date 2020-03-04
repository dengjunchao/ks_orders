from config import Status
from flask_restful import Resource
from flask import request, jsonify
from ky_omm.common.add_order import AddOrder


class AddOrders(Resource):

    def post(self):
        """
        插入数据
        1.获取数据
        2.判断是否空值状态
        3.判断是否是纯数字
        4.不是纯数字，re 提取网址
        :return:返回插入成功后信息
        """
        if request.json:
            orders_type = request.json.get("orders_type", None)
            orders_id = request.json.get("orders_id", None)
            orders_counts = request.json.get("orders_counts", None)
            comment_counts = request.json.get("comment_counts", None)

            if not comment_counts:
                comment_counts = 0

            if orders_type is not "5" and int(comment_counts) is not 0:
                return {"status": 404, "msg": "comment_counts字段不允许传值"}

            if not orders_type or not orders_id or not orders_counts:
                return {"status": 404, "msg": "orders_type={} orders_id={} orders_counts={}".format(
                    orders_type, orders_id, orders_counts
                )}

            return jsonify(AddOrder(
                orders_type=orders_type,
                orders_id=orders_id,
                orders_counts=orders_counts,
                comment_counts=comment_counts
            ).add_data())

        else:
            return {'status': Status.FAILED, 'msg': 'no data'}
