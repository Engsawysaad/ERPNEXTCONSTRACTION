"""
Pakistan Localization: GST (17%), WHT on subcontractors, PKR currency.
"""

import frappe
from frappe.utils import flt


GST_RATE = 17.0
WHT_RATE_SUBCONTRACTOR = 6.0
CURRENCY = "PKR"
COUNTRY = "Pakistan"


def get_tax_settings():
    return {
        "gst_rate": GST_RATE,
        "wht_subcontractor": WHT_RATE_SUBCONTRACTOR,
        "currency": CURRENCY,
    }


def apply_wht_on_payment_certificate(doc):
    """Apply WHT deduction on subcontractor payment certs for Pakistan."""
    wht = flt(doc.net_payable) * WHT_RATE_SUBCONTRACTOR / 100
    doc.wht_deduction = wht
    doc.net_payable_after_wht = flt(doc.net_payable) - wht
