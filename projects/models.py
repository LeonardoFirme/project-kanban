from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    name = models.CharField(_('Nome'), max_length=100)
    description = models.TextField(_('Descrição'), blank=True, null=True)
    avatar = models.ImageField(_('Avatar'), upload_to='teams/avatars/', blank=True, null=True)
    members = models.ManyToManyField('auth.User', blank=True, related_name='teams', verbose_name=_('Membros'))
    created_at = models.DateTimeField(_('Criado em'), default=timezone.now)

    class Meta:
        verbose_name = _('Equipe')
        verbose_name_plural = _('Equipes')
        ordering = ['name']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile', verbose_name=_('Usuário'))
    avatar = models.ImageField(_('Avatar'), upload_to='users/avatars/', blank=True, null=True)

    class Meta:
        verbose_name = _('Perfil')
        verbose_name_plural = _('Perfis')

    def __str__(self):
        return self.user.username


class Project(models.Model):
    STATUS_CHOICES = (
        ('planning', _('Planejamento')),
        ('in_progress', _('Em Andamento')),
        ('completed', _('Concluído')),
        ('on_hold', _('Em Espera')),
    )
    name = models.CharField(_('Nome'), max_length=150)
    description = models.TextField(_('Descrição'), blank=True, null=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='planning')
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_projects',
        verbose_name=_('Responsável'),
    )
    teams = models.ManyToManyField(Team, blank=True, related_name='projects', verbose_name=_('Equipes'))
    start_date = models.DateField(_('Data de Início'), null=True, blank=True)
    end_date = models.DateField(_('Data de Término'), null=True, blank=True)
    created_at = models.DateTimeField(_('Criado em'), default=timezone.now)
    updated_at = models.DateTimeField(_('Atualizado em'), default=timezone.now)

    class Meta:
        verbose_name = _('Projeto')
        verbose_name_plural = _('Projetos')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_unique_members(self):
        seen = set()
        result = []
        for team in self.teams.all():
            for member in team.members.all():
                if member.id not in seen:
                    seen.add(member.id)
                    result.append(member)
        return result


class Activity(models.Model):
    EVENT_TEAM_JOINED = 'team_joined'
    EVENT_TEAM_LEFT = 'team_left'
    EVENT_MEMBER_JOINED = 'member_joined'
    EVENT_MEMBER_LEFT = 'member_left'
    EVENT_TASK_CREATED = 'task_created'
    EVENT_TASK_STARTED = 'task_started'
    EVENT_TASK_COMPLETED = 'task_completed'
    EVENT_TASK_REOPENED = 'task_reopened'
    EVENT_TASK_STATUS_CHANGED = 'task_status_changed'
    EVENT_PROJECT_UPDATED = 'project_updated'

    EVENT_CHOICES = (
        (EVENT_TEAM_JOINED, _('Equipe entrou no projeto')),
        (EVENT_TEAM_LEFT, _('Equipe saiu do projeto')),
        (EVENT_MEMBER_JOINED, _('Membro entrou no projeto')),
        (EVENT_MEMBER_LEFT, _('Membro saiu do projeto')),
        (EVENT_TASK_CREATED, _('Tarefa criada')),
        (EVENT_TASK_STARTED, _('Tarefa iniciada')),
        (EVENT_TASK_COMPLETED, _('Tarefa concluída')),
        (EVENT_TASK_REOPENED, _('Tarefa reaberta')),
        (EVENT_TASK_STATUS_CHANGED, _('Status da tarefa alterado')),
        (EVENT_PROJECT_UPDATED, _('Projeto atualizado')),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities', verbose_name=_('Projeto'))
    event_type = models.CharField(_('Evento'), max_length=30, choices=EVENT_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities', verbose_name=_('Equipe'))
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='activities', verbose_name=_('Usuário'))
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='activities', verbose_name=_('Tarefa'))
    description = models.TextField(_('Descrição'), blank=True, null=True)
    created_at = models.DateTimeField(_('Criado em'), default=timezone.now)

    class Meta:
        verbose_name = _('Atividade')
        verbose_name_plural = _('Atividades')
        ordering = ['-created_at']
        indexes = [models.Index(fields=['project', '-created_at'])]

    def __str__(self):
        return f"{self.get_event_type_display()} @ {self.project.name}"

    @property
    def icon(self):
        return {
            self.EVENT_TEAM_JOINED: 'group_add',
            self.EVENT_TEAM_LEFT: 'group_remove',
            self.EVENT_MEMBER_JOINED: 'person_add',
            self.EVENT_MEMBER_LEFT: 'person_remove',
            self.EVENT_TASK_CREATED: 'add_task',
            self.EVENT_TASK_STARTED: 'play_arrow',
            self.EVENT_TASK_COMPLETED: 'task_alt',
            self.EVENT_TASK_REOPENED: 'restart_alt',
            self.EVENT_TASK_STATUS_CHANGED: 'sync_alt',
            self.EVENT_PROJECT_UPDATED: 'edit',
        }.get(self.event_type, 'info')

    @property
    def color(self):
        return {
            self.EVENT_TEAM_JOINED: 'green',
            self.EVENT_TEAM_LEFT: 'red',
            self.EVENT_MEMBER_JOINED: 'green',
            self.EVENT_MEMBER_LEFT: 'red',
            self.EVENT_TASK_CREATED: 'blue',
            self.EVENT_TASK_STARTED: 'yellow',
            self.EVENT_TASK_COMPLETED: 'green',
            self.EVENT_TASK_REOPENED: 'orange',
            self.EVENT_TASK_STATUS_CHANGED: 'purple',
            self.EVENT_PROJECT_UPDATED: 'gray',
        }.get(self.event_type, 'gray')


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', _('Baixa')),
        ('medium', _('Média')),
        ('high', _('Alta')),
        ('urgent', _('Urgente')),
    )
    STATUS_CHOICES = (
        ('todo', _('A Fazer')),
        ('doing', _('Fazendo')),
        ('review', _('Revisão')),
        ('done', _('Concluído')),
    )
    title = models.CharField(_('Título'), max_length=200)
    description = models.TextField(_('Descrição'), blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Projeto'))
    assignee = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Responsável'))
    priority = models.CharField(_('Prioridade'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(_('Data de Vencimento'), null=True, blank=True)
    created_at = models.DateTimeField(_('Criado em'), default=timezone.now)
    updated_at = models.DateTimeField(_('Atualizado em'), default=timezone.now)

    class Meta:
        verbose_name = _('Tarefa')
        verbose_name_plural = _('Tarefas')
        ordering = ['-created_at']

    def __str__(self):
        return self.title