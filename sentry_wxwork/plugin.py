# coding: utf-8
import logging
from datetime import datetime, timedelta
from collections import defaultdict

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from sentry.plugins.bases import notify
from sentry.http import safe_urlopen
from sentry.utils import json
from sentry.utils.safe import safe_execute
from sentry.utils.forms import form_to_config
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry.exceptions import PluginError

from . import __version__, __doc__ as package_doc


# 配置
class WxworkNotificationsOptionsForm(notify.NotificationConfigurationForm):
    api_origin = forms.CharField(
        label=_('Request URL'),
        widget=forms.TextInput(attrs={'placeholder': 'http://192.168.120.242:7000/v1/msg/zwjPost'}),
        initial='http://192.168.120.242:7000/v1/msg/zwjPost'
    )
    api_type = forms.CharField(
        label=_('Request Type'),
        widget=forms.TextInput(attrs={'placeholder': 'POST | GET'}),
        initial='POST'
    )
    api_url = forms.CharField(
        label=_('Sentry URL'),
        widget=forms.TextInput(attrs={'placeholder': 'sentry web url for bugger'}),
        initial='http://192.168.120.140:9000/'
    )
    message_template = forms.CharField(
        label=_('Message template'),
        widget=forms.Textarea(attrs={'class': 'span4'}),
        help_text=_('Set in standard python\'s {}-format convention, available names are: '
                    '{project_name}, {url}, {title}, {message}, {tag[%your_tag%]}'),
        initial='**[{project_name}]** [{tag[level]}: {title}]({url})\n\n> {message}'
    )

class WxworkNotificationsPlugin(notify.NotificationPlugin):
    title = 'WeChat Work For HT'
    slug = 'sentry_wxwork'
    description = package_doc
    version = __version__
    author = 'Wjzhang'
    author_url = 'https://github.com/wjzhang-ty/sentry-wxwork'
    resource_links = [
        ('Source', 'https://github.com/wjzhang-ty/sentry-wxwork'),
    ]

    conf_key = 'sentry_wxwork'
    conf_title = title
    project_conf_form = WxworkNotificationsOptionsForm
    logger = logging.getLogger('sentry_wxwork')
    feature_descriptions = [
        FeatureDescription(
            """
            Send notification via WeChat Work for Sentry.
            """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    access_token = None

    def is_configured(self, project, **kwargs):
        f = bool(1)
        return f
    
    def get_config(self, project, **kwargs):
        form = self.project_conf_form
        if not form:
            return []

        return form_to_config(form)

    def build_message(self, group, event, api_url):
        return {
            'system': 'Sentry',
            'title': event.title,
            'projectName': group.project.name,
            'url': group.get_absolute_url(),
            'sentryURL': api_url
        }

    # 发消息
    def send_message(self, payload, project):
        api_origin = self.get_option('api_origin', project)
        api_type = self.get_option('api_type', project)
        safe_urlopen(method=api_type, url=api_origin, json=payload)

    def send_webhook(self, payload, webhook, project):
        self.logger.debug('Sending webhook to url: %s ' % webhook)
        api_origin = self.get_option('api_origin', project)
        api_type = self.get_option('api_type', project)
        response = safe_urlopen(method=api_type, url=api_origin, json=payload)
        self.logger.debug('Response code: %s, content: %s' % (response.status_code, response.content))

    # 似乎是错误推送
    def notify_users(self, group, event, fail_silently=False, **kwargs):
        self.logger.debug('Received notification for event: %s' % event)

        project = group.project
        api_url = self.get_option('api_url', project)
        payload = self.build_message(group, event, api_url)
        self.logger.debug('Built payload: %s' % payload)
        safe_execute(self.send_message, payload, group.project, _with_transaction=False)

        to_webhook = self.get_option('to_webhook', project)
        if to_webhook:
            safe_execute(self.send_webhook, payload, to_webhook, project, _with_transaction=False)
