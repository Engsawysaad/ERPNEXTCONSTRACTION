"""
Row-level permission helpers — multi-company isolation.
"""

import frappe


def get_company_filter(user):
    """Restrict queries to companies the user is allowed to access."""
    if "CMS Admin" in frappe.get_roles(user):
        return ""
    companies = frappe.db.get_list(
        "User Permission",
        filters={"user": user, "allow": "Company", "is_default": 0},
        pluck="company",
    )
    if not companies:
        # Fall back to default company
        default = frappe.defaults.get_user_default("company", user)
        companies = [default] if default else []
    if not companies:
        return "1=0"  # No access
    placeholder = ", ".join(["%s"] * len(companies))
    return f"`tabBOQ`.company in ({placeholder})" % tuple(companies)


def has_permission(doc, user=None, permission_type=None):
    """
    Extra permission gate: subcontractors may only see their own documents.
    """
    user = user or frappe.session.user
    roles = frappe.get_roles(user)

    # Admins always pass
    if "CMS Admin" in roles or "System Manager" in roles:
        return True

    # Subcontractor portal users: only their linked supplier records
    if "CMS Subcontractor" in roles and doc.doctype == "Subcontractor Payment Certificate":
        supplier = frappe.db.get_value("Supplier", {"email_id": user}, "name")
        return doc.subcontractor == supplier

    return True
