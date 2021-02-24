from requests_html import HTML, HTMLSession

from gate_analytics.analytics.models import (
    QuestionType,
    Submission,
    SubmissionItemStatus,
)
from gate_analytics.utils.itertools import make_batch
from gate_analytics.utils.text import deduplicate_slashes


def parse(url: str) -> Submission:
    url = deduplicate_slashes(url)
    html: HTML = HTMLSession().get(url).html
    for question_pnl in html.find(".questionPnlTbl"):
        for img in question_pnl.find(".questionRowTbl img"):
            src = deduplicate_slashes(img.attrs["src"])
            print(src)
        metas = make_batch(question_pnl.find(".menu-tbl td"), size=2)
        assert metas[0][0].full_text == "Question Type :"
        question_type = QuestionType.from_text(metas[0][1].full_text)
        assert metas[1][0].full_text == "Question ID :"
        question_uid = metas[1][1].full_text.strip()
        assert metas[2][0].full_text == "Status :"
        status = SubmissionItemStatus.from_text(metas[2][1].full_text)
        answer = ""
        if status == SubmissionItemStatus.Answered and question_type in [
            QuestionType.MCQ,
            QuestionType.MSQ,
        ]:
            assert metas[3][0].full_text == "Chosen Option :"
            answer = metas[3][1].full_text.strip()
        elif (
            status == SubmissionItemStatus.Answered
            and question_type == QuestionType.NAT
        ):
            prompt, value = question_pnl.find(".questionRowTbl td")[-2:]
            assert prompt.full_text == "Given Answer :"
            answer = value.full_text.strip()
        print(question_type.name, question_uid, status.name, answer)
        print("-" * 40)
    raise NotImplementedError()
