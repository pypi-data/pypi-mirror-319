from django.urls import path

from dj_waanverse_auth.views.login_views import mfa_login_view
from dj_waanverse_auth.views.mfa_views import (
    activate_mfa_view,
    activate_mfa_with_code_view,
    deactivate_mfa_view,
    generate_recovery_codes_view,
    get_recovery_codes_view,
)

urlpatterns = [
    path("activate/", activate_mfa_view, name="mfa_activate"),
    path("deactivate/", deactivate_mfa_view, name="mfa_deactivate"),
    path("login/", mfa_login_view, name="mfa_login"),
    path(
        "activate/verify/", activate_mfa_with_code_view, name="mfa_activate_with_code"
    ),
    path("recovery-codes/", get_recovery_codes_view, name="get_recovery_codes"),
    path(
        "generate-recovery-codes/",
        generate_recovery_codes_view,
        name="generate_recovery_codes",
    ),
]
