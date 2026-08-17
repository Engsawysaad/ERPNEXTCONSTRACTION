# AGENTS.md — Construction Management Suite

## Project Type

Frappe v16 / ERPNext v16 custom app. **Requires a running Frappe bench with ERPNext installed.**

## Key Commands

```bash
# Install the app on a site
bench --site <site> install-app construction_management_suite

# Run migrations after changes
bench --site <site> migrate

# Build frontend assets
bench build --app construction_management_suite

# Restart after hook/JS changes
bench restart
```

There are **no tests, linting, or CI** in this repo. After making changes, verify with `bench migrate` and `bench build`.

## Architecture

**7 registered modules** (see `modules.txt`), each under `construction_management_suite/<module_name>/`:

| Module | Directory | Key DocTypes |
|--------|-----------|--------------|
| BOQ Management | `boq_management/` | BOQ, BOQ Item, BOQ Template |
| Estimation | `estimation/` | Rate Analysis, Cost Estimation |
| Project Costing | `project_costing/` | Project Budget, Cost Code, WIP Entry |
| Site Management | `site_management/` | Daily Site Report, Site Material Request |
| Progress Billing | `progress_billing/` | Interim Payment Certificate, Retention Release |
| Subcontractor Management | `subcontractor_management/` | Subcontract Agreement, Work Order, Payment Certificate |
| Material Planning | `material_planning/` | Material Forecast, Site Transfer, Consumption Entry |

**Each DocType follows standard Frappe layout:**
```
<module>/doctype/<doctype_name>/
  ├── <doctype_name>.json          # Schema definition
  ├── <doctype_name>.py            # Controller
  └── test_<doctype_name>.py       # (none yet — no tests exist)
```

## ERPNext Integration

This app extends ERPNext **without modifying core** via Custom Fields (prefixed `cms_`). Fields are created in `construction_management_suite/setup.py:after_install()` and re-applied on `after_migrate()`. Affected DocTypes: Project, Purchase Order, Sales Invoice, Stock Entry.

**Do not modify ERPNext core DocType JSON files directly.** Use Custom Fields or Property Setters via fixtures.

## Hooks

`construction_management_suite/hooks.py` is the central wiring file:
- `doc_events` — document lifecycle triggers (on_submit, on_cancel, etc.)
- `scheduler_events` — daily/weekly/monthly background jobs
- `fixtures` — exported Custom Fields, Property Setters, Roles, Workspace
- `permission_query_conditions` — row-level company filtering
- `has_permission` — extra permission gates (e.g., subcontractor isolation)
- `jinja` — custom print format methods/filters
- `override_whitelisted_methods` — currently empty; add here if overriding existing endpoints

## API Endpoints

All whitelisted methods live in `construction_management_suite/api/boq.py`. They are called via Frappe REST or JS `frappe.call`.

## Localization

Regional overrides under `construction_management_suite/localization/{ksa,uae,pakistan,india,...}/`. Each region has an `overrides.py` that hooks into VAT/GST/WHT logic. KSA and UAE are implemented; others are stubs.

## Permissions

- **7 CMS roles** defined in `setup.py:create_roles()` — prefixed with `CMS`.
- Row-level filtering by company via `utils/permissions.py:get_company_filter`.
- Subcontractor users see only their own payment certificates.

## Common Pitfalls

- After editing any DocType JSON or adding Custom Fields, always run `bench --site <site> migrate` to sync.
- `patches.txt` is currently empty — no data patches yet.
- No `opencode.json` or `.cursorrules` exists; add project-specific agent config if needed.
- The `requirements.txt` only lists `frappe` and `erpnext` — no additional Python deps.
- After modifying `hooks.py` (scheduler, doc_events, fixtures), run `bench restart`.
