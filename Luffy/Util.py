# _*_ coding:utf-8 _*_
# __author__Zj__

from django.db.models import Sum
import random
from PIL import Image
from io import BytesIO
from PIL import ImageDraw
from PIL import ImageFont
from Luffy import models
import datetime


def get_all_code(name_list: list, chart=False):
    """
    查询出来列表里的人的代码总量的总共的代码量
    :param name_list: username list
    :param chart: ajax or not
    :return:
    """
    if not isinstance(name_list, list):
        raise TypeError("must list")

    man_all_code_dict = models.Summary.objects.filter(user__username__in=name_list).values("user__username").annotate(
        all_code=Sum("code")).values("user__username", "all_code").order_by("-all_code")
    if chart:
        ajax_list = []
        for obj in man_all_code_dict:
            ajax_list.append([obj.get("user__username"), obj.get("all_code")])
        return ajax_list
    else:
        return man_all_code_dict


def get3random(simple=False):
    if simple:
        return random.randint(0, 50), random.randint(0, 100), random.randint(0, 100)
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_img():
    """
    获取验证码图片
    :return:
    """
    new_img = Image.new("RGB", size=(270, 32), color=(get3random()))
    draw = ImageDraw.Draw(new_img)
    font_cate = ImageFont.truetype("static/font/font.otf", size=26)
    code_list = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_lowcase = chr(random.randint(97, 122))
        random_upcase = chr(random.randint(65, 90))
        write_str = random.choice([random_num, random_lowcase, random_upcase])
        code_list.append(write_str)
        draw.text((i * 20 + 30, 2), write_str, fill=get3random(simple=True), font=font_cate)
    codeStr = "".join(code_list)
    by = BytesIO()  # 相当于内存句柄
    new_img.save(by, "png")
    data = by.getvalue()
    return codeStr, data


def date_range():
    """
    获取总结汇报时间
    :return:
    """
    now_date = int(datetime.datetime.now().strftime("%H%M"))

    datarange = range(2100, 2358)

    res = 1 if now_date in datarange else 0

    return res


def get_no_summary_user(module):  # 添加一个默认参数 后期分模块查询的时候使用
    """
    获取没有总结的用户对象 以及 他们的总代码量
    :param moudles:
    :return:
    """
    yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    # 当前全部的用户对象   #  当前用户小组的
    all_user = models.UserInfo.objects.filter(modules=module).filter(status=1).values_list("username")
    # 组成一个用户 集合
    user_set = set([user[0] for user in all_user])
    # 当天的有总结的用户对象
    today_user = models.Summary.objects.filter(user__modules=module).filter(create_time=yesterday).values_list(
        "user__username")
    # 当天有总结的用户集合
    today_user_set = set([user[0] for user in today_user])
    # 获取没有总结的人的列表
    no_summary_user_list = list(user_set - today_user_set)
    # 获取这些没有总结同学的总代码量
    code_res = get_all_code(no_summary_user_list)

    return yesterday, today, code_res


def not_in_date(much_list, small_list):
    """
    判断 是不是满足七天 不满足 就 添加代码量为 0
    :param much_list:
    :param small_list:
    :return:
    """

    ext_list = []
    for c in much_list:  # 全部的日期(多的那个)
        if c not in small_list:  # 少的那个
            ext_list.append((0, c))  # 生成一个不存在的列表
    return ext_list


def get_month_data(username, months=11):
    """
    获取每个人每个月的代码总量
    :param username:
    :param months:
    :return:
    """
    month_code_list = []
    if not isinstance(months, int):
        return month_code_list
    for i in range(5, months):
        count = 0
        res = models.Summary.objects.filter(user__username=username, create_time__month=i + 1).values_list("code")
        for r in res:
            count += r[0]
        month_code_list.append(count)

    return month_code_list
