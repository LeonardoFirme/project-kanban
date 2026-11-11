from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_activity_unified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='event_type',
            field=models.CharField(
                choices=[
                    ('team_joined', 'Equipe entrou no projeto'),
                    ('team_left', 'Equipe saiu do projeto'),
                    ('member_joined', 'Membro entrou no projeto'),
                    ('member_left', 'Membro saiu do projeto'),
                    ('task_created', 'Tarefa criada'),
                    ('task_started', 'Tarefa iniciada'),
                    ('task_completed', 'Tarefa concluída'),
                    ('task_reopened', 'Tarefa reaberta'),
                    ('task_status_changed', 'Status da tarefa alterado'),
                    ('project_updated', 'Projeto atualizado'),
                ],
                max_length=30,
                verbose_name='Evento',
            ),
        ),
    ]