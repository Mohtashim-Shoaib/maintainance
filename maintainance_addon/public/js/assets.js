// apps/maintainance_addon/maintainance_addon/public/js/assets.js
// Asset connection panel styles
const ASSET_CONNECTION_STYLES = `
	<style id="asset-connection-styles">
		.asset-section { background:#fff; border:1px solid #e6e9ef; border-radius:8px; box-shadow:0 2px 6px rgba(16,24,40,0.04); padding:12px 12px 6px; margin:12px 0; }
		.asset-section-header { font-weight:600; cursor:pointer; color:#0f62fe; margin:0 0 6px; display:flex; align-items:center; justify-content:space-between; }
		.asset-section-header .asset-title { display:flex; align-items:center; gap:8px; }
		.asset-badge { display:inline-block; background:#eef2ff; color:#1d4ed8; border:1px solid #e0e7ff; border-radius:999px; font-size:11px; padding:2px 8px; }
		.asset-table-wrap { overflow-x:auto; border-radius:6px; }
		.asset-table { width:100%; border-collapse:separate; border-spacing:0; }
		.asset-table th { padding:8px 10px; background:#f8fafc; color:#334155; border-bottom:1px solid #e6e9ef; text-align:left; font-weight:600; font-size:12px; position:sticky; top:0; z-index:1; }
		.asset-table td { padding:8px 10px; border-bottom:1px solid #f1f5f9; font-size:12px; color:#374151; }
		.asset-table tbody tr:nth-child(odd) { background:#fcfdff; }
		.asset-table tbody tr:hover { background:#f1f5ff; }
		.asset-status { font-size:11px; padding:2px 6px; border-radius:999px; border:1px solid #e5e7eb; background:#f9fafb; color:#111827; }
		.asset-actions a { color:#0f62fe; font-size:12px; }
		
		/* Dashboard specific styles */
		.asset-dashboard-section { margin-bottom: 20px; }
		.asset-dashboard-section h6 { color: #0f62fe; font-weight: 600; margin-bottom: 10px; }
		.asset-dashboard-section .table { margin-bottom: 0; }
		.asset-dashboard-section .table th { background-color: #f8fafc; border-top: none; }
		.asset-dashboard-section .table td { vertical-align: middle; }
		.asset-dashboard-section .badge { font-size: 10px; }
	</style>
`;

frappe.ui.form.on('Asset', {
    refresh(frm) {
        console.log('Asset DEBUG: refresh - assets.js loaded!');
        
        // Inject styles once
        if (!document.getElementById('asset-connection-styles')) {
            $('head').append(ASSET_CONNECTION_STYLES);
        }
        
        // Button to open dialog
        if (frm.doc.docstatus >= 0) {
            frm.add_custom_button(__('Related Documents'), function() {
                show_related_documents_for_asset(frm);
            }, __('View'));
        }
        
        // Add custom content to Connection tab
        if (!frm.is_new()) {
            // Test the API first
            test_api_call(frm);
            add_connection_tab_content(frm);
        }
    },
    
    // Listen for tab changes
    onload_post_render(frm) {
        console.log('Asset DEBUG: onload_post_render');
        
        // Add event listener for tab changes
        $(document).on('click', '.nav-link[data-toggle="tab"]', function() {
            const tabName = $(this).attr('data-fieldname');
            console.log('Asset DEBUG: Tab clicked:', tabName);
            
            if (tabName === 'connections_tab' || $(this).text().trim() === 'Connection') {
                setTimeout(() => {
                    console.log('Asset DEBUG: Connection tab activated, adding content');
                    add_connection_tab_content(frm);
                }, 500);
            }
        });
    }
});

// ===== Related Documents panel for Asset =====

function test_api_call(frm) {
    console.log('Asset DEBUG: Testing API call for asset:', frm.doc.name);
    frappe.xcall('maintainance_addon.api.get_related_documents_for_asset', { 
        asset_name: frm.doc.name 
    }).then((result) => {
        console.log('Asset DEBUG: API test result:', result);
    }).catch((error) => {
        console.error('Asset DEBUG: API test error:', error);
    });
}

