import frappe
from frappe.utils import flt, nowdate, add_days


def recompute_forecasts():
    """Scheduled daily: update Material Forecast 'already ordered qty' from open POs."""
    forecasts = frappe.get_all(
        "Material Forecast",
        filters={"status": ["in", ["Draft", "Approved"]], "docstatus": 1},
    )
    for f in forecasts:
        try:
            doc = frappe.get_doc("Material Forecast", f.name)
            for item in doc.items:
                ordered = frappe.db.sql(
                    """
                    SELECT SUM(poi.qty) AS total
                    FROM `tabPurchase Order Item` poi
                    JOIN `tabPurchase Order` po ON po.name = poi.parent
                    WHERE poi.item_code = %s
                      AND po.project = %s
                      AND po.docstatus = 1
                      AND po.status NOT IN ('Completed','Cancelled')
                    """,
                    (item.item_code, doc.project),
                    as_dict=True,
                )
                item.already_ordered_qty = flt((ordered[0] or {}).get("total", 0))
                item.net_qty_required = flt(item.boq_qty) * (1 + flt(item.waste_factor) / 100)
                item.qty_to_order = max(0, flt(item.net_qty_required) - flt(item.already_ordered_qty))
                item.estimated_value = flt(item.qty_to_order) * flt(item.estimated_rate)
            doc.total_forecast_qty_value = sum(flt(i.estimated_value) for i in doc.items)
            doc.db_update()
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"CMS: forecast recompute failed for {f.name}")
