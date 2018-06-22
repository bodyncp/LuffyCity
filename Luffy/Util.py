# _*_ coding:utf-8 _*_
# __author__Zj__


import random
from PIL import Image
from io import BytesIO
from PIL import ImageDraw
from PIL import ImageFont
from Luffy import models
import datetime


def get_all_code(name_list, chart=False):
    # 查询出来出进来的这些人的总共的代码量
    man_all_code = models.Summary.objects.filter(user__username__in=name_list).values("user__username", "code")
    man_all_code_dict = {}

    for name in man_all_code:
        man_all_code_dict[name.get("user__username")] = 0
    for name2 in man_all_code:
        man_all_code_dict[name2.get("user__username")] += name2.get("code")

    man_all_code_list = []
    for item in enumerate(man_all_code_dict.items()):
        man_all_code_list.append(item)  # (1, ('jack', 30))
    if chart:
        ajax_list = []
        for i in man_all_code_list:
            ajax_list.append(list(i[1]))
        return ajax_list
    else:
        return man_all_code_list


def get3random(simple=False):
    if simple:
        return random.randint(0, 50), random.randint(0, 100), random.randint(0, 100)
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def get_img():
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
    now_date = int(datetime.datetime.now().strftime("%H%M"))

    datarange = range(2200, 2300)

    res = 1 if now_date in datarange else 0

    return res


def get_no_summary_user():
    yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))

    all_user = models.UserInfo.objects.all().filter(status=1).values_list("username")

    user_set = set([user[0] for user in all_user])

    today_user = models.Summary.objects.all().filter(create_time=yesterday).values_list("user__username")
    today_user_set = set([user[0] for user in today_user])

    no_summary_user_list = list(user_set - today_user_set)


    code_res = get_all_code(no_summary_user_list)






    return yesterday, today, code_res
