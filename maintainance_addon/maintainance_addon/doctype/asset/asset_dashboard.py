from frappe import _


def get_data(data=None):
	return {
		"non_standard_fieldnames": {
			"Asset Movement": "asset",
		},
		"internal_links": {
			"Machine Parts Issuance": ["machine_part_details", "machine_no"],
		},
		"transactions": [
			{"label": _("Movement"), "items": ["Asset Movement"]},
			{"label": _("Parts Issuance"), "items": ["Machine Parts Issuance"]}
		],
	}
