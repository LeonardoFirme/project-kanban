from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='teams/avatars/', verbose_name='Avatar'),
        ),
    ]