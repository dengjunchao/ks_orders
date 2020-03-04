"""
    主页视图
"""

import json
from config import Status
from ky_omm.common.back_order import BackOrder
from ky_omm.common.query_order import QueryOrder
from flask import views, request, jsonify, render_template
from ky_omm.common.add_order import AddOrder



class Index(views.MethodView):
    def get(self):
        """
        主页面
        :return: 渲染主页
        """
        # print(request.headers)
        return render_template('index.html')

    def post(self):
        """
        插入数据
        1.获取数据
        2.判断是否空值状态
        3.判断是否是纯数字
        4.不是纯数字，re 提取网址
        :return:返回插入成功后信息
        """
        orders_type = request.form.get("insert_video_type", None)
        orders_id = request.form.get("orders_id", None).rstrip()
        orders_counts = request.form.get("orders_counts", None)
        comment_counts = request.form.get("comment_counts", None)

        if not comment_counts:
            comment_counts = 0
        if len(orders_id) == 0 and len(orders_counts) == 0:
            return {'status': Status.FAILED, 'msg': '输入值是空'}

        return jsonify(AddOrder(
                                orders_type=orders_type,
                                orders_id=orders_id,
                                orders_counts=orders_counts,
                                comment_counts=comment_counts
                                ).add_data())

    def put(self):
        """
        订单退订：获取数据，判断是否为空,然后执行
        :return:状态信息
        """
        orders_type = request.form.get("order_unsubscribe_type", None)
        orders_id = request.form.get("order_id", None)

        if len(orders_id) == 0 or len(orders_id) > 24:
            return {'status': Status.FAILED, 'msg': '输入值是空或者输入值错误'}

        return jsonify(BackOrder(orders_type=orders_type, orders_id=orders_id).back_order())

    def patch(self):
        # 获取数据
        file = request.files.get("file")
        file_data = str(file.read(), encoding="UTF-8-sig")
        datas = file_data.split("\r\n")

        list_res = []
        i = 0
        for data_res in datas:
            # 获取数据
            i += 1
            data_r = json.loads(data_res)
            orders_type = data_r.get("orders_type", None)
            orders_id = data_r.get("orders_id", None)
            orders_counts = data_r.get("orders_counts", None)
            comment_counts = data_r.get("comment_counts", None)

            if not comment_counts:
                comment_counts = 0

            res_data = AddOrder(
                orders_type=orders_type,
                orders_id=orders_id,
                orders_counts=orders_counts,
                comment_counts=comment_counts
            ).add_data()

            if res_data.get("status") == 404:
                list_res.append({'video_data': orders_id, 'msg': '验证未通过'})

        if len(list_res) == 0:
            return {'status': 200, 'msg': "上传成功"}
        else:
            return {'status': 404, 'msg': str(list_res)}


    def options(self):
        """
        查询订单号
        业务逻辑：判断是否符合视频id和订单id长度
        条件成立：执行QueryOrder.query_order()
        获取查询结果，然后进行判断，如果count =1 就是订单id号，大于1就是视频id号
        :return: 状态码和信息
        """

        data = json.loads(request.data.decode(encoding="utf-8"))
        orders_id = data.get("orders_id").rstrip()

        query_result = None
        if len(orders_id) <= 24:
            query_result = QueryOrder(orders_id=orders_id).query_order()

            if query_result.get('count', None) is None:
                return {'status': Status.FAILED, 'data': "订单号不存在"}
        else:
            return {'status': Status.FAILED, 'data': "订单号不存在"}

        return {'status': Status.SUCCEED, 'data': query_result.get('data')}
