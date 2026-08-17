def project_overview():
    return {
        "heatmap": True,
        "heatmap_message": "Construction Project Activity",
        "fieldname": "project",
        "transactions": [
            {"label": "Billing", "items": ["Interim Payment Certificate", "Retention Release"]},
            {"label": "Site", "items": ["Daily Site Report", "Site Material Request"]},
            {"label": "Subcontracting", "items": ["Subcontract Agreement", "Subcontractor Payment Certificate"]},
            {"label": "Planning", "items": ["BOQ", "Cost Estimation", "Project Budget"]},
        ],
    }
