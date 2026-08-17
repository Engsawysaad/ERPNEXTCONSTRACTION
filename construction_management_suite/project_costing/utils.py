import frappe
from frappe.utils import flt, nowdate, add_months, getdate


def sync_erpnext_project(doc, method):
    """Keep Project.expected_end_date and notes in sync with CMS budget."""
    pass


def calculate_daily_variance():
    """Scheduled: recalculate variance for all active project budgets."""
    budgets = frappe.get_all("Project Budget", filters={"status": "Active", "docstatus": 1})
    for b in budgets:
        try:
            doc = frappe.get_doc("Project Budget", b.name)
            doc.fetch_actual_costs()
            doc.fetch_committed_costs()
            doc.calculate_variance()
            doc.db_update()
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"CMS: variance calc failed for {b.name}")


def refresh_cash_flow_projections():
    """Scheduled weekly: refresh cash flow projections on all active budgets."""
    pass


def create_monthly_wip_entries():
    """Scheduled monthly: create WIP Journal Entries for active projects."""
    pass
