from .models import ProfileSettingsForm, ExperienceForm # Import the models
from .models import Payment
from django.contrib import admin
from .models import ContactMessage, ThemePreference, UserRegistration, InviteCode

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

class ThemePreferenceAdmin(admin.ModelAdmin):
    list_display = ('email', 'theme_preference')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_of_birth')
    search_fields = ('name', 'email')

class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'invite_code')
    search_fields = ('email', 'invite_code')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order_id', 'created_at')
    search_fields = ('payment_id', 'order_id')


class ProfileSettingsFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_number',
                    'country', 'state_region')
    search_fields = ('name', 'email', 'mobile_number',
                     'country', 'state_region')





class ExperienceFormAdmin(admin.ModelAdmin):
    list_display = ('email', 'designing_experience', 'additional_details')
    search_fields = ('email', 'designing_experience', 'additional_details')


admin.site.register(ExperienceForm, ExperienceFormAdmin)
admin.site.register(ProfileSettingsForm, ProfileSettingsFormAdmin)

# Register the models with the admin site


# Register the models and their respective admin classes
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(ThemePreference, ThemePreferenceAdmin)
admin.site.register(UserRegistration, UserProfileAdmin)
admin.site.register(InviteCode, InviteCodeAdmin)
