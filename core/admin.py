from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


from core.models import Song, Event, User, Client, Editor, Manager, Request, SongRights


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        abstract_user_id = kwargs.pop('user_id')
        abstract_user = User.objects.get(pk=abstract_user_id)
        self.fields['user_id'].initial = abstract_user
        super(ClientForm, self).__init__(*args, **kwargs)


class EditorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        abstract_user_id = kwargs.pop('user_id')
        abstract_user = User.objects.get(pk=abstract_user_id)
        self.fields['user_id'].initial = abstract_user
        super(EditorForm, self).__init__(*args, **kwargs)


class ManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        abstract_user_id = kwargs.pop('user_id')
        abstract_user = User.objects.get(pk=abstract_user_id)
        self.fields['user_id'].initial = abstract_user
        super(ManagerForm, self).__init__(*args, **kwargs)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'has_rights']
    search_fields = ['name', 'artist']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("date", "get_host")

    def get_host(self, obj):
        if obj.host is not None:
            return "%s %s" % (obj.host.first_name, obj.host.last_name)
        else:
            return ""
    get_host.admin_order_field = 'организатор'
    get_host.short_description = 'Организатор'

    fieldsets = (
        (None, {'fields': ('date', 'songs', 'request')}),
        (None, {'fields': ('host',), 'classes': ('hidden',)}),
    )

    def save_model(self, request, obj, form, change):
        obj.host = request.user
        request = Request.objects.get(pk=obj.request.id)
        request.state = 'confirmed'
        request.save()
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display = ("username","first_name", "last_name", "email","is_active","is_staff","last_login","date_joined")
    forms = UserUpdateForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'), 'classes': ('hidden',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined'), 'classes': ('hidden',)}),
        (None, {'fields': ('type',)})
    )

    def get_form(self, request, obj=None, **kwargs):
        # self.exclude = ("email", )
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['first_name'].initial = 'Cool'
        return form

    def response_add(self, request, obj, post_url_continue=None):
        if obj.type == 'client':
            return redirect('/core/client/add/?user_id=%s' % obj.id)
        elif obj.type == 'editor':
            return redirect('/core/editor/add/?user_id=%s' % obj.id)
        elif obj.type == 'manager':
            return redirect('/core/manager/add/?user_id=%s' % obj.id)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ['get_first_name', 'get_last_name', 'get_email', 'get_username', 'number']
    # list_filter = ('user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__username', 'number')
    search_fields = ['number']

    def get_first_name(self, obj):
        return obj.user_id.first_name
    get_first_name.admin_order_field = 'имя'
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.user_id.last_name
    get_last_name.admin_order_field = 'Фамилия'
    get_last_name.short_description = 'Фамилия'

    def get_username(self, obj):
        return obj.user_id.username
    get_username.admin_order_field = 'логин'
    get_username.short_description = 'Логин'

    def get_email(self, obj):
        return obj.user_id.email
    get_email.admin_order_field = 'Почта'
    get_email.short_description = 'Почта'

    forms = ClientForm
    fieldsets = (
        (None, {'fields': ('number', 'card_number', 'address')}),
        (None, {'fields': ('user_id',), 'classes': ('hidden',)}),
    )


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    model = Editor
    list_display = ['get_first_name', 'get_last_name', 'get_email', 'get_username', 'staff_code']
    search_fields = ['staff_code']

    def get_first_name(self, obj):
        return obj.user_id.first_name
    get_first_name.admin_order_field = 'имя'
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.user_id.last_name
    get_last_name.admin_order_field = 'Фамилия'
    get_last_name.short_description = 'Фамилия'

    def get_username(self, obj):
        return obj.user_id.username
    get_username.admin_order_field = 'логин'
    get_username.short_description = 'Логин'

    def get_email(self, obj):
        return obj.user_id.email
    get_email.admin_order_field = 'Почта'
    get_email.short_description = 'Почта'

    forms = EditorForm
    fieldsets = (
        (None, {'fields': ('staff_code',)}),
        (None, {'fields': ('user_id',), 'classes': ('hidden',)}),
    )


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    model = Manager
    list_display = ['get_first_name', 'get_last_name', 'get_email', 'get_username', 'staff_code']
    search_fields = ['staff_code']

    def get_first_name(self, obj):
        return obj.user_id.first_name
    get_first_name.admin_order_field = 'имя'
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.user_id.last_name
    get_last_name.admin_order_field = 'Фамилия'
    get_last_name.short_description = 'Фамилия'

    def get_username(self, obj):
        return obj.user_id.username
    get_username.admin_order_field = 'логин'
    get_username.short_description = 'Логин'

    def get_email(self, obj):
        return obj.user_id.email
    get_email.admin_order_field = 'Почта'
    get_email.short_description = 'Почта'

    forms = ManagerForm
    fieldsets = (
        (None, {'fields': ('staff_code',)}),
        (None, {'fields': ('user_id',), 'classes': ('hidden',)}),
    )


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['get_first_name', 'date', 'state']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'имя'
    get_first_name.short_description = 'Имя'

    fieldsets = (
        (None, {'fields': ('date', 'music')}),
        (None, {'fields': ('state', 'user'), 'classes': ('hidden',)}),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.state = 'processing'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(RequestAdmin, self).get_queryset(request)
        if request.user.type == 'client':
            return qs.filter(user=request.user)
        return qs


@admin.register(SongRights)
class SongRightsAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'status']
    list_filter = ('status',)
    search_fields = ['name', 'artist']


