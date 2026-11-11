from datetime import date

from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Activity, Project, Task, Team


def dashboard_callback(request, context):
    context.update({
        'total_projects': Project.objects.count(),
        'total_tasks': Task.objects.count(),
        'total_teams': Team.objects.count(),
        'total_users': User.objects.count(),
        'recent_projects': Project.objects.prefetch_related('teams')[:5],
        'recent_tasks': Task.objects.select_related('project', 'assignee')[:5],
    })
    return context


def public_home(request):
    status_labels = dict(Project.STATUS_CHOICES)
    projects_status = Project.objects.values('status').annotate(total=Count('id')).order_by('status')
    chart_projects_status = {
        'labels': [status_labels.get(i['status'], i['status']) for i in projects_status],
        'values': [i['total'] for i in projects_status],
    }

    priority_labels = dict(Task.PRIORITY_CHOICES)
    tasks_priority = Task.objects.values('priority').annotate(total=Count('id')).order_by('priority')
    chart_tasks_priority = {
        'labels': [priority_labels.get(i['priority'], i['priority']) for i in tasks_priority],
        'values': [i['total'] for i in tasks_priority],
    }

    task_status_labels = dict(Task.STATUS_CHOICES)
    tasks_status = Task.objects.values('status').annotate(total=Count('id')).order_by('status')
    chart_tasks_status = {
        'labels': [task_status_labels.get(i['status'], i['status']) for i in tasks_status],
        'values': [i['total'] for i in tasks_status],
    }

    today = date.today()
    months = []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        months.append((y, m))

    timeline = Project.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id'))
    timeline_map = {(i['month'].year, i['month'].month): i['total'] for i in timeline if i['month']}

    month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    chart_projects_timeline = {
        'labels': [f"{month_names[m - 1]}/{str(y)[2:]}" for y, m in months],
        'values': [timeline_map.get((y, m), 0) for y, m in months],
    }

    context = {
        'total_projects': Project.objects.count(),
        'total_tasks': Task.objects.count(),
        'total_teams': Team.objects.count(),
        'projects': Project.objects.prefetch_related('teams').order_by('-created_at'),
        'chart_projects_status': chart_projects_status,
        'chart_tasks_priority': chart_tasks_priority,
        'chart_tasks_status': chart_tasks_status,
        'chart_projects_timeline': chart_projects_timeline,
    }
    return render(request, 'public/home.html', context)


def public_calendar(request):
    return render(request, 'public/calendar.html')


def public_calendar_events(request):
    events = []

    for project in Project.objects.prefetch_related('teams'):
        if project.start_date:
            events.append({
                'title': f"▶ {project.name}",
                'start': project.start_date.isoformat(),
                'url': f"/projetos/{project.pk}/",
                'backgroundColor': '#9333ea',
                'borderColor': '#7e22ce',
            })
        if project.end_date:
            events.append({
                'title': f"■ {project.name}",
                'start': project.end_date.isoformat(),
                'url': f"/projetos/{project.pk}/",
                'backgroundColor': '#16a34a',
                'borderColor': '#15803d',
            })

    for task in Task.objects.select_related('project'):
        if task.due_date:
            color = '#dc2626' if task.priority == 'urgent' else '#f97316' if task.priority == 'high' else '#3b82f6' if task.priority == 'medium' else '#6b7280'
            events.append({
                'title': f"✓ {task.title}",
                'start': task.due_date.isoformat(),
                'url': f"/projetos/{task.project.pk}/",
                'backgroundColor': color,
                'borderColor': color,
            })

    return JsonResponse(events, safe=False)


def public_project_detail(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related('teams', 'tasks__assignee'), pk=pk)
    tasks = project.tasks.select_related('assignee').order_by('-created_at')
    activities = project.activities.select_related('team', 'user', 'task').order_by('-created_at')
    context = {
        'project': project,
        'tasks': tasks,
        'activities': activities,
    }
    return render(request, 'public/project_detail.html', context)


def public_tasks(request):
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    tasks = Task.objects.select_related('project', 'assignee').prefetch_related('project__teams')
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    context = {
        'tasks': tasks.order_by('-created_at'),
        'status_filter': status,
        'priority_filter': priority,
    }
    return render(request, 'public/tasks.html', context)