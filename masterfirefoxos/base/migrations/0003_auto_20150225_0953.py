# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150218_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locale',
            name='code',
            field=models.CharField(choices=[('bn', 'Bengali'), ('hr', 'Croatian'), ('cs', 'Czech'), ('en', 'English'), ('de', 'German'), ('el', 'Greek'), ('hi', 'Hindi'), ('hu', 'Hungarian'), ('it', 'Italian'), ('ja', 'Japanese'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('sr', 'Serbian'), ('es', 'Spanish'), ('ta', 'Tamil'), ('xx', 'Pirate')], unique=True, db_index=True, max_length=10),  # noqa
            preserve_default=True,
        ),
    ]
