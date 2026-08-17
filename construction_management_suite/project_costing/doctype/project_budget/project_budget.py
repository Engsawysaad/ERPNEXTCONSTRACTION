import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ProjectBudget(Document):
    def validate(self):
        self.fetch_actual_costs()
        self.fetch_committed_costs()
        self.calculate_variance()

    def fetch_actual_costs(self):
        """Sum stock entries, payroll, and purchase invoices tagged to this project."""
        actual = (
            frappe.db.sql(
                """
                SELECT SUM(credit_amount - debit_amount) AS actual
                FROM `tabGL Entry`
                WHERE project = %s AND docstatus = 1 AND is_cancelled = 0
                """,
                self.project,
                as_dict=True,
            )[0].get("actual")
            or 0
        )
        self.total_actual_cost = flt(abs(actual))
        self._distribute_actuals_to_items()

    def fetch_committed_costs(self):
        """Sum outstanding Purchase Orders for this project."""
        committed = (
            frappe.db.sql(
                """
                SELECT SUM(grand_total - advance_paid) AS committed
                FROM `tabPurchase Order`
                WHERE project = %s AND docstatus = 1 AND status NOT IN ('Completed','Cancelled')
                """,
                self.project,
                as_dict=True,
            )[0].get("committed")
            or 0
        )
        self.total_committed_cost = flt(committed)

    def _distribute_actuals_to_items(self):
        """Placeholder — in production this should break down by cost code GL tags."""
        pass

    def calculate_variance(self):
        self.variance_amount = flt(self.total_budget) - flt(self.total_actual_cost)
        if flt(self.total_budget) > 0:
            self.budget_utilization_percent = flt(self.total_actual_cost) / flt(self.total_budget) * 100
        for item in self.items:
            item.variance = flt(item.budgeted_amount) - flt(item.actual_amount)

    def on_submit(self):
        self.status = "Active"
        self.db_set("status", "Active")

    @frappe.whitelist()
    def refresh_actuals(self) -> None:
        self.fetch_actual_costs()
        self.fetch_committed_costs()
        self.calculate_variance()
        self.save()
        frappe.msgprint(_("Actuals refreshed"))
