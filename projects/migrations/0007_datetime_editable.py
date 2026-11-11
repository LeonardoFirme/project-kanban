import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_team_member_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Atualizado em'),
        ),
    ]