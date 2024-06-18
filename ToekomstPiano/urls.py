from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# Define URL patterns
urlpatterns = [
    # Index page
    path("", views.INDEX, name="INDEX"),
    # Home page
    path("HOME", views.HOME, name="HOME"),  
    # Login page
    path("LOGIN", views.LOGIN, name="LOGIN"),  
    # Country page
    path("COUNTRY", views.COUNTRY, name="COUNTRY"), 
    # Registration form
    path("REGISTRATION_FORM", views.REGISTRATION_FORM,name="REGISTRATION_FORM"),  
    # Services page
    path("SERVICES", views.SERVICES, name="SERVICES"), 
    # About page
    path("ABOUT", views.ABOUT, name="ABOUT"), 
    # Grading system page
    path("GRADING_SYSTEM", views.GRADINGSYSTEM,name="GRADING_SYSTEM"),  
    # Documents page
    path("USERHOME/documents/", views.documents,name="documents"), 
    # Feedback page
    path("FEEDBACK", views.FEEDBACK, name="FEEDBACK"), 
    # Terms page
    path("TERMS", views.TERMS, name="TERMS"),  
    # Visa page
    path("USERHOME/Visa", views.VISA, name="Visa"),  
    # Password change page
    path("cp", views.cp, name="cp"),  
    # User home page
    path("USERHOME/", views.USERHOME, name="USERHOME"),  
    # Site map page
    path("USERHOME/SiteMap", views.SiteMap, name="SiteMap"),  
    # User page
    path("Main", views.Main, name="Main"), 
    # Logout page
    path("LOGOUT", views.LOGOUT, name="LOGOUT"),  
    # Profile page
    path("USERHOME/Profile", views.profilepage,name="profilepage"), 
    # Account page
    path("Account", views.Account, name="Account"),  
    
    #     path("h",views.h,name="h"),
    # Visa Details
    path('USERHOME/VisaRequiredDocuments',views.VisaRequiredDocuments, name="VisaRequiredDocument"),
    #profile saved url
    path('profile_saved/', views.profile_saved, name='profile_saved'),
    #payment url
    path('Payment/', views.Payment, name='Payment'),
    #success url
    path('success/', views.success_view, name='success'),
    #USER INBOX url
    path('USERHOME/INBOX', views.INBOX, name='INBOX'),
]
