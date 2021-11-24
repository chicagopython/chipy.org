import datetime

from django.db import migrations, models

def copy_duration_from_days_to_expire_to_time_to_expire(apps, schema_editor):
    JobPost = apps.get_model('job_board', 'JobPost')
    for job_post in JobPost.objects.all():
        job_post.time_to_expire = datetime.timedelta(days=job_post.days_to_expire)
        job_post.save()

class Migration(migrations.Migration):
    dependencies = [
        ('job_board', '0009_jobpost_time_to_expire'),
    ]
    operations = [
        migrations.RunPython(copy_duration_from_days_to_expire_to_time_to_expire),
    ]
