from django.contrib import admin

from .models import (
    AnswerKey,
    AnswerKeyItem,
    Exam,
    Question,
    Submission,
    SubmissionEvaluation,
    SubmissionItem,
    Topic,
)

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(AnswerKey)
admin.site.register(AnswerKeyItem)
admin.site.register(Submission)
admin.site.register(SubmissionEvaluation)
admin.site.register(SubmissionItem)
admin.site.register(Topic)
