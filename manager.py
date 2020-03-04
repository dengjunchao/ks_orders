"""
    主程序入口
    MANAGER.add_url_rule 视图路由
    debug_logs：日志 需要传入警告级别
"""
import logging
from flask import Flask, jsonify, request
from ky_omm.view.index import Index
from ky_omm.view.explain import Explain, ApiDocument
from libs.debug_logs import debug_logs
from flask_restful import Api
from libs.add_orders import AddOrders
from libs.query_orders import QueryOrders
from libs.back_order import BackOrders


manager = Flask(__name__)
api = Api(manager)

manager.add_url_rule("/", view_func=Index.as_view(name="index"))
manager.add_url_rule("/explain", view_func=Explain.as_view(name="explain"))
manager.add_url_rule("/api_document", view_func=ApiDocument.as_view(name="api_document"))

api.add_resource(AddOrders, '/add_order')
api.add_resource(QueryOrders, '/query_order')
api.add_resource(BackOrders, '/back_order')

# debug_logs(logging.ERROR)

if __name__ == '__main__':
    manager.run(host='0.0.0.0', port=5000)
