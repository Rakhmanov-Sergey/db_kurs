from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


from core.models import Song, Event, User, Client, Editor, Manager, Request


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
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # if request.user.is_authenticated():
        is_client = (request.user.type == "client")
        if is_client:
            form.base_fields['name'].disabled = True

        return form

    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


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

    # def response_change(self, request, obj):
    #     return redirect('/admin/sales/invoice')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    forms = ClientForm
    fieldsets = (
        (None, {'fields': ('number', 'card_number', 'address')}),
        (None, {'fields': ('user_id',), 'classes': ('hidden',)}),
    )


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    forms = EditorForm
    fieldsets = (
        (None, {'fields': ('staff_code',)}),
        (None, {'fields': ('user_id',), 'classes': ('hidden',)}),
    )


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    forms = ManagerForm
    fieldsets = (
        (None, {'fields': ('staff_code',)}),
        (None, {'fields': ('user_id',), 'classes': ('hidden',)}),
    )


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass

