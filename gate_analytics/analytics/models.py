from django.db import models


class Exam(models.Model):
    branch = models.CharField(max_length=2)
    year = models.DateField()
    set = models.IntegerField()
    branch_full_name = models.CharField(max_length=255)

    conducting_authority = models.TextField(blank=True)
    number_of_applicants = models.IntegerField(blank=True, null=True)
    applicants_present = models.IntegerField(blank=True, null=True)

    recommended_answer_key = models.ForeignKey(
        "AnswerKey",
        related_name="recommended_for_exam",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = (("branch", "year", "set"),)

    def __str__(self):
        return f"{self.branch}-{self.year.year}-{self.set}"


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class QuestionType(models.IntegerChoices):
    MCQ = 0
    MSQ = 1
    NAT = 2


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    number = models.IntegerField()

    image = models.URLField()
    gateoverflow_link = models.URLField()
    type = models.IntegerField(choices=QuestionType.choices, db_index=True)
    answer_choices = models.JSONField()
    max_marks = models.FloatField()
    topics = models.ManyToManyField(Topic, blank=True, null=True)

    class Meta:
        unique_together = (("exam", "number"),)

    def __str__(self):
        return f"{self.exam}-{self.number}"


class AnswerKey(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    answers = models.ManyToManyField(
        Question, through="AnswerKeyItem", through_fields=("key", "question")
    )

    def evaluate_all_submissions(self) -> None:
        raise NotImplementedError()

    class Meta:
        unique_together = (("exam", "name"),)

    def __str__(self):
        return f"{self.exam}-{self.name}"


class AnswerKeyItem(models.Model):
    key = models.ForeignKey(AnswerKey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    correct_answer = models.TextField()
    marks_to_all = models.BooleanField(default=False)
    excluded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.key}-{self.question}"


class Submission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    candidate_id = models.CharField(max_length=255)
    candidate_name = models.CharField(max_length=255)
    test_center_name = models.CharField(max_length=255)
    test_date = models.DateField()
    test_time_start = models.DateTimeField()
    test_time_end = models.DateTimeField()
    submission_url = models.URLField(unique=True, db_index=True)

    items = models.ManyToManyField(
        Question, through="SubmissionItem", through_fields=("submission", "question")
    )
    evaluations = models.ManyToManyField(
        AnswerKey, through="SubmissionEvaluation", through_fields=("submission", "key")
    )

    def reevaluate(self) -> None:
        raise NotImplementedError()

    class Meta:
        unique_together = (("exam", "candidate_id"),)

    def __str__(self):
        return f"{self.exam}-{self.candidate_id}"


class SubmissionEvaluation(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    key = models.ForeignKey(AnswerKey, on_delete=models.CASCADE)
    attempted = models.IntegerField()
    positive_marks = models.FloatField()
    negative_marks = models.FloatField()
    net_marks = models.FloatField()

    def __str__(self):
        return f"{self.submission}-{self.key}-{self.net_marks:.2f}"


class SubmissionItem(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"{self.submission}-{self.question}-{self.answer}"
