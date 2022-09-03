from django.urls import path
from .views import *

app_name = "dlp"
urlpatterns = [
    path('dashboard/', dashboard_views, name="dashboard"),
    path('policy/', policy_views, name="policy"),
    path('rules/', rules_views, name="rules"),
    path('logs/', logs_views, name="logs"),

    # only superuser
    path('add_policy/', add_policy_views, name="add_policy"),
    path('update_policy/<int:id>/', update_policy_views, name="update_policy"),
    path('delete_policy/<int:id>/', delete_policy_views, name="delete_policy"),

    path('add_rule/', add_rule_views, name="add_rule"),
    path('update_rule/<int:id>/', update_rule_views, name="update_rule"),
    path('delete_rule/<int:id>/', delete_rule_views, name="delete_rule"),

    path('update_log/<int:id>/', update_log_views, name="update_log"),
    path('delete_log/<int:id>/', delete_log_views, name="delete_log"),

    # export
    path('export/log/excel/', logs_export_excel_views, name="logs_export_excel"),
    path('export/log/csv/', logs_export_csv_views, name="logs_export_csv"),
]
