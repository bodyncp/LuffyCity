from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)

    phone = models.CharField(verbose_name="学员电话", max_length=11, null=True)

    signature = models.CharField(verbose_name="签名", max_length=32, default="如果你有理想的话,就努力去实现")

    gender = models.IntegerField(verbose_name="用户性别", choices=[(1, "男"), (2, "女")], default=1)

    addr = models.CharField(verbose_name="用户地址", max_length=16, null=True)

    head_image = models.FileField(verbose_name="用户头像", upload_to="Head/", default="Head/default.png")

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    url = models.URLField(verbose_name="博客地址", null=True)

    modules = models.ForeignKey(verbose_name="所属模块", to="Module", to_field="nid", on_delete=models.DO_NOTHING,
                                null=True)
    teams = models.ForeignKey(verbose_name="所属小组", to="Team", to_field="nid", on_delete=models.DO_NOTHING, null=True)

    status = models.BooleanField(default=1)

    def __str__(self):
        return self.username


class Summary(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="所属学员", to="UserInfo", to_field="nid", on_delete=models.DO_NOTHING, null=True)
    abstract = models.CharField(verbose_name="总结摘要", max_length=64, null=True)
    today_content = models.TextField(verbose_name="今天内容", default=1)
    tomorrow_content = models.TextField(verbose_name="明天计划", default=1)
    code = models.IntegerField(verbose_name="代码量", default=1)
    create_time = models.DateField(verbose_name="创建时间", auto_now_add=True)
    types = models.ForeignKey(verbose_name="总结类型", to="Types", to_field="nid", on_delete=models.DO_NOTHING, null=True)
    complete = models.BooleanField(verbose_name="是否完成任务", choices=((0, "no"), (1, "yes")), default=0)

    def __str__(self):
        return self.abstract


class Types(models.Model):
    nid = models.AutoField(primary_key=True)

    classify = models.CharField(verbose_name="总结分类", max_length=12, )

    # ext = models.CharField(verbose_name="扩展字段", max_length=32, null=True)

    def __str__(self):
        return self.classify


class Module(models.Model):
    nid = models.AutoField(primary_key=True)

    module = models.CharField(verbose_name="模块名称", max_length=32)

    # ext = models.CharField(verbose_name="扩展字段", max_length=32, null=True)

    def __str__(self):
        return self.module


class Team(models.Model):
    nid = models.AutoField(primary_key=True)

    team_name = models.CharField(max_length=16, verbose_name="小组名称")

    def __str__(self):
        return self.team_name


class Share(models.Model):
    nid = models.AutoField(primary_key=True)

    desc = models.CharField(verbose_name="分享描述", max_length=64)

    content = models.TextField(verbose_name="分享内容")

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    user = models.ForeignKey(verbose_name="所属学员", to="UserInfo", to_field="nid", on_delete=models.DO_NOTHING)

    commentCount = models.IntegerField(verbose_name="评论数")

    def __str__(self):
        return self.desc


class UrlShare(models.Model):
    nid = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    title = models.CharField(verbose_name="博客概要", max_length=20, default="xx")
    desc = models.TextField(verbose_name="博客知识点概要")
    url = models.URLField(verbose_name="分享博客地址")
    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.DO_NOTHING)
    isFavor = models.IntegerField(verbose_name="点赞数")


class Favor(models.Model):
    nid = models.AutoField(primary_key=True)

    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.DO_NOTHING)

    isUp = models.BooleanField(verbose_name="点赞")

    url = models.ForeignKey(to="UrlShare", to_field="nid", on_delete=models.DO_NOTHING)


class Comment(models.Model):
    nid = models.AutoField(primary_key=True)

    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    comment = models.TextField(verbose_name="评论内容")

    share = models.ForeignKey(to="Share", to_field="nid", on_delete=models.DO_NOTHING)

    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.DO_NOTHING)