function add_connection_tab_content(frm) {
    console.log('Asset DEBUG: Adding connection tab content');
    
    // Always use the asset name as a machine number
    const machine_nos = [frm.doc.name];
    console.log('Asset DEBUG: Using asset name as machine number:', machine_nos);
    
    // Also get machine numbers from the child table
    const child_machine_nos = get_machine_numbers_from_asset(frm);
    console.log('Asset DEBUG: Machine numbers from child table:', child_machine_nos);
    
    // Combine both
    const all_machine_nos = [...new Set([...machine_nos, ...child_machine_nos])];
    console.log('Asset DEBUG: All machine numbers:', all_machine_nos);
    
    // Fetch related data and add to connection tab
    fetch_related_data_for_asset(frm).then((data) => {
        console.log('Asset DEBUG: Fetched data:', data);
        
        // Create HTML content for the connection tab
        let html = '<div class="asset-connection-content" style="padding: 20px;">';
        
        // Add Machine Numbers section
        if (all_machine_nos.length > 0) {
            const machine_rows = all_machine_nos.map(machine_no => ({
                name: machine_no,
                status: 'Linked',
                source: machine_no === frm.doc.name ? 'Asset Name' : 'Machine Part Details'
            }));
            
            html += create_connection_table('Machine Numbers', machine_rows, [
                { key: 'name', label: 'Machine Number' },
                { key: 'status', label: 'Status' },
                { key: 'source', label: 'Source' },
            ]);
        }
        
        // Add Machine Part Details section
        if (data.machine_part_issuance_rows && data.machine_part_issuance_rows.length > 0) {
            html += create_connection_table('Machine Part Details', data.machine_part_issuance_rows, [
                { key: 'parent', label: 'Parent', doctype: 'Asset' },
                { key: 'name', label: 'Name', doctype: 'Machine Part Details' },
                { key: 'item_code', label: 'Item Code', doctype: 'Item' },
                { key: 'machine_no', label: 'Machine No' },
                { key: 'stock_entry', label: 'Stock Entry', doctype: 'Stock Entry' },
            ]);
        }
        
        // Add Maintenance Schedules section
        if (data.maintenance_schedule_rows && data.maintenance_schedule_rows.length > 0) {
            html += create_connection_table('Maintenance Schedules', data.maintenance_schedule_rows, [
                { key: 'name', label: 'MS', doctype: 'Maintenance Schedule' },
                { key: 'status', label: 'Status' },
                { key: 'date', label: 'Start Date' },
                { key: 'asset_name', label: 'Asset' },
                { key: 'company', label: 'Company' },
            ]);
        }
        
        // Add Work Orders section
        if (data.work_order_rows && data.work_order_rows.length > 0) {
            html += create_connection_table('Work Orders', data.work_order_rows, [
                { key: 'name', label: 'WO', doctype: 'Work Order' },
                { key: 'status', label: 'Status' },
                { key: 'date', label: 'Created' },
                { key: 'production_item', label: 'Item' },
                { key: 'company', label: 'Company' },
            ]);
        }
        
        // Add Job Cards section
        if (data.job_card_rows && data.job_card_rows.length > 0) {
            html += create_connection_table('Job Cards', data.job_card_rows, [
                { key: 'name', label: 'JC', doctype: 'Job Card' },
                { key: 'status', label: 'Status' },
                { key: 'date', label: 'Created' },
                { key: 'work_order', label: 'Work Order' },
                { key: 'company', label: 'Company' },
            ]);
        }
        
        html += '</div>';
        
        // Add content to the connection tab
        add_html_to_connection_tab(frm, html);
        
    }).catch((error) => {
        console.error('Asset DEBUG: Error adding connection tab content', error);
        add_error_state_to_connection_tab(frm, error);
    });
}

function add_empty_state_to_connection_tab(frm) {
    const html = `
        <div class="asset-connection-content" style="padding: 20px;">
            <div class="alert alert-info">
                <h6>Related Documents</h6>
                <p>Loading related documents for asset: ${frm.doc.name}</p>
            </div>
        </div>
    `;
    add_html_to_connection_tab(frm, html);
}

