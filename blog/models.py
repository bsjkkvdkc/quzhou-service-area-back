from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True, default='')
    content = models.TextField()
    category = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def summary_short(self):
        return self.summary[:100] if self.summary else self.content[:100]


class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('service', '服务质量'),
        ('facility', '设施设备'),
        ('food', '餐饮美食'),
        ('shopping', '商铺购物'),
        ('environment', '环境卫生'),
        ('other', '其他建议'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]
    
    name = models.CharField(max_length=100, blank=True, default='匿名用户', verbose_name='姓名')
    contact = models.CharField(max_length=200, blank=True, default='', verbose_name='联系方式')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name='反馈类型')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='优先级')
    subject = models.CharField(max_length=200, verbose_name='反馈标题')
    content = models.TextField(verbose_name='详细内容')
    rating = models.IntegerField(default=3, verbose_name='评分(1-5)')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_resolved = models.BooleanField(default=False, verbose_name='是否已解决')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '意见反馈'
        verbose_name_plural = '意见反馈'

    def __str__(self):
        return f"[{self.get_category_display()}] {self.subject}"

    @property
    def rating_stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)
