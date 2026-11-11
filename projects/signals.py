from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Activity, Project, Task, Team


@receiver(pre_save, sender=Project)
def project_pre_save(sender, instance, **kwargs):
    if instance.pk:
        instance.updated_at = timezone.now()
        try:
            old = Project.objects.get(pk=instance.pk)
            if old.status != instance.status:
                Activity.objects.create(
                    project=instance,
                    event_type=Activity.EVENT_PROJECT_UPDATED,
                    description=f"Status: {old.get_status_display()} \u2192 {instance.get_status_display()}",
                )
        except Project.DoesNotExist:
            pass


@receiver(post_save, sender=Project)
def project_post_save(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            project=instance,
            event_type=Activity.EVENT_PROJECT_UPDATED,
            description="Projeto criado",
        )


@receiver(pre_save, sender=Task)
def task_pre_save(sender, instance, **kwargs):
    if instance.pk:
        instance.updated_at = timezone.now()
        try:
            instance._old_status = Task.objects.get(pk=instance.pk).status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            project=instance.project,
            event_type=Activity.EVENT_TASK_CREATED,
            task=instance,
            user=instance.assignee,
            description=instance.title,
        )
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status and old_status != instance.status:
        old_label = dict(Task.STATUS_CHOICES).get(old_status, old_status)
        new_label = dict(Task.STATUS_CHOICES).get(instance.status, instance.status)

        Activity.objects.create(
            project=instance.project,
            event_type=Activity.EVENT_TASK_STATUS_CHANGED,
            task=instance,
            user=instance.assignee,
            description=f"{instance.title} \u2014 {old_label} \u2192 {new_label}",
        )


@receiver(m2m_changed, sender=Project.teams.through)
def project_teams_changed(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for team_id in pk_set:
            team = Team.objects.get(pk=team_id)
            Activity.objects.create(
                project=instance,
                event_type=Activity.EVENT_TEAM_JOINED,
                team=team,
                description=team.name,
            )
    elif action == 'post_remove':
        for team_id in pk_set:
            try:
                team = Team.objects.get(pk=team_id)
            except Team.DoesNotExist:
                continue
            Activity.objects.create(
                project=instance,
                event_type=Activity.EVENT_TEAM_LEFT,
                team=team,
                description=team.name,
            )


@receiver(m2m_changed, sender=Team.members.through)
def team_members_changed(sender, instance, action, pk_set, **kwargs):
    team = instance
    if action == 'post_add':
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                continue
            for project in team.projects.all():
                Activity.objects.create(
                    project=project,
                    event_type=Activity.EVENT_MEMBER_JOINED,
                    team=team,
                    user=user,
                    description=user.username,
                )
    elif action == 'post_remove':
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                continue
            for project in team.projects.all():
                Activity.objects.create(
                    project=project,
                    event_type=Activity.EVENT_MEMBER_LEFT,
                    team=team,
                    user=user,
                    description=user.username,
                )