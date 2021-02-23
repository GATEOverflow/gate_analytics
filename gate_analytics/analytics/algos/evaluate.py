from gate_analytics.analytics.models import AnswerKey, Submission, SubmissionEvaluation


def evaluate(submission: Submission, key: AnswerKey) -> SubmissionEvaluation:
    raise NotImplementedError()
