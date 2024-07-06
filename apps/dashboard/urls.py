from django.urls import path
from apps.dashboard import views


app_name = "dash"

urlpatterns = [
    path("", views.dash, name="dashboard"),
    path("tax/", views.tax, name="tax"),
    path("billing-month/", views.billing_month, name="billing_month"),
    path("register_manager/", views.register_manager, name="register_manager"),
    path("register_instructor/", views.register_instructor, name="register_instructor"),
    path("register_family/", views.register_family, name="register_family"),
    path("register_student/", views.register_student, name="register_student"),
    path(
        "instructor_student/", views.instructor_student_view, name="instructor_student"
    ),
    path(
        "get_students_by_family/<str:family_id>/",
        views.get_students_by_family,
        name="get_students_by_family",
    ),
    path("classes/", views.classes, name="classes"),
    path("change-password/", views.change_password, name="change_password"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "admin_password_change/",
        views.admin_password_change,
        name="admin_password_change",
    ),
    path("invoices/", views.invoices, name="invoices"),
    path("instructor_invoices/", views.instructor_invoices, name="instructor_invoices"),
    path(
        "family_inv_de/<str:family_id>/",
        views.family_invoice_details,
        name="family_invoice_details",
    ),
    path(
        "invoices/student/<int:student_id>/",
        views.student_invoice_details,
        name="student_invoice_details",
    ),
    path("invoices/instructor/advancesdisc/", views.advancesdisc, name="advancesdisc"),
    path("invoices/families/invoices-link/", views.invoices_link, name="invoices_link"),
]
