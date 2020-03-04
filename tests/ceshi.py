from pymongo import MongoClient

# TIKTOK_HOST = MongoClient('mongodb://root:kyyfzx2019@192.168.100.2:27017/').douyin_server.orders_test
#
# TIKTOK_HOST_ORDER = MongoClient('mongodb://root:kyyfzx2019@192.168.100.2:27017/').douyin_server.orders

# res1 = TIKTOK_HOST.find()
#
#
# # print(res1.count())
# for i in res1:
#
#     TIKTOK_HOST_ORDER.insert({
#         'order_type': int(i['order_type']),
#         'item_id': i["item_id"],
#         'order_date': i["order_date"],
#         'start_num': i["start_num"],
#         'now_num': i["now_num"],
#         'order_state': i["order_state"],
#         'counts': i["counts"],
#         'work_status': i["work_status"],
#         "sign": i["sign"],
#         "robots_num": i["robots_num"],
#         "order_count": i["order_count"]
#     })

# JISU_DEVICE_RIGISTER = MongoClient('mongodb://root:kyyfzx2019@192.168.100.2:27017/').aweme_server.jisu_device_register


# print(TIKTOK_HOST.find().count())

# openudid = ""
# for i in range(10):
#     for item in TIKTOK_HOST.aggregate([{'$sample': {'size': 1}}]):
#         if item["ttreq"]:
#             openudid = item["openudid"]
#             break


# a = 0
# b = 0
#
#
# if not a or not b:
#     print(11)
#
