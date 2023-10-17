import re

from rest_framework import settings
from rest_framework.exceptions import ValidationError


class UrlValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        youtube_pattern = r'^(https?://(?:www\.)?youtube\.com/)'

        if url:
            app_domains = getattr(settings, 'ALLOWED_HOSTS', None)
            if app_domains:
                for domain in app_domains:
                    app_pattern = r'^(https?://(?:www\.)?{re.escape(domain)])'
                    if re.match(app_pattern, url) or re.match(youtube_pattern, url):
                        break
                else:
                    raise ValidationError(
                      'Недопустимый URL. Ссылка должна вести только на youtube.com'
                    )
            else:
                if not re.match(youtube_pattern, url):
                    raise ValidationError(
                        'Недопустимый URL. Ссылка должна вести только на youtube.com'
                    )