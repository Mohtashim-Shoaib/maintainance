// Copyright (c) 2025, mohtashim and contributors
// For license information, please see license.txt

frappe.query_reports["Asset Report"] = {
	"filters": [
		{
			"fieldname": "asset",
			"label": __("Asset"),
			"fieldtype": "Link",
			"options": "Asset",
			"reqd": 0
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 0
		}
	]
};
