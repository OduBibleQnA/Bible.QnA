from django.contrib import admin
from .models import Question, Testimony

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'question', 'answered', 'answer_medium', 'answer_date', 'archived')
    list_filter = ('answer_medium', 'answer_date', 'archived')
    search_fields = ('name', 'question')

@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ('name', 'approved', 'archived')
    list_filter = ('approved', 'archived')
    search_fields = ('name', 'shortened_testimony')
