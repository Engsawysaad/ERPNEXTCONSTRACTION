import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class RateAnalysis(Document):
    def validate(self):
        self.calculate_resources()
        self.calculate_totals()

    def calculate_resources(self):
        for res in self.resources:
            res.amount = flt(res.qty) * flt(res.rate)
            res.net_amount = flt(res.amount) * (1 + flt(res.waste_factor) / 100)

    def calculate_totals(self):
        totals = {"Material": 0, "Labour": 0, "Equipment": 0, "Subcontract": 0, "Overhead": 0}
        for res in self.resources:
            rt = res.resource_type
            if rt in totals:
                totals[rt] += flt(res.net_amount)

        self.total_material_cost = totals["Material"]
        self.total_labour_cost = totals["Labour"]
        self.total_equipment_cost = totals["Equipment"]
        self.total_subcontract_cost = totals["Subcontract"]
        self.total_overhead_cost = totals["Overhead"]
        self.total_cost = sum(totals.values())
        output = flt(self.output_qty) or 1
        self.rate_per_unit = self.total_cost / output
