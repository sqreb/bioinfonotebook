# Generated by Django 2.0.1 on 2018-02-07 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('doc', models.TextField()),
                ('priority', models.IntegerField(default=0)),
                ('url', models.CharField(default='NA', max_length=255)),
                ('public', models.BooleanField(default=False)),
                ('root', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DocRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', related_query_name='child', to='docs.Doc')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', related_query_name='parent', to='docs.Doc')),
            ],
        ),
        migrations.CreateModel(
            name='InfoTag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('Pri', 'Primary'), ('Sec', 'Secondary'), ('S', 'Success'), ('Dag', 'Danger'), ('E', 'Warning'), ('If', 'Info'), ('Lt', 'Light'), ('Dk', 'Dark'), ('Lk', 'Link')], max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SearchTag',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='doc',
            name='info_tags',
            field=models.ManyToManyField(to='docs.InfoTag'),
        ),
        migrations.AddField(
            model_name='doc',
            name='search_tags',
            field=models.ManyToManyField(to='docs.SearchTag'),
        ),
    ]