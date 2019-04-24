# Generated by Django 2.1.1 on 2018-09-26 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_personlabel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Similarpeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_label', models.IntegerField(db_column='id_label', null=True)),
                ('similar_person', models.CharField(db_column='similar_person', max_length=45, null=True)),
                ('similar', models.IntegerField(db_column='similar', null=True)),
            ],
            options={
                'db_table': 'similar_people',
                'managed': False,
            },
        ),
    ]
