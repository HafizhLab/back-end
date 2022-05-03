from django.contrib import admin

from hafizhlab.challenges.models import Challenge, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'mode', 'scope_type', 'scope_id', 'created_at', 'question_count')
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.question_set.count()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'ayah')
