from django.db import models
from django.urls import reverse
from user.models import User

KIND_CHOICES = [
    ('Annual', '연차'),
    ('Monthly', '월차'),
    ('morning_Half', '반차 (오전)'),
    ('afternoon_Half', '반차 (오후)'),
    ('official', '공가 및 특별휴가'),
    ('carry_over', '이월 (1일)'),
    ('carry_over_Half', '이월 (0.5일)'),
]
KIND_CHOICES_INV = {val: val for val, _ in KIND_CHOICES}

class Patient(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @property
    def get_html_url(self):
        url = reverse('leave:patient_edit', args=(self.id,))
        return f'<div class="event-title" data-toggle="tooltip" title="Memo: {self.memo}"><a href="{url}" style="color:black;"> {self.title} </a></div>'

    def __str__(self):
        return f'{self.title} | {self.user.first_name}'


class Leave(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    kind = models.CharField(choices=KIND_CHOICES, max_length=20, blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)  # 휴가 사용자
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leave_created_by') # 누가 등록했는지

    @staticmethod
    def field_value_and_text():
        ret = {'kind': KIND_CHOICES}
        return ret

    def __str__(self):
        return f'{self.name} | {self.from_date} | {self.kind}'
