import frappe
from frappe.utils import flt, nowdate, getdate


def check_retention_release():
    """Scheduled daily: notify if defects liability period has ended for any project."""
    today = getdate(nowdate())
    candidates = frappe.db.sql(
        """
        SELECT rr.name, rr.project, rr.defects_liability_period_end, rr.release_amount
        FROM `tabRetention Release` rr
        WHERE rr.docstatus = 0
          AND rr.status = 'Approved'
          AND rr.defects_liability_period_end <= %s
        """,
        today,
        as_dict=True,
    )
    for r in candidates:
        frappe.sendmail(
            recipients=[frappe.db.get_value("Project", r.project, "owner")],
            subject=f"[CMS] Retention Release Due — {r.project}",
            message=f"Retention release {r.name} for project {r.project} is now due. "
                    f"Defects liability period ended on {r.defects_liability_period_end}. "
                    f"Amount: {r.release_amount}",
        )
