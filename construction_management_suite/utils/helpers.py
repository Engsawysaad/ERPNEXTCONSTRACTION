"""
Shared utility helpers — Jinja filters, formatting, number-to-words.
Used by print formats and templates.
"""

import frappe
from frappe.utils import flt, fmt_money, money_in_words


def format_currency_arabic(amount, currency="SAR"):
    """Format currency amount in Arabic style (right-to-left aware)."""
    formatted = fmt_money(flt(amount), currency=currency)
    return formatted


def number_to_words_arabic(amount, currency="SAR"):
    """Convert numeric amount to Arabic words for cheques / print formats."""
    try:
        from num2words import num2words
        words = num2words(flt(amount), lang="ar", to="currency")
        return words
    except ImportError:
        # Graceful fallback when num2words not installed
        return money_in_words(flt(amount), currency)
    except Exception:
        return money_in_words(flt(amount), currency)


def arabic_number(value):
    """Jinja filter: convert Western digits to Eastern Arabic-Indic numerals."""
    eastern = {"0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
               "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"}
    return "".join(eastern.get(c, c) for c in str(value))


def get_project_summary(project_name):
    """Return a concise dict of project KPIs for print format headers."""
    project = frappe.db.get_value(
        "Project",
        project_name,
        ["project_name", "customer", "cms_contract_value", "cms_retention_percent",
         "expected_start_date", "expected_end_date", "percent_complete"],
        as_dict=True,
    )
    return project or {}


def get_boq_items_by_section(boq_name):
    """Return BOQ items grouped by boq_section for structured print formats."""
    items = frappe.db.sql(
        """
        SELECT boq_section, item_code, description, uom, qty, rate, amount
        FROM `tabBOQ Item`
        WHERE parent = %s
        ORDER BY boq_section, idx
        """,
        boq_name,
        as_dict=True,
    )
    sections = {}
    for item in items:
        sec = item.get("boq_section") or "General"
        sections.setdefault(sec, []).append(item)
    return sections
