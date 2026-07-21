import csv
import io
from django.http import HttpResponse
from django.contrib import admin
from .models import Blog, Feedback


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    readonly_fields = ['name', 'category', 'subject', 'content', 'rating', 'created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'category', 'priority', 'rating', 'is_read', 'is_resolved', 'created_at']
    list_filter = ['category', 'priority', 'is_read', 'is_resolved', 'created_at']
    search_fields = ['subject', 'content', 'name']
    readonly_fields = ['name', 'contact', 'category', 'priority', 'subject', 'content', 'rating', 'created_at', 'updated_at']
    actions = ['export_to_csv', 'mark_as_read', 'mark_as_resolved']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "标记为已读"

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = "标记为已解决"

    def export_to_csv(self, request, queryset):
        """导出反馈为CSV文件"""
        output = io.StringIO()
        writer = csv.writer(output)
        # 写入表头
        writer.writerow(['ID', '姓名', '联系方式', '反馈类型', '优先级', '标题', '详细内容', '评分', '是否已读', '是否已解决', '提交时间'])
        # 写入数据
        for feedback in queryset:
            writer.writerow([
                feedback.id,
                feedback.name,
                feedback.contact,
                feedback.get_category_display(),
                feedback.get_priority_display(),
                feedback.subject,
                feedback.content,
                feedback.rating,
                '是' if feedback.is_read else '否',
                '是' if feedback.is_resolved else '否',
                feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        # 创建响应
        response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename=feedbacks_' + Feedback.objects.first().created_at.strftime('%Y%m%d') if Feedback.objects.exists() else 'feedbacks.csv'
        response['Content-Disposition'] = 'attachment; filename=feedbacks_' + Feedback.objects.latest('created_at').created_at.strftime('%Y%m%d%H%M%S') if Feedback.objects.exists() else 'feedbacks.csv'
        return response
    export_to_csv.short_description = "导出选中反馈为CSV"
