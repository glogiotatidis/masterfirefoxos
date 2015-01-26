from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

import jingo
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent


jingo.env.install_gettext_translations(translation)


Page.register_templates(
    {
        'title': 'Content template',
        'path': 'content.html',
        'regions': (
            ('main', 'Main content area'),
        ),
    },
    {
        'title': 'Home template',
        'path': 'home.html',
        'regions': (
            ('main', 'Main content area'),
        ),
    }
)


class YouTubeParagraphEntry(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    youtube_id = models.CharField(max_length=100)
    _l10n_fields = ['title', 'text', 'youtube_id']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'videoparagraph.html',
            {
                'title': _(self.title),
                'text': _(self.text),
                'video': _(self.youtube_id)
            }
        )


class MediaParagraphEntry(MediaFileContent):
    title = models.CharField(max_length=255)
    text = models.TextField()
    _l10n_fields = ['title', 'text']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'mediaparagraph.html',
            {
                'title': _(self.title),
                'text': _(self.text),
                'mediafile': self.mediafile
            }
        )


class FAQEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    _l10n_fields = ['question', 'answer']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string(
            'faqentry.html',
            {
                'question': _(self.question),
                'answer': _(self.answer),
            }
        )


class RichTextEntry(RichTextContent):
    _l10n_fields = ['text']

    class Meta:
        abstract = True

    def render(self, **kwargs):
        return render_to_string('richtext.html', {'html': _(self.text)})


class QuizEntry(models.Model):
    question = models.TextField(max_length=255)
    image = models.FileField(blank=True, null=True)
    answer_1 = models.TextField(max_length=255, help_text='This is the correct answer')
    answer_2 = models.TextField(max_length=255)
    answer_3 = models.TextField(max_length=255, blank=True, default='')
    answer_4 = models.TextField(max_length=255, blank=True, default='')

    _l10n_fields = ['question', 'answer_1', 'answer_2',
                    'answer_3', 'answer_4']

    class Meta:
        abstract = True

    @property
    def answers(self):
        import random
        a = [
            {'correct': True, 'text': _(self.answer_1)}
        ]
        for i in range(2, 5):
            value = getattr(self, 'answer_{}'.format(i))
            if getattr(self, 'answer_{}'.format(i)):
                a.append({'correct': False, 'text': _(value)})

        random.shuffle(a)
        return a

    def render(self, **kwargs):
        return render_to_string(
            'quizentry.html',
            {
                'question': _(self.question),
                'image': self.image,
                'answers': self.answers,
            }
        )



Page.create_content_type(RichTextEntry)
Page.create_content_type(MediaParagraphEntry,
                         TYPE_CHOICES=(('default', 'default'),))
Page.create_content_type(FAQEntry)
Page.create_content_type(YouTubeParagraphEntry)
Page.create_content_type(QuizEntry)
