from frappe import _


def get_data():
    return [
        {
            "module_name": "BOQ Management",
            "label": _("BOQ Management"),
            "color": "#1abc9c",
            "icon": "octicon octicon-list-ordered",
            "type": "module",
            "description": _("Bill of Quantities — creation, revisions, templates and rate linkage"),
        },
        {
            "module_name": "Estimation",
            "label": _("Estimation"),
            "color": "#3498db",
            "icon": "octicon octicon-graph",
            "type": "module",
            "description": _("Cost estimation, rate analysis and tender workflows"),
        },
        {
            "module_name": "Project Costing",
            "label": _("Project Costing"),
            "color": "#e74c3c",
            "icon": "octicon octicon-dashboard",
            "type": "module",
            "description": _("Budget monitoring, WIP tracking and cash flow forecasting"),
        },
        {
            "module_name": "Site Management",
            "label": _("Site Management"),
            "color": "#f39c12",
            "icon": "octicon octicon-tools",
            "type": "module",
            "description": _("Daily reports, attendance, material requests and progress tracking"),
        },
        {
            "module_name": "Progress Billing",
            "label": _("Progress Billing"),
            "color": "#9b59b6",
            "icon": "octicon octicon-file-text",
            "type": "module",
            "description": _("IPC, running bills, retention and client certification workflows"),
        },
        {
            "module_name": "Subcontractor Management",
            "label": _("Subcontractor Management"),
            "color": "#2ecc71",
            "icon": "octicon octicon-organization",
            "type": "module",
            "description": _("Subcontract agreements, work orders and payment certificates"),
        },
        {
            "module_name": "Material Planning",
            "label": _("Material Planning"),
            "color": "#e67e22",
            "icon": "octicon octicon-package",
            "type": "module",
            "description": _("Procurement planning, forecasting, consumption and site transfers"),
        },
    ]
