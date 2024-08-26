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
		# self.status()
	
	# def status(self):
	# 	machine_part_doc = frappe.get_doc("Machine Parts Issuance", self.part_request)
	# 	machine_part_qty = machine_part_doc.qty_to_be_provided
	# 	general_item_doc = frappe.get_doc('General Item Issuance', self.general_request_form)
	# 	general_item_qty = general_item_doc.qty_to_provided
	# 	if machine_part_doc:
	# 		if machine_part_qty == 0:
	# 			self.status = "Complete"
	# 		elif machine_part_qty != 0:
	# 			self.status = "In Progress"
	# 		else:
	# 			self.status = "Draft"
	# 	if general_item_doc:
	# 		if general_item_qty == 0:
	# 			self.status = "Complete"
	# 		elif general_item_qty != 0:
	# 			self.status = "In Progress"
	# 		else:
	# 			self.status = "Draft"
	# 	if machine_part_qty is not None and general_item_doc is not None:
	# 		if machine_part_qty == 0 and general_item_qty == 0:
	# 			self.status = "Complete"
	# 		elif machine_part_qty != 0 and general_item_qty == 0:
	# 			self.status = "In Progress"
	# 		elif machine_part_qty == 0 and general_item_qty != 0:
	# 			self.status = "In Progress"
	# 		else:
	# 			self.status = "Draft"
		
	
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
