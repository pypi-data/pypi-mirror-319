# Generated by Django 3.0.3 on 2020-05-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('django_attachments', '0002_auto_20180727_0804'),
	]

	operations = [
		migrations.AddField(
			model_name='attachment',
			name='options',
			field=models.TextField(blank=True, verbose_name='Options'),
		),
	]
