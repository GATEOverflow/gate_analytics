from requests_html import HTML

from gate_analytics.analytics.models import Submission


def parse(html_content: str) -> Submission:
    html = HTML(html=html_content)
    question_panels = html.find(".question-pnl")
    print(len(question_panels))
    raise NotImplementedError()
