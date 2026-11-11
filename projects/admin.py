from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Activity, Project, Task, Team, UserProfile

admin.site.site_header = "Kanban"
admin.site.site_title = "Kanban Admin"
admin.site.index_title = "Painel de Controle"

admin.site.unregister(User)


class UserProfileInline(StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil"
    fk_name = "user"
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    search_fields = ("username", "email", "first_name", "last_name")
    list_display = ("username", "avatar_preview", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    inlines = (UserProfileInline,)
    readonly_fields = ("last_login",)

    @admin.display(description="Avatar")
    def avatar_preview(self, obj):
        profile = getattr(obj, "profile", None)
        if profile and profile.avatar:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />',
                profile.avatar.url,
            )
        return "—"


class ActivityInline(TabularInline):
    model = Activity
    extra = 0
    fields = ("event_type", "team", "user", "task", "created_at")
    readonly_fields = ("event_type", "created_at")
    ordering = ("-created_at",)
    max_num = 20
    can_delete = False


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ("name", "avatar_preview", "members_count", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    filter_horizontal = ("members",)

    @admin.display(description="Avatar")
    def avatar_preview(self, obj):
        if obj and obj.avatar:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />',
                obj.avatar.url,
            )
        return "—"

    @admin.display(description="Membros")
    def members_count(self, obj):
        return obj.members.count()


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ("name", "status", "owner", "teams_list", "start_date", "end_date", "created_at")
    list_filter = ("status", "owner", "teams", "created_at")
    search_fields = ("name", "description")
    filter_horizontal = ("teams",)
    autocomplete_fields = ("owner",)
    inlines = (ActivityInline,)

    @admin.display(description="Equipes")
    def teams_list(self, obj):
        return ", ".join(t.name for t in obj.teams.all()) or "—"


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = ("title", "project", "assignee", "priority", "status", "due_date", "created_at")
    list_filter = ("status", "priority", "project", "assignee", "created_at")
    search_fields = ("title", "description")
    list_select_related = ("project", "assignee")


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ("user", "avatar_preview")
    search_fields = ("user__username", "user__email")

    @admin.display(description="Avatar")
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />',
                obj.avatar.url,
            )
        return "—"


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ("created_at", "project", "event_type", "team", "user", "task")
    list_filter = ("event_type", "created_at", "project", "team")
    search_fields = ("project__name", "team__name", "user__username", "task__title")
    list_select_related = ("project", "team", "user", "task")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)