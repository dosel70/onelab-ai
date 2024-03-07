from django.db import models
from oneLabProject.models import Period


class Member(Period):
    member_email = models.CharField(blank=False, null=False, max_length=50)
    # 학교 이메일
    member_school_email = models.CharField(blank=False, null=False, max_length=50, default="<EMAIL>")
    member_password = models.CharField(blank=False, null=False, max_length=20)
    member_name = models.CharField(blank=False, null=False, max_length=100)
    member_phone = models.CharField(null=False, blank=False, max_length=100)
    # 일반 회원: True, 관리자: False
    member_status = models.BooleanField(null=False, default=True)
    member_type = models.TextField(blank=False, default="oneLabProject")

    class Meta:
        db_table = 'tbl_member'
