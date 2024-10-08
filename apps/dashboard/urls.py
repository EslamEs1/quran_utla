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
    path("register_marketer/", views.register_marketer, name="register_marketer"),
    path("register_student/", views.register_student, name="register_student"),
    path(
        "instructor_student/", views.instructor_student_view, name="instructor_student"
    ),
    path(
        "marketer_student_view/",
        views.marketer_student_view,
        name="marketer_student_view",
    ),
    path(
        "get_students_by_family/<str:family_id>/",
        views.get_students_by_family,
        name="get_students_by_family",
    ),
    path("classes/", views.classes, name="classes"),
    path("change-password/", views.change_password, name="change_password"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "admin_password_change/",
        views.admin_password_change,
        name="admin_password_change",
    ),
    path("invoices/", views.invoices, name="invoices"),
    path("instructor_invoices/", views.instructor_invoices, name="instructor_invoices"),
    path(
        "instructor/invoices/detail/",
        views.instructor_invoices_detail,
        name="instructor_invoices_detail",
    ),
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
    path("users/removed/", views.users_removed, name="users_removed"),
    path(
        "users/active-user/<int:user_id>/",
        views.delete_user,
        name="delete_user",
    ),
    path(
        "users/delete-users-list/<int:user_id>/",
        views.delete_users_list,
        name="delete_users_list",
    ),
    path(
        "marketer-commissions/",
        views.marketer_commission_view,
        name="marketer_commission_view",
    ),
    path("markete-his-students/", views.marketer_students, name="marketer_students"),
    path("contact/", views.contact, name="contact"),
    path("teacher-contact/", views.teacher_contact, name="teacher_contact"),
    path("edit-billing-month/", views.edit_billing_month, name="edit_billing_month"),
    path(
        "delete-billing-month/<int:id>/",
        views.delete_billing_month,
        name="delete_billing_month",
    ),
    path("edit_manager/<int:id>/", views.edit_manager, name="edit_manager"),
    path("delete_manager/<int:id>/", views.delete_manager, name="delete_manager"),
    path("edit_family/<str:id>/", views.edit_family, name="edit_family"),
    path("delete_family/<str:id>/", views.delete_family, name="delete_family"),
    path("edit_instructor/<int:id>/", views.edit_instructor, name="edit_instructor"),
    path("edit_student/<int:id>/", views.edit_student, name="edit_student"),
    path("delete_student/<int:id>/", views.delete_student, name="delete_student"),
    path(
        "del_student_instructor/<int:id>/",
        views.del_student_instructor,
        name="del_student_instructor",
    ),
    path("edit_classes/<int:id>/", views.edit_classes, name="edit_classes"),
    path("delete_classes/<int:id>/", views.delete_classes, name="delete_classes"),
    path("edit_markter/<int:id>/", views.edit_markter, name="edit_markter"),
    path("delete_markter/<int:id>/", views.delete_markter, name="delete_markter"),
    path(
        "del_student_marketer/<int:id>/",
        views.del_student_marketer,
        name="del_student_marketer",
    ),
    path("delete_disc/<int:id>/", views.delete_disc, name="delete_disc"),
    path("requestorder/", views.requestorder, name="requestorder"),
]
