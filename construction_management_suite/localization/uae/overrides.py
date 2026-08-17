"""
UAE Localization: VAT (5%), FTA compliance, AED currency.
"""

import frappe
from frappe.utils import flt


VAT_RATE = 5.0
CURRENCY = "AED"
COUNTRY = "United Arab Emirates"


def get_vat_settings():
    return {
        "tax_rate": VAT_RATE,
        "currency": CURRENCY,
        "fta_enabled": True,
    }


def apply_vat_on_ipc(ipc_doc):
    vat = flt(ipc_doc.net_payable_this_period) * VAT_RATE / 100
    ipc_doc.vat_amount = vat
    ipc_doc.net_payable_with_vat = flt(ipc_doc.net_payable_this_period) + vat
