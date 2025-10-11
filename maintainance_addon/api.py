
import frappe

@frappe.whitelist(allow_guest=True)
def get_available_qty(item_code):
	try:
		actual_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty","item_code","warehouse")
		frappe.response["message"] = actual_qty
	except Exception as e:
		frappe.log_error(f"Error getting available qty for {item_code}: {e}", "get_available_qty")

@frappe.whitelist()
def get_related_documents_for_asset(asset_name):
	"""
	Get all related documents for an Asset based on machine number from machine_part_details
	"""
	try:
		# Simple test - just return the asset name and some test data
		print(f"API DEBUG: Getting related documents for asset: {asset_name}")
		
		# Test the query directly with all the fields you requested
		test_query = frappe.db.sql("""
			SELECT parent, name, item_code, machine_no, stock_entry FROM `tabMachine Part Details` WHERE machine_no = %s
		""", (asset_name,), as_dict=True)
		print(f"API DEBUG: Test query result: {test_query}")
		
		# Return the test data
		result = {
			"machine_part_issuances_count": len(test_query),
			"machine_part_issuance_rows": test_query,
			"maintenance_schedules_count": 0,
			"maintenance_schedule_rows": [],
			"work_orders_count": 0,
			"work_order_rows": [],
			"job_cards_count": 0,
			"job_card_rows": []
		}
		
		print(f"API DEBUG: Returning result: {result}")
		return result
		
	except Exception as e:
		print(f"API DEBUG: Error: {e}")
		import traceback
		traceback.print_exc()
		return {
			"machine_part_issuances_count": 0,
			"machine_part_issuance_rows": [],
			"maintenance_schedules_count": 0,
			"maintenance_schedule_rows": [],
			"work_orders_count": 0,
			"work_order_rows": [],
			"job_cards_count": 0,
			"job_card_rows": []
		}