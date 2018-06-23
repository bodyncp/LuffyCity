import uuid
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from Luffy.Form import UserFrom, SummaryForm
from Luffy import models
from Luffy.Util import get_all_code, get_img, date_range, get_no_summary_user


@login_required
def index(request):
    yesterday, today, code_res = get_no_summary_user()
    code_res.sort(key=lambda x: x[1][1])
    code_res = code_res[:3]
    res = date_range()
    # res = 1
    user = [request.user.username, ]
    try:
        user_all_code = get_all_code(user)[0][1][1]
    except Exception as e:
        user_all_code = 0
    code = request.session.get("count")
    yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    summary = models.Summary.objects.filter(create_time=yesterday).order_by("-code")
    summary1 = summary[0:4]
    try:
        last_three_man_name = [user.user.username for user in summary.reverse()[:3]]
    except Exception as e:
        last_three_man_name = [user.user.username for user in summary.reverse()]
    last_man_list = get_all_code(last_three_man_name)
    return render(request, "index.html", locals())


def register(request):
    if request.is_ajax():
        form = UserFrom(request.POST)
        response = {"status": True, "msg": None, "user": None}
        form = UserFrom(request.POST)
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            # addr = form.cleaned_data.get("addr")
            # phone = form.cleaned_data.get("phone")
            email = form.cleaned_data.get("email")
            # url = form.cleaned_data.get("url")
            models_id = form.cleaned_data.get("modules")
            teams_id = form.cleaned_data.get("teams")
            gender = form.cleaned_data.get("gender")
            head_img_obj = request.FILES.get("file")
            extra_fields = {}
            if head_img_obj:
                head_img_obj.name = str(uuid.uuid4()) + ".png"
                extra_fields["head_image"] = head_img_obj
            models.UserInfo.objects.create_user(username=user, password=pwd, email=email, modules_id=models_id,
                                                teams_id=teams_id, gender=gender, **extra_fields)
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
    response["data"] = data[:5]
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
