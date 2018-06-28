# _*_ coding:utf-8 _*_
# __author__Zj__

from django.template import Library
from Luffy.Util import get_no_summary_user
from Luffy import models
register = Library()


def user_no_summary():


    pass
    # # 可以分模块查询出没总结的同学
    # yesterday, today, code_res = get_no_summary_user()
    #
    # code_res.sort(key=lambda x: x[1][1])
    # code_res = code_res[:3]  # 获取后三名
    # # 获取 全部总结  需要分组查询
    # summary = models.Summary.objects.filter(create_time=yesterday).order_by("-code")
    # # 取前四名 展示
    # summary1 = summary[0:4]
