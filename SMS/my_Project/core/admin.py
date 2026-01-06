#dir
#cd .\my_Project\
#dir
#python manage.py runserver


from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'roll_number',
        'get_username',   # Updated
        'get_email',      # Updated
        'phone',
        'gender',
        'course',
        'status',         # ✅ Status field
    )

    list_filter = (
        'status',
        'gender',
        'course',
    )

    search_fields = (
        'user__username',   # Updated
        'user__email',      # Updated
        'roll_number',
        'phone',
    )

    ordering = ('roll_number',)

    # Functions to get username and email from related User
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