function add_error_state_to_connection_tab(frm, error) {
    const html = `
        <div class="asset-connection-content" style="padding: 20px;">
            <div class="alert alert-danger">
                <h6>Error Loading Related Documents</h6>
                <p>There was an error loading related documents: ${error.message || error}</p>
            </div>
        </div>
    `;
    add_html_to_connection_tab(frm, html);
}

function add_html_to_connection_tab(frm, html) {
    // Wait for the connection tab to be available
    setTimeout(() => {
        // Try to find the connection tab content area
        const connectionTab = $('.form-layout .tab-content .tab-pane[data-fieldname="connections_tab"]');
        if (connectionTab.length > 0) {
            console.log('Asset DEBUG: Found connection tab, adding content');
            connectionTab.html(html);
        } else {
            // Try alternative selectors
            const alternativeSelectors = [
                '.form-layout .tab-content .tab-pane.active',
                '.form-layout .tab-content .tab-pane:last',
                '.form-layout .tab-content',
                '.form-layout .form-document'
            ];
            
            for (let selector of alternativeSelectors) {
                const element = $(selector);
                if (element.length > 0) {
                    console.log('Asset DEBUG: Found element with selector:', selector);
                    element.append(html);
                    break;
                }
            }
        }
    }, 1000);
}

function create_connection_table(title, rows, columns) {
    let html = `
        <div class="asset-connection-section" style="margin-bottom: 20px;">
            <h6 style="color: #0f62fe; font-weight: 600; margin-bottom: 10px;">${title} (${rows.length})</h6>
            <div class="table-responsive">
                <table class="table table-bordered table-condensed">
                    <thead>
                        <tr>`;
    
    // Header
    columns.forEach(col => {
        html += `<th>${col.label}</th>`;
    });
    html += `</tr></thead><tbody>`;
    
    // Body
    if (rows && rows.length > 0) {
        rows.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                let val = row[col.key] || '';
                if (col.doctype && val) {
                    // Create clickable link for any field with doctype
                    const route = `/app/${col.doctype.toLowerCase().replace(/ /g, '-')}/${encodeURIComponent(val)}`;
                    val = `<a href="${route}" target="_blank" style="color: #0f62fe; text-decoration: none;">${frappe.utils.escape_html(val)}</a>`;
                } else if (col.key === 'status' && val) {
                    // Add status badge
                    val = `<span class="badge badge-secondary">${frappe.utils.escape_html(val)}</span>`;
                } else {
                    val = frappe.utils.escape_html(String(val)) || '';
                }
                html += `<td>${val}</td>`;
            });
            html += '</tr>';
        });
    } else {
        html += `<tr><td colspan="${columns.length}" class="text-muted">No records found</td></tr>`;
    }
    
    html += `</tbody></table></div></div>`;
    return html;
}

function create_dashboard_table(title, rows, columns) {
    let html = `<div class="asset-dashboard-section">
        <h6>${title} (${rows.length})</h6>
        <div class="table-responsive">
            <table class="table table-bordered table-condensed">
                <thead>
                    <tr>`;
    
    // Header
    columns.forEach(col => {
        html += `<th>${col.label}</th>`;
    });
    html += `</tr></thead><tbody>`;
    
    // Body
    if (rows && rows.length > 0) {
        rows.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                let val = row[col.key] || '';
                if (col.doctype && val) {
                    // Create clickable link for any field with doctype
                    const route = `/app/${col.doctype.toLowerCase().replace(/ /g, '-')}/${encodeURIComponent(val)}`;
                    val = `<a href="${route}" target="_blank" style="color: #0f62fe; text-decoration: none;">${frappe.utils.escape_html(val)}</a>`;
                } else if (col.key === 'status' && val) {
                    // Add status badge
                    val = `<span class="badge badge-secondary">${frappe.utils.escape_html(val)}</span>`;
                } else {
                    val = frappe.utils.escape_html(String(val)) || '';
                }
                html += `<td>${val}</td>`;
            });
            html += '</tr>';
        });
    } else {
        html += `<tr><td colspan="${columns.length}" class="text-muted">No records found</td></tr>`;
    }
    
    html += `</tbody></table></div></div>`;
    return html;
}

