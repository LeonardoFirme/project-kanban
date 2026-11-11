from django.conf import settings
from django.db import migrations, models


def migrate_team_to_teams(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    for project in Project.objects.all():
        if project.team_id:
            project.teams.add(project.team_id)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_team_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL, verbose_name='Membros'),
        ),
        migrations.AddField(
            model_name='project',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='projects', to='projects.team', verbose_name='Equipes'),
        ),
        migrations.RunPython(migrate_team_to_teams, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='project',
            name='team',
        ),
    ]