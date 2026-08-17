/**
 * Construction Management Suite — Global JS
 * Shared utilities, project dashboard widget, quick entry helpers.
 */

/* ── Global Namespace ── */
window.CMS = window.CMS || {};

CMS.getProjectDashboard = function (project, callback) {
    frappe.call({
        method: "construction_management_suite.api.boq.get_project_cost_dashboard",
        args: { project },
        callback: (r) => callback && callback(r.message),
    });
};

CMS.renderKPICard = function (container, label, value, currency, state) {
    const formatted = format_currency(value, currency);
    const stateClass = state ? `cms-kpi-card ${state}` : "cms-kpi-card";
    $(container).append(`
        <div class="${stateClass}">
            <div class="cms-kpi-value">${formatted}</div>
            <div class="cms-kpi-label">${label}</div>
        </div>
    `);
};

CMS.renderProgressBar = function (container, value, max) {
    const pct = max > 0 ? Math.min((value / max) * 100, 100) : 0;
    const cls = pct > 100 ? "over-budget" : pct > 80 ? "warning" : "";
    $(container).html(`
        <div class="cms-progress-bar">
            <div class="cms-progress-fill ${cls}" style="width:${pct}%"></div>
        </div>
        <small class="text-muted">${pct.toFixed(1)}%</small>
    `);
};

/* ── Quick Actions ── */
CMS.quickCreateDailyReport = function (project) {
    frappe.new_doc("Daily Site Report", { project });
};

CMS.quickCreateSMR = function (project) {
    frappe.new_doc("Site Material Request", { project });
};

/* ── Form-level Shortcuts ── */
frappe.ui.form.on("Project", {
    refresh(frm) {
        if (frm.doc.name && !frm.is_new()) {
            frm.add_custom_button(__("View BOQs"), () => {
                frappe.set_route("List", "BOQ", { project: frm.doc.name });
            }, __("CMS"));
            frm.add_custom_button(__("Project Budget"), () => {
                frappe.set_route("List", "Project Budget", { project: frm.doc.name });
            }, __("CMS"));
            frm.add_custom_button(__("Daily Reports"), () => {
                frappe.set_route("List", "Daily Site Report", { project: frm.doc.name });
            }, __("CMS"));
            frm.add_custom_button(__("Cost Dashboard"), () => {
                CMS.getProjectDashboard(frm.doc.name, (data) => {
                    if (!data) return;
                    const dialog = new frappe.ui.Dialog({
                        title: __("Project Cost Dashboard — {0}", [frm.doc.name]),
                        size: "large",
                    });
                    const $body = $(dialog.body);
                    $body.css({ display: "flex", flexWrap: "wrap", padding: "16px" });
                    const b = data.budget || {};
                    CMS.renderKPICard($body, __("Total Budget"), b.total_budget, frm.doc.currency, "");
                    CMS.renderKPICard($body, __("Actual Cost"), b.total_actual_cost, frm.doc.currency,
                        (b.budget_utilization_percent || 0) > 90 ? "over-budget" : "on-track");
                    CMS.renderKPICard($body, __("Total Billed"), (data.billing || {}).total_billed, frm.doc.currency, "");
                    dialog.show();
                });
            }, __("CMS"));
        }
    },
});
