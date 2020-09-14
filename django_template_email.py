# Use the standard Django emailing + templating
# by putting email templates in "email/{template}.html"
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils.html import strip_tags


class TemplateEmail:
    def __init__(self, to, subject, template, context={}, **kwargs):
        self.to = to
        self.subject = subject
        self.template = template
        self.context = context

        self.from_name = kwargs.pop("from_name", settings.DEFAULT_FROM_NAME)
        self.from_email = kwargs.pop("from_email", settings.DEFAULT_FROM_EMAIL)
        self.reply_to = kwargs.pop("reply_to", settings.DEFAULT_REPLY_TO_EMAIL)

        # expected to be lists
        self.to = self.to if not isinstance(self.to, str) else [self.to]
        self.reply_to = (
            self.reply_to if not isinstance(self.reply_to, str) else [self.reply_to]
        )

        self.rendered_html_content = render_to_string(
            f"email/{self.template}.html", self.context
        )
        try:
            self.rendered_plain_text_content = render_to_string(
                f"email/{self.template}.txt", self.context
            )
        except TemplateDoesNotExist:
            self.rendered_plain_text_content = strip_tags(self.rendered_html_content)

        self.email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.rendered_plain_text_content,
            from_email=f"{self.from_name} <{self.from_email}>",
            to=self.to,
            reply_to=[self.reply_to],
            **kwargs,
        )
        self.email.attach_alternative(self.rendered_html_content, "text/html")

    def send(self):
        # catch errors
        self.email.send()
