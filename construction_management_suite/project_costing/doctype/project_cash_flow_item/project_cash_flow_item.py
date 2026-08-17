import frappe
from frappe.model.document import Document
from frappe.utils import flt


class ProjectCashFlowItem(Document):
    def validate(self):
        self.planned_net = flt(self.planned_inflow) - flt(self.planned_outflow)
        self.actual_net = flt(self.actual_inflow) - flt(self.actual_outflow)
        self.variance = flt(self.actual_net) - flt(self.planned_net)
