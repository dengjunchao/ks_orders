"""
    添加数据模块
"""
import time
from config import Config, Status, OrderType
from ky_omm.common.rerify import photo_info


class AddOrder(object):
    """
        增加订单
    """

    def __init__(self, orders_type, orders_id, orders_counts, comment_counts):
        """
        初始化
        :param data_type: 数据类型
        :param data: 数据
        mo_Ky_omm 数据库链接
        """
        self.orders_type = int(orders_type)
        self.orders_id = orders_id
        self.orders_counts = int(orders_counts)
        self.comment_counts = comment_counts
        self.ks_database = Config.KS_HOST
        self.start_number = 0

    def insert_data(self, query_data, start_num=0, photo_name="",
                    user_id="", user_name="", photo_id="", comment_id="", comment_nums=0
                    ):
        """
        插入数据到数据库
        :param query_data: 查询数据
        :param start_num: 开始数量
        :param user_id: 用户id
        :param photo_id: 作品id
        :param comment_id: 评论点赞ip
        :return: 返回状态码、id号、开始数量
        """

        query_res = self.ks_database.find(query_data).sort('order_date')

        if query_res.count() >= 1:
            last_data = query_res[query_res.count() - 1]
            self.start_number = int(start_num) + int(last_data["order_count"])

        self.start_number = start_num

        order_id = self.ks_database.insert_one({
            'orders_type': int(self.orders_type),
            'user_id': str(user_id),
            'user_name': user_name,
            'photo_name': photo_name,
            'photo_id': str(photo_id),
            'comment_id': str(comment_id),
            "comment_rows": comment_nums,
            'orders_date': int(time.time() * 1000),
            'start_number': int(self.start_number),
            'now_number': 0,
            'orders_state': 0,
            'work_status': 0,
            "sign": 1,
            "robots_number": 0,
            "orders_counts": int(self.orders_counts)
        })

        return {'status': Status.SUCCEED, "orders_id": str(order_id.inserted_id), "start_number": self.start_number}

    def like(self):
        """
        点赞业务
        对数据验证
        如果数据验证成功就调用add_data 方法
        :return:状态信息
        """
        verify_res = photo_info(self.orders_id)
        status = verify_res.get("status")

        if status == 404:
            return {'status': Status.FAILED, "msg": verify_res.get("msg", None)}

        if status == 200:
            photo_id = verify_res.get("photo_id", None)
            user_id = verify_res.get("user_id", None)
            user_name = verify_res.get("user_name", None)
            query_data = {"photo_id": photo_id, 'order_type': self.orders_type, "order_state": {"$ne": 2}}

            return self.insert_data(
                query_data=query_data,
                photo_name=self.orders_id,
                start_num=self.start_number,
                user_id=user_id,
                photo_id=photo_id,
                user_name=user_name,
                comment_nums=0
            )
        else:
            return {'status': Status.FAILED, 'msg': 'video_id({}) is not legal!'.format(self.orders_id)}

    def attention(self):
        """
        关注业务
        :return:状态信息
        """
        verify_res = photo_info(self.orders_id)
        status = verify_res.get("status")

        if status == 404:
            return {'status': Status.FAILED, "msg": verify_res.get("msg", None)}

        if status == 200:
            photo_id = verify_res.get("photo_id", None)
            user_id = verify_res.get("user_id", None)
            user_name = verify_res.get("user_name", None)
            query_data = {"photo_id": photo_id, 'order_type': self.orders_type, "order_state": {"$ne": 2}}

            return self.insert_data(
                query_data=query_data,
                start_num=self.start_number,
                user_id=user_id,
                user_name=user_name,
                comment_nums=0
            )
        else:
            return {'status': Status.FAILED, 'msg': 'video_id({}) is not legal!'.format(self.orders_id)}

    def comment_like(self):
        """
        评论赞
        :return:状态信息
        """
        verify_res = photo_info(self.orders_id)
        status = verify_res.get("status")

        if status == 404:
            return {'status': Status.FAILED, "msg": verify_res.get("msg", None)}

        if status == 200:
            photo_id = verify_res.get("photo_id", None)
            user_id = verify_res.get("user_id", None)
            start_num = verify_res.get("view_count", None)
            user_name = verify_res.get("user_name", None)

            query_data = {"photo_id": photo_id, 'order_type': self.orders_type, "order_state": {"$ne": 2}}

            return self.insert_data(
                query_data=query_data,
                photo_name=self.orders_id,
                start_num=start_num,
                user_id=user_id,
                photo_id=photo_id,
                user_name=user_name,
                comment_nums=0
            )
        else:
            return {'status': Status.FAILED, 'msg': 'video_id({}) is not legal!'.format(self.orders_id)}

    def paly_number(self):
        """
        播放量
        对数据验证
        如果数据验证成功就调用add_data 方法
        :return:状态信息
        """
        verify_res = photo_info(self.orders_id)
        status = verify_res.get("status")

        if status == 404:
            return {'status': Status.FAILED, "msg": verify_res.get("msg", None)}

        if status == 200:
            photo_id = verify_res.get("photo_id", None)
            user_id = verify_res.get("user_id", None)
            start_num = verify_res.get("view_count", None)
            user_name = verify_res.get("user_name", None)

            query_data = {"photo_id": photo_id, 'order_type': self.orders_type, "order_state": {"$ne": 2}}

            return self.insert_data(
                query_data=query_data,
                photo_name=self.orders_id,
                start_num=start_num,
                user_id=user_id,
                photo_id=photo_id,
                user_name=user_name,
                comment_nums=0
            )
        else:
            return {'status': Status.FAILED, 'msg': 'video_id({}) is not legal!'.format(self.orders_id)}

    def comment_praise(self):
        """
        评论赞
        :return:
        """
        query_data = {"user_id": self.orders_id, 'order_type': self.orders_type, "order_state": {"$ne": 2}}

        if len(self.orders_id) == 9:
            return self.insert_data(query_data=query_data, user_id=self.orders_id, comment_nums=self.comment_counts)
        if len(self.orders_id) == 15:
            return self.insert_data(query_data=query_data, comment_id=self.orders_id, comment_nums=self.comment_counts)
        else:
            return {'status': Status.FAILED, 'msg': 'video_id({}) is not legal!'.format(self.orders_id)}

    def add_data(self):
        """
        根据类型来执行对应方法
        :return:
        """
        if OrderType.LIKE == self.orders_type:
            return self.like()

        if OrderType.ATTENTION == self.orders_type:
            return self.attention()

        if OrderType.COMMENT_LIKE == self.orders_type:
            return self.comment_like()

        if OrderType.PLAY == self.orders_type:
            return self.paly_number()

        if OrderType.COMMENT_PRAISE == self.orders_type:
            return self.comment_praise()

        return {'status': Status.FAILED, 'msg': '数据类型错误'}
