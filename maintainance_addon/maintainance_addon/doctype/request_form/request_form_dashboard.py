from frappe import _

def get_data():
    return {
        "fieldname": "custom_request_form",  # Primary link field for Material Request
        "non_standard_fieldnames": {  # Use this for fields that are not the main link
            "General Item Issuance": "request_form",  # Ensure this is the correct field
            "Machine Parts Issuance": "request_form",  # Ensure this is the correct field
        },
        "internal_links": {
            "Material Request": ["items", "material_request"],  # This is working
        },
        "transactions": [
            {
                "label": _("Reference"),
                "items": ["Material Request", "General Item Issuance", "Machine Parts Issuance"],  # Include both
            },
        ],
    }
