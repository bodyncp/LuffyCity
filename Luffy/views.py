import uuid
import datetime
import os
from PIL import Image
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from LuffyCity.settings import BASE_DIR
from Luffy import models
from django.contrib.auth.decorators import login_required
from Luffy.Form import UserFrom, SummaryForm, EditForm, EidtMoTeam
from Luffy.Util import get_all_code, get_img, not_in_date
from Luffy.Util import date_range, get_no_summary_user, get_month_data


@login_required
def index(request, **kwargs):
    user_obj = request.user
    if kwargs:
        module_id = kwargs.pop("module")
        module = models.Module.objects.filter(nid=module_id).first()
    else:
        module = user_obj.modules
    yesterday, today, code_res = get_no_summary_user(module=module)  # 可以分组块查询出没总结的同学
    res = date_range()
    # res = 1
    user = [user_obj.username, ]
    try:
        user_all_code = get_all_code(user)[0].get("all_code")
        # 当前用户的代码量
    except Exception as e:
        print("Exception-index-->", e)
        user_all_code = 0
    code = request.session.get("count")
    # 可做分页展示
    # 获取 全部总结  需要分组查询
    summary = models.Summary.objects.filter(create_time=yesterday, user__modules=module).order_by("-code")
    # 取前四名 展示
    current_page_num = request.GET.get("page", default=1)
    current_page_num = int(current_page_num)
    paginator = Paginator(summary, 3)
    try:
        first_4_summary = paginator.page(current_page_num)
    except EmptyPage as e:
        current_page_num = 1
        first_4_summary = paginator.page(current_page_num)
    page_range = paginator.page_range

    # 查询出 最后代码量少的三位同学
    last_three_man_name = [user.user.username for user in summary.reverse()[:2]]  # 获取后两名

    # 获取了他们的代码总量
    last_man_list = get_all_code(last_three_man_name)
    modules = models.Module.objects.all()
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
    """

    :param request:
    :return:
    """
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
    res = date_range()
    if not res:
        return redirect("/index")
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


@login_required
def editinfo(request):
    """
    :param request:
    :return:
    """
    if request.is_ajax():
        response = {"status": True, "msg": None, "user": None}
        form = EditForm(request.POST)
        if form.is_valid():
            nid = request.user.nid
            username = form.cleaned_data.get("username")
            extra_fields = form.cleaned_data
            head_img_obj = request.FILES.get("file")
            if head_img_obj:
                print("head_img_obj", head_img_obj)
                file_path = os.path.join(BASE_DIR, "Head")
                head_img_obj.name = str(uuid.uuid4()) + ".png"
                extra_fields["head_image"] = "Head/" + head_img_obj.name
                img = Image.open(head_img_obj)
                img.save(os.path.join(file_path, head_img_obj.name))

            models.UserInfo.objects.filter(nid=nid).update(**extra_fields)
        else:
            response["status"] = False
            response["msg"] = form.errors
        return JsonResponse(response)
    form = EditForm(initial={"modules": request.user.modules, "teams": request.user.teams})
    return render(request, "editInfo.html", locals())


def editmoteam(request):
    """
    修改用户的模块信息 后期 分组以及模块展示用
    :param request:
    :return:
    """
    user = request.GET.get("user")
    username = request.user.username
    if user == username:
        if request.method == "GET":
            user_obj = models.UserInfo.objects.filter(username=username).first()
            form = EidtMoTeam(initial={"modules": user_obj.modules, "teams": user_obj.teams})
            return render(request, "editmoteam.html", locals())
        else:
            form = EidtMoTeam(request.POST)
            if form.is_valid():
                extra_fields = form.cleaned_data
                models.UserInfo.objects.filter(username=username).update(**extra_fields)
            return redirect("/index/")
    else:
        return redirect("/login/")


def page_error(request):


    """
    :param request:
    :return:
    :function: 错误重定向
    """
    return render(request, '404.html')
