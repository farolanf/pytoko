from collections import Sequence
from django.conf import settings
from django.core.mail import send_mail as send
from django.template.loader import get_template

def send_mail(subject, template, recipients):

    if not isinstance(recipients, (list, tuple)):
        recipients = (recipients,)

    html = get_template(template).render(context={
        'subject': subject,
        'recipients': recipients
    })

    send(subject, '', settings.DEFAULT_FROM_EMAIL, recipients, html_message=html)