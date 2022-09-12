# Generated by Django 3.2.14 on 2022-08-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variavel', models.CharField(max_length=50, unique=True)),
                ('valor', models.CharField(blank=True, max_length=400, null=True)),
            ],
            options={
                'verbose_name': 'configuração',
                'verbose_name_plural': 'configurações',
                'ordering': ['variavel'],
            },
        ),
    ]