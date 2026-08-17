import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class DailySiteReport(Document):
    def validate(self):
        self.validate_date()
        self.set_submitted_by()
        self.calculate_labour_cost()

    def validate_date(self):
        if self.report_date and self.report_date > nowdate():
            frappe.throw(_("Report date cannot be in the future"))

    def set_submitted_by(self):
        if not self.submitted_by:
            self.submitted_by = frappe.session.user

    def calculate_labour_cost(self):
        for row in self.labour:
            row.daily_cost = flt(row.headcount) * flt(row.daily_rate)

    def on_submit(self):
        self.status = "Submitted"
        self._update_project_progress()
        self._create_timesheet_entries()

    def _update_project_progress(self):
        """Update ERPNext Project percent_complete from this report."""
        if self.project and self.cumulative_percent_complete:
            frappe.db.set_value(
                "Project",
                self.project,
                "percent_complete",
                flt(self.cumulative_percent_complete),
            )

    def _create_timesheet_entries(self):
        """For each labour row, optionally create ERPNext Timesheet entries."""
        pass


def on_submit(doc, method):
    doc.on_submit()
