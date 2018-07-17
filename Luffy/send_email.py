#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 20:00
# @Author  : NCP
# @File    : send_email.py
# @Software: PyCharm

import os


def send(code, rec_user):
    os.system('您的验证码是：%s | mail -v -r "zjcode@aliyun.com" -s "Luffycity修改密码专属快递" %s' % (code, rec_user))