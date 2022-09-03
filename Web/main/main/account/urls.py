from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    

    path('login/', login_views, name="login"),
    path('logout/', logout_views, name="logout"),

    path('profile/', profile_views, name="profile"),

    # user
    path("update/profile/", update_user_profile_views, name="update_user_profile"),
    path("change_password", change_password_views, name="change_password"),

    # only superuser
    path('users/', users_views, name="users"),
    path('add_user/', add_user_views, name="add_user"),
    path('delete_user/<str:username>', user_delete_views, name="user_delete"),
    path("edit_user/<str:username>", edit_user_views, name="edit_user"),
]
