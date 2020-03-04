"""
    文档说明视图
"""

from flask import views, render_template


class Explain(views.MethodView):

    def get(self):
        """
        文档说明
        :return:渲染文档页面
        """
        return render_template('explain.html')


class ApiDocument(views.MethodView):

    def get(self):
        """
        api文档说明
        :return:渲染api文档页面
        """
        return render_template('api_ document.html')
