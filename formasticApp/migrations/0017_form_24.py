# Generated by Django 4.2.5 on 2023-10-12 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formasticApp', '0016_delete_form_16'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form_24',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('Text0', models.CharField()),
                ('Email_Field1', models.CharField()),
                ('Number2', models.CharField()),
                ('Password_Field3', models.CharField()),
                ('Multiple_Choice4', models.CharField()),
                ('Checkbox5', models.CharField()),
                ('Radio6', models.CharField()),
                ('Dropdown7', models.CharField()),
                ('Date_Field8', models.DateField()),
                ('File_Field9', models.FileField(null=True, upload_to='uploads/')),
                ('Text_Area10', models.TextField(default='')),
            ],
        ),
    ]
