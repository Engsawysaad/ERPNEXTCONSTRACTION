"""
India Localization: GST (CGST/SGST/IGST), TDS on subcontractors (194C),
INR currency, retention norms.
"""

import frappe
from frappe.utils import flt


GST_RATE = 18.0
TDS_RATE = 2.0
CURRENCY = "INR"
COUNTRY = "India"


def get_tax_settings():
    return {
        "gst_rate": GST_RATE,
        "tds_subcontractor": TDS_RATE,
        "currency": CURRENCY,
        "gstin_required": True,
    }


def split_gst(amount, is_interstate=False):
    """Return CGST+SGST or IGST split based on inter/intra state."""
    if is_interstate:
        return {"IGST": flt(amount) * GST_RATE / 100}
    half = flt(amount) * GST_RATE / 2 / 100
    return {"CGST": half, "SGST": half}
