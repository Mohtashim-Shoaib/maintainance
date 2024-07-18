
# import frappe

# @frappe.whitelist(allow_guest=True)
# def get_available_qty(item_code):
# 	try:
# 		actual_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty","item_code","warehouse")
# 		frappe.response["message"] = actual_qty
# 	except Exception as e:
# 		frappe.log_error(f"Error getting available qty for {item_code}: {e}", "get_available_qty")

    # try:
    #     actual_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty")
	# 	frappe.response["message"] = actual_qty
	# except Exception as e:
	# 	frappe.log_error(f"Error getting available qty for {item_code}: {e}", "get_available_qty")