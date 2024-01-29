from django.urls import path
from .views import *

urlpatterns = [
    path("register/",Register),
    path("login/",Login),
    path("dashboard/",Dashboard),
    path("validate/",Validate),
    path("valid-mails/",ValidMails),
    path("invalid-mails/",InvalidMails),
    path("valid-mails-csv/",ValidMailsCSV),
    path("invalid-mails-csv/",InvalidMailsCSV),
    path("logout/",Logout),
]