# Copyright (c) 2025, Maintainance Addon and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	columns = [
		{
			"fieldname": "machine_no",
			"label": _("Machine No"),
			"fieldtype": "Link",
			"options": "Asset",
			"width": 120
		},
		{
			"fieldname": "item_code",
			"label": _("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"fieldname": "issued_qty",
			"label": _("Issued Qty"),
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "uom",
			"label": _("UOM"),
			"fieldtype": "Data",
			"width": 80
		},
		{
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "stock_entry",
			"label": _("Stock Entry"),
			"fieldtype": "Link",
			"options": "Stock Entry",
			"width": 150
		},
		{
			"fieldname": "operator_name",
			"label": _("Operator Name"),
			"fieldtype": "Link",
			"options": "Machine Operator",
			"width": 150
		},
		{
			"fieldname": "parent",
			"label": _("Parent"),
			"fieldtype": "Link",
			"options": "Machine Parts Issuance",
			"width": 150
		}
	]
	return columns


def get_data(filters):
	# Build the query to get data from Machine Part Details
	mpd = DocType("Machine Part Details")
	se = DocType("Stock Entry")
	
	# Base query to get data from Machine Part Details
	query = (
		frappe.qb.from_(mpd)
		.select(
			mpd.item_code,
			mpd.issued_qty,
			mpd.uom,
			mpd.machine_no,
			mpd.date,
			mpd.stock_entry,
			mpd.operator_name,
			mpd.parent
		)
		.left_join(se)
		.on(mpd.stock_entry == se.name)
		.where(mpd.stock_entry.isnotnull())
	)
	
	# Apply filters
	if filters.get("asset"):
		query = query.where(mpd.machine_no == filters.get("asset"))
	
	if filters.get("company"):
		query = query.where(se.company == filters.get("company"))
	
	if filters.get("from_date"):
		query = query.where(mpd.date >= filters.get("from_date"))
	
	if filters.get("to_date"):
		query = query.where(mpd.date <= filters.get("to_date"))
	
	# Order by machine_no ascending
	query = query.orderby(mpd.machine_no, order=frappe.qb.asc)
	
	# Execute query
	data = query.run(as_dict=True)
	
	return data