# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.module.medialibrary.fields


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0007_auto_20150128_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='image',
            field=feincms.module.medialibrary.fields.MediaFileForeignKey(to='medialibrary.MediaFile', null=True, blank=True),
            preserve_default=True,
        ),
    ]
