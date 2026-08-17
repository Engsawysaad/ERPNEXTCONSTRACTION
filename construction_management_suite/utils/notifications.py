"""
Notification configuration for Frappe notification engine.
"""

import frappe


def get_notification_config():
    return {
        "for_doctype": {
            "BOQ": {"status": "Draft"},
            "Interim Payment Certificate": {"status": "Draft"},
            "Subcontract Agreement": {"status": "Draft"},
            "Daily Site Report": {"status": "Draft"},
        }
    }
