# apps/maintainance_addon/maintainance_addon/doctype/asset/asset_dashboard.py

import frappe

def get_data(data):
	"""
	Override the Asset dashboard to show related documents based on machine numbers
	"""
	# Get the current asset name from the context
	asset_name = frappe.form_dict.get('name') or frappe.local.request.args.get('name')
	
	if not asset_name:
		return data
	
	try:
		# Get machine numbers from the asset's machine_part_details child table
		machine_numbers = frappe.db.get_all(
			"Machine Part Details",
			filters={"parent": asset_name, "parenttype": "Asset"},
			fields=["machine_no"],
			distinct=True
		)
		
		machine_nos = [row.machine_no for row in machine_numbers if row.machine_no]
		
		if not machine_nos:
			# Add a custom section showing no machine numbers found
			if not data.get('custom_sections'):
				data.custom_sections = []
			
			data.custom_sections.append({
				'label': 'Related Documents',
				'content': '<div class="alert alert-info">No machine numbers found in Machine Part Details.</div>'
			})
			return data
		
		# Get Machine Part Issuances
		machine_part_issuances = frappe.db.sql("""
			SELECT 
				name,
				status,
				posting_date as date,
				company,
				work_order
			FROM `tabMachine Part Issuance`
			WHERE machine_no IN %s
			ORDER BY posting_date DESC
			LIMIT 10
		""", (machine_nos,), as_dict=True)
		
		# Get Maintenance Schedules
		maintenance_schedules = frappe.db.sql("""
			SELECT 
				name,
				status,
				start_date as date,
				company,
				asset_name
			FROM `tabMaintenance Schedule`
			WHERE asset_name = %s
			ORDER BY start_date DESC
			LIMIT 10
		""", (asset_name,), as_dict=True)
		
		# Get Work Orders related to machine numbers
		work_orders = frappe.db.sql("""
			SELECT 
				name,
				status,
				creation as date,
				company,
				production_item
			FROM `tabWork Order`
			WHERE machine_no IN %s
			ORDER BY creation DESC
			LIMIT 10
		""", (machine_nos,), as_dict=True)
		
		# Get Job Cards related to machine numbers
		job_cards = frappe.db.sql("""
			SELECT 
				name,
				status,
				creation as date,
				company,
				work_order
			FROM `tabJob Card`
			WHERE machine_no IN %s
			ORDER BY creation DESC
			LIMIT 10
		""", (machine_nos,), as_dict=True)
		
		# Create custom sections for each document type
		if not data.get('custom_sections'):
			data.custom_sections = []
		
		# Machine Part Issuances section
		if machine_part_issuances:
			mpi_html = create_document_table('Machine Part Issuances', machine_part_issuances, [
				{'key': 'name', 'label': 'MPI', 'doctype': 'Machine Part Issuance'},
				{'key': 'status', 'label': 'Status'},
				{'key': 'date', 'label': 'Date'},
				{'key': 'work_order', 'label': 'Work Order'},
				{'key': 'company', 'label': 'Company'},
			])
			data.custom_sections.append({
				'label': f'Machine Part Issuances ({len(machine_part_issuances)})',
				'content': mpi_html
			})
		
		# Maintenance Schedules section
		if maintenance_schedules:
			ms_html = create_document_table('Maintenance Schedules', maintenance_schedules, [
				{'key': 'name', 'label': 'MS', 'doctype': 'Maintenance Schedule'},
				{'key': 'status', 'label': 'Status'},
				{'key': 'date', 'label': 'Start Date'},
				{'key': 'asset_name', 'label': 'Asset'},
				{'key': 'company', 'label': 'Company'},
			])
			data.custom_sections.append({
				'label': f'Maintenance Schedules ({len(maintenance_schedules)})',
				'content': ms_html
			})
		
		# Work Orders section
		if work_orders:
			wo_html = create_document_table('Work Orders', work_orders, [
				{'key': 'name', 'label': 'WO', 'doctype': 'Work Order'},
				{'key': 'status', 'label': 'Status'},
				{'key': 'date', 'label': 'Created'},
				{'key': 'production_item', 'label': 'Item'},
				{'key': 'company', 'label': 'Company'},
			])
			data.custom_sections.append({
				'label': f'Work Orders ({len(work_orders)})',
				'content': wo_html
			})
		
		# Job Cards section
		if job_cards:
			jc_html = create_document_table('Job Cards', job_cards, [
				{'key': 'name', 'label': 'JC', 'doctype': 'Job Card'},
				{'key': 'status', 'label': 'Status'},
				{'key': 'date', 'label': 'Created'},
				{'key': 'work_order', 'label': 'Work Order'},
				{'key': 'company', 'label': 'Company'},
			])
			data.custom_sections.append({
				'label': f'Job Cards ({len(job_cards)})',
				'content': jc_html
			})
		
		# Machine Numbers section
		if machine_nos:
			machine_rows = [{'name': mn, 'status': 'Linked', 'source': 'Machine Part Details'} for mn in machine_nos]
			machine_html = create_document_table('Machine Numbers', machine_rows, [
				{'key': 'name', 'label': 'Machine Number'},
				{'key': 'status', 'label': 'Status'},
				{'key': 'source', 'label': 'Source'},
			])
			data.custom_sections.append({
				'label': f'Machine Numbers ({len(machine_nos)})',
				'content': machine_html
			})
		
	except Exception as e:
		frappe.log_error(f"Error in asset dashboard: {e}", "asset_dashboard")
		if not data.get('custom_sections'):
			data.custom_sections = []
		data.custom_sections.append({
			'label': 'Related Documents',
			'content': f'<div class="alert alert-danger">Error loading related documents: {str(e)}</div>'
		})
	
	return data

def create_document_table(title, rows, columns):
	"""
	Create an HTML table for displaying document data
	"""
	html = f'<div class="asset-dashboard-section"><h6>{title}</h6>'
	html += '<div class="table-responsive"><table class="table table-bordered table-condensed">'
	
	# Header
	html += '<thead><tr>'
	for col in columns:
		html += f'<th>{col["label"]}</th>'
	html += '</tr></thead>'
	
	# Body
	html += '<tbody>'
	if rows:
		for row in rows:
			html += '<tr>'
			for col in columns:
				val = row.get(col['key'], '')
				if col['key'] == 'name' and col.get('doctype'):
					# Create clickable link
					route = f'/app/{col["doctype"].lower().replace(" ", "-")}/{frappe.utils.encode_uri_component(val)}'
					val = f'<a href="{route}" target="_blank">{frappe.utils.escape_html(val)}</a>'
				elif col['key'] == 'status' and val:
					# Add status badge
					val = f'<span class="badge badge-secondary">{frappe.utils.escape_html(val)}</span>'
				else:
					val = frappe.utils.escape_html(str(val)) if val else ''
				html += f'<td>{val}</td>'
			html += '</tr>'
	else:
		html += f'<tr><td colspan="{len(columns)}" class="text-muted">No records found</td></tr>'
	
	html += '</tbody></table></div></div>'
	return html