function get_machine_numbers_from_asset(frm) {
    console.log('Asset DEBUG: Getting machine numbers from asset');
    console.log('Asset DEBUG: frm.doc:', frm.doc);
    console.log('Asset DEBUG: machine_part_details:', frm.doc.machine_part_details);
    
    const set = new Set();
    const rows = Array.isArray(frm.doc.machine_part_details) ? frm.doc.machine_part_details : [];
    console.log('Asset DEBUG: rows length:', rows.length);
    
    rows.forEach((r, index) => { 
        console.log(`Asset DEBUG: Row ${index}:`, r);
        if (r.machine_no) {
            console.log('Asset DEBUG: Found machine_no:', r.machine_no);
            set.add(r.machine_no); 
        }
    });
    
    const result = Array.from(set);
    console.log('Asset DEBUG: Final machine numbers:', result);
    return result;
}

async function fetch_related_data_for_asset(frm) {
    if (!frm.doc.name) {
        return {
            machine_part_issuances_count: 0,
            machine_part_issuance_rows: [],
            maintenance_schedules_count: 0,
            maintenance_schedule_rows: [],
            work_orders_count: 0,
            work_order_rows: [],
            job_cards_count: 0,
            job_card_rows: []
        };
    }

    try {
        const result = await frappe.xcall('maintainance_addon.api.get_related_documents_for_asset', { 
            asset_name: frm.doc.name 
        });
        return result || {
            machine_part_issuances_count: 0,
            machine_part_issuance_rows: [],
            maintenance_schedules_count: 0,
            maintenance_schedule_rows: [],
            work_orders_count: 0,
            work_order_rows: [],
            job_cards_count: 0,
            job_card_rows: []
        };
    } catch (e) {
        console.warn('Asset DEBUG: Failed to fetch related data', e);
        return {
            machine_part_issuances_count: 0,
            machine_part_issuance_rows: [],
            maintenance_schedules_count: 0,
            maintenance_schedule_rows: [],
            work_orders_count: 0,
            work_order_rows: [],
            job_cards_count: 0,
            job_card_rows: []
        };
    }
}

function render_table_asset(titleId, titleLabel, count, rows, columns) {
    const header = `
		<div id="${titleId}" class="asset-section-header">
			<div class="asset-title">${titleLabel} <span class="asset-badge">${count||0}</span></div>
			<div class="asset-actions"><a>View All</a></div>
		</div>
	`;
    const ths = columns.map(c => `<th>${c.label}</th>`).join('');
    const trs = (rows||[]).map(r => {
        const tds = columns.map(c => {
            let val = r[c.key];
            if (c.key === 'status' && val) {
                val = `<span class="asset-status">${frappe.utils.escape_html(val)}</span>`;
            }
            if (c.key === 'name' && c.doctype) {
                const route = `/app/${c.doctype.toLowerCase().replace(/ /g,'-')}/${encodeURIComponent(val)}`;
                val = `<a href="${route}" target="_blank">${frappe.utils.escape_html(val||'')}</a>`;
            }
            return `<td>${val ?? ''}</td>`;
        }).join('');
        return `<tr>${tds}</tr>`;
    }).join('');
    const table = `
		<div class="asset-table-wrap">
			<table class="asset-table">
				<thead><tr>${ths}</tr></thead>
				<tbody>${trs || `<tr><td colspan="${columns.length}" style="padding:8px; color:#888; font-size:12px;">None</td></tr>`}</tbody>
			</table>
		</div>`;
    return `<div class="asset-section">${header}${table}</div>`;
}

