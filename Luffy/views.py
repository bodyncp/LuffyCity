import uuid
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from Luffy import models
from django.contrib.auth.decorators import login_required
from Luffy.Form import UserFrom, SummaryForm
from Luffy.Util import get_all_code, get_img, not_in_date
from Luffy.Util import date_range, get_no_summary_user, get_month_data


@login_required
def index(request):
    yesterday, today, code_res = get_no_summary_user()  # 可以分模块查询出没总结的同学
    code_res.sort(key=lambda x: x[1][1])
    code_res = code_res[:3]  # 获取后三名
    res = date_range()
    # res = 1
    user = [request.user.username, ]
    try:
        user_all_code = get_all_code(user)[0][1][1]  # 当前用户的代码量
    except Exception as e:
        user_all_code = 0
    code = request.session.get("count")

    # yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    # 可做分页展示
    # 获取 全部总结  需要分模块查询
    summary = models.Summary.objects.filter(create_time=yesterday).order_by("-code")
    # 取前四名 展示
    summary1 = summary[0:4]

    try:
        # 查询出 最后代码量少的三位同学
        last_three_man_name = [user.user.username for user in summary.reverse()[:3]]
    except Exception as e:
        last_three_man_name = [user.user.username for user in summary.reverse()]
    # 获取了他们的代码总量
    last_man_list = get_all_code(last_three_man_name)
    return render(request, "index.html", locals())


def register(request):
    if request.is_ajax():
        form = UserFrom(request.POST)
        response = {"status": True, "msg": None, "user": None}
        form = UserFrom(request.POST)
        if form.is_valid():
            response["user"] = user = form.cleaned_data.pop("user")
            pwd = form.cleaned_data.pop("pwd")
            form.cleaned_data.pop("invite_code")
            extra_fields = form.cleaned_data
            head_img_obj = request.FILES.get("file")
            if head_img_obj:
                head_img_obj.name = str(uuid.uuid4()) + ".png"
                extra_fields["head_image"] = head_img_obj
            models.UserInfo.objects.create_user(username=user, password=pwd, **extra_fields)
        else:
            msg = form.errors
            response["status"] = False
            response["msg"] = form.errors
        return JsonResponse(response)
    form = UserFrom()
    return render(request, "register.html", locals())


@login_required
def getdata(request):
    response = {}
    username_obj = models.UserInfo.objects.all()
    username_list = [username.username for username in username_obj]
    data = get_all_code(username_list, chart=True)
    data.sort(key=lambda x: x[1])
    response["data"] = data[-5:]
    return JsonResponse(response)


def login(request):
    if request.method == "POST":
        response = {}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        imgcode = request.POST.get("imgcode")
        right_code = request.session.get("code")
        if imgcode.upper() == right_code.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                response["status"] = True
            else:
                response["status"] = False
                response["codeError"] = "用户名或密码错误！"
            return JsonResponse(response)
        else:
            response["status"] = False
            response["codeError"] = "验证码输入错误，刷新后重试"
            return JsonResponse(response)
    return render(request, 'login.html')


def get_code(request):
    codeStr, data = get_img()
    request.session["code"] = codeStr
    return HttpResponse(data)


@login_required
def summary(request):
    form = SummaryForm()
    if request.method == "POST":
        form = SummaryForm(request.POST)
        if form.is_valid():
            summary_dict = form.cleaned_data
            summary_dict["user_id"] = request.user.nid
            today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            summary_obj = models.Summary.objects.filter(user_id=request.user.nid, create_time=today).first()
            if summary_obj:
                summary_dict.pop("code")
                models.Summary.objects.filter(user_id=request.user.nid, create_time=today).update(**summary_dict)
            else:
                models.Summary.objects.create(**summary_dict)
            request.session['count'] = 1
            return redirect("/index/")
        else:
            render(request, "summary.html", locals())
    return render(request, "summary.html", locals())


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/login/")


@login_required
def detail(request):
    """

    :param request:
    :return:
    """
    # get请求获取username 接着就是发ajax 请求
    user = request.GET.get("user")
    if request.is_ajax():
        response = {"sevenDate": None, "codeCount": None, "monthCode": None}
        date_format = "%Y-%m-%d"
        # user = request.user.username
        current_time = datetime.datetime.now().strftime(date_format)
        seven_ago_time = (datetime.datetime.now() - datetime.timedelta(days=6)).strftime(date_format)
        code = models.Summary.objects.filter(user__username=user,
                                             create_time__range=(seven_ago_time, current_time)).values_list("code",
                                                                                                            "create_time")
        # 把代码 与 日期 组成 元祖
        code = [(i[0], str(i[1].strftime(date_format))) for i in code]
        # 查询出来七天中存在的天数
        exist_data_list = [i[1] for i in code]
        date_seven_list = []
        for i in range(7):
            date_seven_list.append((datetime.datetime.now() - datetime.timedelta(days=i)).strftime(date_format))
        # 今天到后七天的时间全部的
        date_seven_list.reverse()
        ext_list = not_in_date(date_seven_list, exist_data_list)
        code.extend(ext_list)
        code.sort(key=lambda x: x[1])
        code_all = [i[0] for i in code]
        response["sevenDate"] = date_seven_list
        response["codeCount"] = code_all
        month_code_list = get_month_data(user)
        response["monthCode"] = month_code_list
        return JsonResponse(response)

    seven_days_summary = models.Summary.objects.filter(user__username=user).order_by("-create_time")[:7]

    return render(request, "detail.html", locals())
