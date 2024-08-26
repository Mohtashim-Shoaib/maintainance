import frappe
from frappe.model.document import Document

class RequestForm(Document):

	def on_submit(self):
		self.send_data_from_request_form_to_part()
		self.send_data_from_request_form_to_general()

	def validate(self):
		self.send_data_from_request_form_to_material_request()
		self.calculation_of_child_table()
		self.calculation_of_child_table1()
		# self.update_status()
	
# 	def update_status(self):
# 		if self.docstatus == 1:
# 			self.status = "Draft"

# 			# Check if `self.general_request_form` is not None and fetch the document
# 			if not self.material_request:
# 				if self.general_request_form:
# 					try:
# 						general_doc = frappe.get_doc('General Item Issuance', self.general_request_form)
# 						if general_doc.status == "Completed":
# 							self.status = "Completed"
# 						elif general_doc.status == "In Progress":
# 							self.status = "In Progress"
# 						else:
# 							self.status = "Draft"
# 					except frappe.DoesNotExistError:
# 						frappe.msgprint(f"General Item Issuance '{self.general_request_form}' not found.")
# 				else:
# 					frappe.msgprint("No General Item Issuance request specified.")

# # Check if `self.part_request` is not None and fetch the document
# 			# Check if `self.part_request` is not None and fetch the document
# 			if not self.material_request:
# 				if self.part_request:
# 					try:
# 						part_request_doc = frappe.get_doc('Machine Parts Issuance', self.part_request)
# 						if part_request_doc.status == "Completed":
# 							self.status = "Completed"
# 						elif part_request_doc.status == "In Progress":
# 							self.status = "In Progress"
# 						else:
# 							self.status = "Draft"
# 					except frappe.DoesNotExistError:
# 						frappe.msgprint(f"Machine Parts Issuance '{self.part_request}' not found.")
# 				else:
# 					frappe.msgprint("No Machine Parts Issuance request specified.")




		
		
	
	def calculation_of_child_table(self):
		total = 0
		for item in self.items:
			total += item.qty
		self.total_parts = total

	def calculation_of_child_table1(self):
		total1 = 0
		for item in self.item:
			total1 += item.qty
		self.total_general = total1
	
	def send_data_from_request_form_to_material_request(self):
		if self.docstatus == 1:
			try:
				material_request_items = []
				for item in getattr(self, 'items', []) + getattr(self, 'item', []):
					if item.balance_qty < item.qty:
						material_request_items.append({
							'item_code': item.item_code,
							'qty': (item.qty - item.balance_qty),
							'schedule_date': self.posting_date,
							'uom': frappe.db.get_value('Item', item.item_code, 'stock_uom'),
						})

				if material_request_items:
					material_request = frappe.get_doc({
						'doctype': 'Material Request',
						'material_request_type': 'Purchase',
						'transaction_date': self.posting_date,
						'set_warehouse': 'Stores - SAH',
						'items': material_request_items,
						'custom_request_form': self.name,
						'title': f"Material Request for {self.name}",
					})
					material_request.insert(ignore_permissions=True)
					material_request.save()
					self.db_set('material_request', material_request.name)
					frappe.msgprint("Material Request created!")
			except Exception as e:
				frappe.log_error(f"Error in send_data_from_request_form_to_material_request: {e}", "RequestForm send_data_from_request_form_to_material_request")


	def send_data_from_request_form_to_part(self):
		if self.total_parts > 0:
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
							"request_form": self.name
						})     
				general_item.insert(ignore_permissions=True)
				general_item.save()
				self.db_set('part_request', general_item.name)
				self.db_set('part_request_form', general_item.name)
			except Exception as e:
				frappe.log_error(f"Error in send_data_from_request_form_to_part: {e}", "RequestForm send_data_from_request_form_to_part")

	def send_data_from_request_form_to_general(self):
		if self.total_general > 0:
			try:
				general_item_issuance = []
				for item in self.item:
				# for item in getattr(self, 'item', []):
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
							"request_form": self.name,
							"general_item_issuance_ct": general_item_issuance
						})     
				general_item.insert(ignore_permissions=True)
				general_item.save()
				self.db_set('general_request_form', general_item.name)

			except Exception as e:
				frappe.log_error(f"Error in send_data_from_request_form_to_general: {e}", "RequestForm send_data_from_request_form_to_general")


@frappe.whitelist()
def get_available_qty(item_code):
    try:
        actual_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty")
        return actual_qty
    except Exception as e:
        frappe.log_error(f"Error getting available qty for {item_code}: {e}", "get_available_qty")
        return None
