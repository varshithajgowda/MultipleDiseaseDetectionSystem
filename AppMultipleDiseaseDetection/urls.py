from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from AppMultipleDiseaseDetection.views import Message
urlpatterns = [
    path('', views.Home, name="Home"),
    path('Base/', views.Base, name="Base"),
    path('about/', views.about, name="about"),
    path('Admin_Login/', views.Admin_Login, name="Admin_Login"),
    path('User_Login/', views.User_Login, name="User_Login"),
    path('User_Registration/', views.User_Registration, name="User_Registration"),
    path('Logout/', views.Logout, name="Logout"),
    path('view_users/', views.view_users, name="view_users"),
    path('view_hospitals/', views.view_hospitals, name="view_hospitals"),
    path('prediction/', views.prediction, name="prediction"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path('heart/', views.heart, name="heart"),
    path('liver/', views.liver, name="liver"),
    path('diabetes/', views.diabetes, name="diabetes"),
    path('hospitals/', views.hospitals, name="hospitals"),
    path('update_hospital/', views.update_hospital, name="update_hospital"),
    path('Message/', Message.as_view(), name='Message'),
    path('delete_doctor/', views.delete_doctor, name="delete_doctor"),

    path('Logout/', views.Logout, name="Logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
