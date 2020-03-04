"""
    订单退订模块
"""
from flask import request
from config import Status
from flask_restful import Resource
from ky_omm.common.query_order import QueryOrder


class QueryOrders(Resource):

    def post(self):
        """
        查询订单号
        业务逻辑：判断是否符合视频id和订单id长度
        条件成立：执行QueryOrder.query_order()
        获取查询结果，然后进行判断，如果count =1 就是订单id号，大于1就是视频id号
        :return: 状态码和信息
        """
        if request.json:
            orders_id = request.json.get("orders_id", None).strip()

            if orders_id is None:
                return {'status': Status.FAILED, 'data': "video_type or order_id none"}

            query_result = QueryOrder(orders_id=orders_id).query_order()

            if query_result.get('count', None) is None:
                return {'status': Status.FAILED, 'data': "订单号不存在"}

            return {'status': Status.SUCCEED, 'data': query_result.get('data')}

        else:
            return {'status': Status.FAILED, 'msg': 'no data'}
