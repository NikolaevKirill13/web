from django.contrib import admin
from django import forms
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id_tg', 'warn')
    exclude = ('warn',)


class BlockingInLine(admin.StackedInline):
    model = Block
    extra = 1
    exclude = ('warn', )


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class BlockForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Мембер', widget=forms.Select)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'stop_time')
    list_filter = ('permanent',)
    fields = ('user', 'start_time', 'permanent')
    #form = BlockForm


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('keyboard_id', 'user_id')
    list_filter = ('user_id', 'keyboard_id')
