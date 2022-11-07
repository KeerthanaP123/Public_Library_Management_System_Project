from django.contrib import admin
from django.contrib.auth.models import Group
from . models import category,Account,Book
from django.contrib.auth.admin import UserAdmin
# #  Register your models here.
admin.site.unregister(Group)
admin.site.site_header="Library"
admin.site.site_title="Welcome To Admin's Dashboard"
admin.site.index_title="Welcome to public Library"
admin.site.register(Account)

class AccountAdmin(UserAdmin):
    list_display = ('fname','lname','email','contact','address','city','state','pincode','roles','status')
    ordering=('fname',)
    search_fields = ('fname','email')
    filter_horizontal = ()
    list_per_page = 50
    list_filter = ('fname','email')
    filedsets=()
    list_display_links = ('email')


admin.site.register(Book)
class categoryadmin(admin.ModelAdmin):
    list_display = ['cat_name']
    search_fields = ('cat_name',)

class bookdisplay(admin.ModelAdmin):
    list_display = ['bk_title']
admin.site.register(category,categoryadmin)
