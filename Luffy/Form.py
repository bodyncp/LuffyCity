# _*_ coding:utf-8 _*_
# __author__Zj__
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from Luffy.models import Module
from Luffy.models import Types
from Luffy.models import Team


class UserFrom(forms.Form):
    m_choices = Module.objects.all().values_list("nid", "module")
    t_choices = Team.objects.all().values_list("nid", "team_name")
    user = forms.CharField(max_length=32, label="用户名",
                           error_messages={"required": "用户名不能为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control"})
                           )

    invite_code = forms.IntegerField(label="邀请码",
                                     error_messages={"required": "邀请码不能为空", "invalid": "邀请码格式不正确"},
                                     widget=widgets.TextInput(attrs={"class": "form-control"})
                                     )

    gender = forms.ChoiceField(label="性别", choices=((0, "女"), (1, "男")), initial=1,
                               widget=widgets.Select(attrs={"class": "form-control"})

                               )
    pwd = forms.CharField(max_length=16, label="密码",
                          error_messages={"required": "密码不能为空"},
                          widget=widgets.PasswordInput(attrs={"class": "form-control"})
                          )

    re_pwd = forms.CharField(max_length=32, label="确认密码",
                             error_messages={"required": "确认密码不能为空"},
                             widget=widgets.PasswordInput(attrs={"class": "form-control"})
                             )

    # addr = forms.CharField(max_length=32, label="地址", error_messages={"required": "地址不能为空"},
    #                        widget=widgets.TextInput(attrs={"class": "form-control"}))
    #
    email = forms.EmailField(label='电子邮箱', error_messages={"required": "电子邮箱不能为空", "invalid": "电子邮箱格式不正确"},
                             widget=widgets.EmailInput(attrs={"class": "form-control"}))

    # url = forms.URLField(max_length=64, label="博客地址", widget=widgets.URLInput(attrs={"class": "form-control"}))

    modules_id = forms.ChoiceField(label="所属模块", choices=m_choices, initial=1,
                                widget=widgets.Select(attrs={"class": "form-control"}))

    teams_id = forms.ChoiceField(label="所属QQ组", choices=t_choices, initial=1,
                              widget=widgets.Select(attrs={"class": "form-control"}))

    def clean_user(self):
        from Luffy.models import UserInfo
        user = self.cleaned_data.get("user")
        flag = UserInfo.objects.filter(username=user).first()
        if not flag:
            return user
        else:
            raise ValidationError("该用户已被注册")

    def clean_invite_code(self):

        if self.cleaned_data.get("invite_code") == 1234:

            return True

        else:
            raise ValidationError("邀请码错误！")

    def clean(self):

        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.pop("re_pwd")
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致！")
        return self.cleaned_data


class SummaryForm(forms.Form):
    ty_choice = Types.objects.all().values_list("nid", "classify")
    abstract = forms.CharField(max_length=64, label="内容摘要", error_messages={"required": "摘要不能为空"},
                               widget=widgets.TextInput(attrs={"class": "form-control"}))

    today_content = forms.CharField(label="今日内容总结", error_messages={"required": "不能为空"},
                                    widget=widgets.Textarea(attrs={"class": "form-control", "rows": "7"}))

    tomorrow_content = forms.CharField(label="明日计划任务", error_messages={"required": "不能为空"},
                                       widget=widgets.Textarea(attrs={"class": "form-control", "rows": "7"}))

    code = forms.IntegerField(label="今日代码量", error_messages={"required": "代码量不能为空", "invalid": "数字格式"},
                              widget=widgets.TextInput(attrs={"class": "form-control"}))

    complete = forms.ChoiceField(label="今日任务是否完成", choices=((0, "未完成"), (1, "完成")), initial=0,
                                 widget=widgets.Select(attrs={"class": "form-control"}))

    types_id = forms.ChoiceField(label="所属类型", choices=ty_choice, initial=1,
                                 widget=widgets.Select(attrs={"class": "form-control"}))












