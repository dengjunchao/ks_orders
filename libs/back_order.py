from config import Status
from flask_restful import Resource
from flask import request, jsonify
from ky_omm.common.back_order import BackOrder


class BackOrders(Resource):

    def post(self):
        """
         订单退订：获取数据，判断是否为空,然后执行
         :return:状态信息
        """
        if request.json:
            orders_type = request.json.get("orders_type", None)
            orders_id = request.json.get("orders_id", None).strip()

            if not orders_type or not orders_id:
                return {"status": Status.FAILED, "msg": "video_type={} order_id={}".format(
                    orders_type, orders_id
                )}
            return jsonify(BackOrder(orders_type=orders_type, orders_id=orders_id).back_order())
        else:
            return {'status': Status.FAILED, 'msg': 'no data'}
