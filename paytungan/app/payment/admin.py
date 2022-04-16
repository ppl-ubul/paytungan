from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted


class PaymentAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "highlight_deleted_field",
        "number",
        "bill_id",
    ) + SafeDeleteAdmin.list_display
    list_filter = (SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"
