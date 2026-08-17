"""
KSA Localization: VAT (15%), ZATCA e-invoicing hooks,
Zakat compliance markers, Arabic bilingual print formats.
"""

import frappe
from frappe.utils import flt


VAT_RATE = 15.0
CURRENCY = "SAR"
COUNTRY = "Saudi Arabia"


def get_vat_settings():
    return {
        "tax_rate": VAT_RATE,
        "tax_account_head": _get_vat_account(),
        "currency": CURRENCY,
        "zatca_enabled": True,
    }


def _get_vat_account():
    try:
        company = frappe.db.get_default("company")
        if not company:
            return None
        return frappe.db.get_value(
            "Account",
            {"account_type": "Tax", "company": company, "account_name": ["like", "%VAT%"]},
            "name",
        )
    except Exception:
        return None


def apply_vat_on_ipc(ipc_doc):
    """Apply 15% VAT to IPC net payable. Called from IPC validate hook."""
    vat = flt(ipc_doc.net_payable_this_period) * VAT_RATE / 100
    ipc_doc.vat_amount = vat
    ipc_doc.net_payable_with_vat = flt(ipc_doc.net_payable_this_period) + vat


def format_arabic_amount(amount, currency=CURRENCY):
    """Return Arabic-formatted amount string for print formats."""
    try:
        from num2words import num2words
        return num2words(amount, lang="ar", to="currency")
    except Exception:
        return str(amount)
