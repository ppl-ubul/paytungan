from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted


class SplitBillAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "highlight_deleted_field",
        "name",
        "user_fund_id",
    ) + SafeDeleteAdmin.list_display
    list_filter = (
        "name",
        SafeDeleteAdminFilter,
    ) + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"


class BillAdmin(SafeDeleteAdmin):
    list_display = (
        highlight_deleted,
        "highlight_deleted_field",
        "split_bill_id",
        "user_id",
    ) + SafeDeleteAdmin.list_display
    list_filter = (
        "user_id",
        SafeDeleteAdminFilter,
    ) + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"
