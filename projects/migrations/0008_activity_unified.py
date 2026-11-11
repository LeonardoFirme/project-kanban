import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def migrate_history_to_activity(apps, schema_editor):
    ProjectTeamHistory = apps.get_model('projects', 'ProjectTeamHistory')
    ProjectMemberHistory = apps.get_model('projects', 'ProjectMemberHistory')
    Activity = apps.get_model('projects', 'Activity')

    for h in ProjectTeamHistory.objects.all():
        Activity.objects.create(
            project_id=h.project_id,
            event_type='team_joined',
            team_id=h.team_id,
            description=h.team.name if h.team else '',
            created_at=h.joined_at,
        )
        if h.left_at:
            Activity.objects.create(
                project_id=h.project_id,
                event_type='team_left',
                team_id=h.team_id,
                description=h.team.name if h.team else '',
                created_at=h.left_at,
            )

    for h in ProjectMemberHistory.objects.all():
        Activity.objects.create(
            project_id=h.project_id,
            event_type='member_joined',
            user_id=h.user_id,
            team_id=h.team_id,
            description=h.user.username if h.user else '',
            created_at=h.joined_at,
        )
        if h.left_at:
            Activity.objects.create(
                project_id=h.project_id,
                event_type='member_left',
                user_id=h.user_id,
                team_id=h.team_id,
                description=h.user.username if h.user else '',
                created_at=h.left_at,
            )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0007_datetime_editable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('team_joined', 'Equipe entrou no projeto'), ('team_left', 'Equipe saiu do projeto'), ('member_joined', 'Membro entrou no projeto'), ('member_left', 'Membro saiu do projeto'), ('task_created', 'Tarefa criada'), ('task_started', 'Tarefa iniciada'), ('task_completed', 'Tarefa concluída'), ('task_reopened', 'Tarefa reaberta'), ('project_updated', 'Projeto atualizado')], max_length=30, verbose_name='Evento')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Criado em')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='projects.project', verbose_name='Projeto')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='projects.task', verbose_name='Tarefa')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='projects.team', verbose_name='Equipe')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Atividade',
                'verbose_name_plural': 'Atividades',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['project', '-created_at'], name='projects_ac_project_9aebc8_idx'),
        ),
        migrations.RunPython(migrate_history_to_activity, migrations.RunPython.noop),
        migrations.DeleteModel(name='ProjectMemberHistory'),
        migrations.DeleteModel(name='ProjectTeamHistory'),
    ]