function render_related_panel_html_for_asset(data) {
    return `
		<div style="padding: 6px 2px;">
			${render_table_asset('mpi-link', 'Machine Part Issuances', data.machine_part_issuances_count, data.machine_part_issuance_rows, [
				{ key: 'name', label: 'MPI', doctype: 'Machine Part Issuance' },
				{ key: 'status', label: 'Status' },
				{ key: 'date', label: 'Date' },
				{ key: 'work_order', label: 'Work Order' },
				{ key: 'company', label: 'Company' },
			])}
			${render_table_asset('ms-link', 'Maintenance Schedules', data.maintenance_schedules_count, data.maintenance_schedule_rows, [
				{ key: 'name', label: 'MS', doctype: 'Maintenance Schedule' },
				{ key: 'status', label: 'Status' },
				{ key: 'date', label: 'Start Date' },
				{ key: 'asset_name', label: 'Asset' },
				{ key: 'company', label: 'Company' },
			])}
			${render_table_asset('wo-link', 'Work Orders', data.work_orders_count, data.work_order_rows, [
				{ key: 'name', label: 'WO', doctype: 'Work Order' },
				{ key: 'status', label: 'Status' },
				{ key: 'date', label: 'Created' },
				{ key: 'production_item', label: 'Item' },
				{ key: 'company', label: 'Company' },
			])}
			${render_table_asset('jc-link', 'Job Cards', data.job_cards_count, data.job_card_rows, [
				{ key: 'name', label: 'JC', doctype: 'Job Card' },
				{ key: 'status', label: 'Status' },
				{ key: 'date', label: 'Created' },
				{ key: 'work_order', label: 'Work Order' },
				{ key: 'company', label: 'Company' },
			])}
		</div>
	`;
}

function attach_section_routes_for_asset() {
    const setRoute = (doctype, filters) => frappe.set_route('List', doctype, filters || {});
    const routeFull = (doctype) => setRoute(doctype);
    $('#mpi-link').on('click', () => routeFull('Machine Part Issuance')).next('.asset-actions')?.on('click', () => routeFull('Machine Part Issuance'));
    $('#ms-link').on('click', () => routeFull('Maintenance Schedule')).next('.asset-actions')?.on('click', () => routeFull('Maintenance Schedule'));
    $('#wo-link').on('click', () => routeFull('Work Order')).next('.asset-actions')?.on('click', () => routeFull('Work Order'));
    $('#jc-link').on('click', () => routeFull('Job Card')).next('.asset-actions')?.on('click', () => routeFull('Job Card'));
}

function render_custom_connections_panel_for_asset(frm) {
    const machine_nos = get_machine_numbers_from_asset(frm);
    if (!machine_nos.length) {
        frm.fields_dict.custom_connection_dashboards.$wrapper.empty().html(`
            <div class="asset-section">
                <div class="asset-section-header">
                    <div class="asset-title">Related Documents <span class="asset-badge">0</span></div>
                </div>
                <div style="padding:8px; color:#888; font-size:12px;">No machine numbers found in Machine Part Details.</div>
            </div>
        `);
        return;
    }
    
    // Create a simple display showing the machine numbers from machine_part_details
    const machine_rows = machine_nos.map(machine_no => ({
        name: machine_no,
        status: 'Linked',
        source: 'Machine Part Details'
    }));
    
    const html = `
        <div style="padding: 6px 2px;">
            ${render_table_asset('machine-link', 'Machine Numbers', machine_rows.length, machine_rows, [
                { key: 'name', label: 'Machine Number' },
                { key: 'status', label: 'Status' },
                { key: 'source', label: 'Source' },
            ])}
        </div>
    `;
    
    frm.fields_dict.custom_connection_dashboards.$wrapper.empty().html(html);
    attach_section_routes_for_asset();
}

function show_related_documents_for_asset(frm) {
    frappe.show_alert({message: __('Fetching related documents...'), indicator: 'blue'});
    fetch_related_data_for_asset(frm).then((data) => {
        const dlg = new frappe.ui.Dialog({ 
            title: __('Related Documents for Asset'), 
            size: 'large', 
            fields: [{ fieldname: 'html', fieldtype: 'HTML' }] 
        });
        const html = render_related_panel_html_for_asset(data || {});
        dlg.fields_dict.html.$wrapper.html(html);
        attach_section_routes_for_asset();
        dlg.show();
    });
}
