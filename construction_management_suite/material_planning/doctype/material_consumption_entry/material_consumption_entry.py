import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class MaterialConsumptionEntry(Document):
    def validate(self):
        for item in self.items:
            item.amount = flt(item.qty) * flt(item.valuation_rate)

    def on_submit(self):
        self.status = "Submitted"
        self._create_stock_entry()

    def _create_stock_entry(self):
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Material Consumption for Manufacture"
        se.company = self.company
        se.posting_date = self.posting_date
        se.project = self.project
        for item in self.items:
            se.append("items", {
                "item_code": item.item_code,
                "qty": flt(item.qty),
                "uom": item.uom,
                "s_warehouse": self.warehouse,
                "batch_no": item.batch_no,
            })
        se.insert(ignore_permissions=True)
        se.submit()
        self.db_set("stock_entry_ref", se.name)
        frappe.msgprint(_("Stock Entry {0} submitted for material consumption").format(se.name))


def on_submit(doc, method):
    doc.on_submit()
