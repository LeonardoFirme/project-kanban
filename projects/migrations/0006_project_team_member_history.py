import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTeamHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Entrou em')),
                ('left_at', models.DateTimeField(blank=True, null=True, verbose_name='Saiu em')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_history', to='projects.project', verbose_name='Projeto')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_history', to='projects.team', verbose_name='Equipe')),
            ],
            options={
                'verbose_name': 'Histórico de Equipe',
                'verbose_name_plural': 'Histórico de Equipes',
                'ordering': ['-joined_at'],
            },
        ),
        migrations.CreateModel(
            name='ProjectMemberHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Entrou em')),
                ('left_at', models.DateTimeField(blank=True, null=True, verbose_name='Saiu em')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_history', to='projects.project', verbose_name='Projeto')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_history', to='projects.team', verbose_name='Equipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_history', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Histórico de Membro',
                'verbose_name_plural': 'Histórico de Membros',
                'ordering': ['-joined_at'],
            },
        ),
    ]