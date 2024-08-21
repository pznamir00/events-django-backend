from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta
from celery import shared_task
from django.db.models import Count
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from applications.users.models import User
from .models import Event


@shared_task
def send_emails(**kwargs):
    """
    This function is the cron system for automatically sending
    emails in users every day with new events that may interest them.
    It triggers on 1 time every day and looks for events that were
    added in last 24 hours.
    After retrieve a list of this events looks for a matches with
    followed hashtags based on relations of their with user.
    Result is a list of events that is submitting to user as email message.
    """
    # get datetime exactly 24 hours before
    yesterday = datetime.today() - timedelta(days=1)
    # get events that was created in last 24 hours
    recent_events = Event.objects.filter(created_at__gte=yesterday)
    # get users with any hashtags
    users = (
        User.objects.annotate(hashtags_num=Count("followed_hashtags"))
        .filter(hashtags_num__qt=0)
        .prefetch_related("followed_hashtags")
    )

    for user in users:
        events = list(
            filter(
                lambda e: True
                in [
                    f"#{hashtag}" in e.description
                    for hashtag in user.followed_hashtags  # pylint: disable=cell-var-from-loop # type: ignore
                ],
                recent_events,
            )
        )
        if events:
            subject = "We found few new events for you"
            html_message = render_to_string(
                "emails/new_events_msg.html", {"events": events}
            )
            plain_message = strip_tags(html_message)
            from_email = "From <events@gamil.com>"
            to = user.email
            mail.send_mail(
                subject, plain_message, from_email, [to], html_message=html_message
            )
