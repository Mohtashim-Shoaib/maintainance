import frappe
from frappe.model.document import Document

class RequestForm(Document):

	def before_save(self):
		pass

	def validate(self):
		# if self.is_new():
			self.send_data_from_request_form_to_part()
			# self.send_data_from_request_form_to_material_request()
			self.send_data_from_request_form_to_general()

	# def onload(self):
	# 	self.set_status()

	

	def send_data_from_request_form_to_part(self):
		try:
			part_issuance_items = []
			for item in getattr(self, 'items', []):
				part_issuance_items.append({
						'item_code': item.item_code,
						'item_name': item.item_code,
						'requested_qty': item.qty,
						'request_quantity': item.qty,
						'remarks': item.remarks,
						'balance_qty': item.balance_qty
					})

			if part_issuance_items:
				general_item = frappe.get_doc({
						'doctype': 'Machine Parts Issuance',
						'date': self.posting_date,
						"user": self.request_by,
						"by_hand": "ABDUL REHMAN",
						"requested_items": part_issuance_items,
					})     
				general_item.insert(ignore_permissions=True)
				general_item.save()
				self.db_set('part_request', general_item.name)
				self.db_set('part_request_form', general_item.name)
		except Exception as e:
			frappe.log_error(f"Error in send_data_from_request_form_to_part: {e}", "RequestForm send_data_from_request_form_to_part")

	def send_data_from_request_form_to_general(self):
		try:
			general_item_issuance = []
			for item in getattr(self, 'item', []):
				general_item_issuance.append({
						'part_name': item.item_code,
						'qty': item.qty,
						'remarks': item.remarks,
						'balance_qty': item.balance_qty
					})

				general_item = frappe.get_doc({
						'doctype': 'General Item Issuance',
						'date': self.posting_date,
						"user": self.request_by,
						"by_hand": "ABDUL REHMAN",
						"general_item_issuance_ct": general_item_issuance
					})     
				general_item.insert(ignore_permissions=True)
				general_item.save()
				self.db_set('general_request_form', general_item.name)

		except Exception as e:
		 	frappe.log_error(f"Error in send_data_from_request_form_to_general: {e}", "RequestForm send_data_from_request_form_to_general")

# def send_data_from_request_form_to_material_request(self):
# 		try:
# 			material_request_items = []
# 			for item in getattr(self, 'items', []) + getattr(self, 'item', []):
# 				if item.balance_qty == 0:
# 					material_request_items.append({
# 						'item_code': item.item_code,
# 						'qty': item.qty,
# 						'schedule_date': self.posting_date,
# 						'uom': frappe.db.get_value('Item', item.item_code, 'stock_uom'),
# 					})

# 			if material_request_items:
# 				material_request = frappe.get_doc({
# 					'doctype': 'Material Request',
# 					'material_request_type': 'Purchase',
# 					'transaction_date': self.posting_date,
# 					'set_warehouse': 'Stores - SAH',
# 					'items': material_request_items,
# 					'title': f"Material Request for {self.name}",
# 				})
# 				material_request.insert(ignore_permissions=True)
# 				material_request.save()
# 				frappe.msgprint("Material Request created!")
# 		except Exception as e:
# 			frappe.log_error(f"Error in send_data_from_request_form_to_material_request: {e}", "RequestForm send_data_from_request_form_to_material_request")

# @frappe.whitelist()
# def get_available_qty(item_code):
# 	try:
# 		actual_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty")
# 		frappe.response["message"] = actual_qty
# 	except Exception as e:
# 		frappe.log_error(f"Error getting available qty for {item_code}: {e}", "get_available_qty")


@frappe.whitelist()
def get_available_qty(item_code):
    try:
        actual_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty")
        return actual_qty
    except Exception as e:
        frappe.log_error(f"Error getting available qty for {item_code}: {e}", "get_available_qty")
        return None
