"""
    配置文件
    Config ：    路径配置
    OrderType：  订单配置
    Status：     状态配置
"""
import os
from pymongo import MongoClient

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    CURREN_PATH   当前路径
    BASE_PATH     根路径
    UPLOAD_PATH   上传路径
    TikTok_HOST   链接mongodb快手数据库
    """

    CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
    BASE_PATH = CURRENT_PATH[:CURRENT_PATH.find("Ky_omm\\") + len("Ky_omm\\")]
    UPLOAD_PATH = os.path.join(os.path.join(BASE_PATH, 'static'), 'upload')
    # TIKTOK_HOST = MongoClient('mongodb://root:kyyfzx2019@192.168.100.2:27017/').douyin_server.orders_test
    # JISU_DEVICE_RIGISTER = MongoClient('mongodb://root:kyyfzx2019@192.168.100.2:27017/').aweme_server.jisu_device_register
    KS_HOST = MongoClient('mongodb://192.168.100.2:27016/').aweme_server.ks_orders


class OrderType(object):
    """
    LIKE             点赞
    ATTENTION        关注
    COMMENT_LIKE    评论点赞
    PLAY            播放
    ORDER_ID        订单id长度
    VIDEO_ID        视频id长度
    """
    LIKE = 1
    ATTENTION = 2
    COMMENT_LIKE = 3
    PLAY = 4
    COMMENT_PRAISE = 5
    ORDER_ID_LEN = 24
    VIDEO_ID_LEN = 19


class Status(object):
    """
    SUCCEED 成功
    FAILED  失败
    """
    SUCCEED = 200
    FAILED = 404
    RETIRED_SINGLE = 2
