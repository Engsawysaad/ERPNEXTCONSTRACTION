import frappe


def execute():
    """Ensure core DocType tables exist. v16-compatible: uses bench migrate instead of DbManager."""
    core_doctypes = [
        "Module Def",
        "Role",
        "User",
        "Notification",
        "User Role",
        "Installed Applications",
    ]
    for dt in core_doctypes:
        try:
            if not frappe.db.table_exists(dt):
                frappe.reload_doc("core", "doctype", dt.lower().replace(" ", "_"))
                frappe.db.commit()
                print(f"Created: {dt}")
            else:
                print(f"Exists:  {dt}")
        except Exception as e:
            print(f"Error {dt}: {e}")
