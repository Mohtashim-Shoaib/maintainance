# # Copyright (c) 2024, mohtashim and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MachinePartsIssuance(Document):
	def before_update_after_submit(self):
		self.calculate_requested_total()
		self.calculate_issued_total()
		self.qty_to_provided()
		self.set_status()
		self.update_balance_qty()
		self.conditions()
		self.update_status()
		# self.send_data_from_mpi_to_si()
		self.send_data_from_mpi_to_si()
		# self.stock_reversal_entry()

	def validate(self):
		self.calculate_requested_total()
		self.calculate_issued_total()
		self.qty_to_provided()
		self.set_status()
		self.update_balance_qty()
		self.conditions()
		# self.send_data_from_mpi_to_si()

	def after_submit(self):
		self.update_balance_qty()
		# self.send_data_from_mpi_to_si()
	
	def on_submit(self):
		frappe.logger().info("Running on_submit method")
		# self.send_data_from_mpi_to_si()
	
	def on_cancel(self):
		if self.stock_entry:
			stock_entry_name = frappe.get_doc('Stock Entry', self.stock_entry)
			if stock_entry_name.docstatus == 1:
				stock_entry_name.cancel()
	
	

	def update_status(self):
		frappe.db.sql("""
		update `tabRequest Form`
				set status = %s,
				machine_parts_status = %s
				where name = %s
		""", (self.status, self.status, self.request_form))


	@frappe.whitelist(allow_guest=True)
	def calculate_requested_total(self):
		total = 0
		for item in self.requested_items:
			total += item.request_quantity
		self.total_requested_item = total
	
	@frappe.whitelist(allow_guest=True)
	def calculate_issued_total(self):
		total = 0
		for item in self.machine_part_details:
			total += item.issued_qty
		self.total_issued_item = total
	
	def qty_to_provided(self):
		if self.total_requested_item is not None and self.total_issued_item is not None:
			self.qty_to_be_provided = (self.total_requested_item - self.total_issued_item)
	
	def set_status(self):
		if self.qty_to_be_provided == 0:
			self.status = "Completed"
		elif self.total_issued_item < self.total_requested_item:
			self.status = "In Progress"
		elif self.qty_to_be_provided < 0:
			self.status = "Draft"

	def update_balance_qty(self):
		# if self.docstatus == 1:
		# 	frappe.throw('Cannot update balance quantity after submission.')
			# return
		for item in self.requested_items:
			item_code = item.item_code
			bin_exists = frappe.db.exists('Bin', {'item_code': item_code})
			if not bin_exists:
				continue
			bin_doc = frappe.get_doc('Bin', {'item_code': item_code})
			balance_qty = bin_doc.actual_qty
			item.balance_qty = balance_qty
			item.db_set('balance_qty', balance_qty)

	def conditions(self):
		requested_quantities = {}
		balance_quantities = {}
		for item in self.requested_items:
			item_code = item.item_code
			if item_code in requested_quantities:
				requested_quantities[item_code] += item.request_quantity
			else:
				requested_quantities[item_code] = item.request_quantity
			if item_code in balance_quantities:
				balance_quantities[item_code] += item.balance_qty
			else:
				balance_quantities[item_code] = item.balance_qty
		for detail in self.machine_part_details:
			item_code = detail.item_code
			issued_qty = detail.issued_qty
			total_requested_qty = requested_quantities.get(item_code, 0)
			total_balance_qty = balance_quantities.get(item_code, 0)
			if issued_qty > total_requested_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than requested quantity ({total_requested_qty}).")
			if issued_qty > total_balance_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than balance quantity ({total_balance_qty}).")

	def send_data_from_mpi_to_si(self):
		settings = frappe.get_single('Maintainance Addon Settings')
		m_type = settings.machine_part_stock_entry_type
		maintainance_addon_settings = frappe.get_single('Maintainance Addon Settings')
		# if self.total_issued_item == self.total_requested_item:
		if 1 == 1:
			try:
				frappe.errprint("Starting send_data_from_mpi_to_si")

				stock_entry_item = []
				for item in self.machine_part_details:
					if item.stock_entry_marked == 0:
						stock_entry_item.append({
							'item_code': item.item_code,
							'qty': item.issued_qty,
							's_warehouse': "Stores - SAH",
							'custom_machine_parts_issuance': self.name,
							'cost_center': maintainance_addon_settings.cost_center
							# 'basic_rate': item.rate,
							# 'warehouse': item.warehouse
						})
				stock_entry = frappe.get_doc({
					"doctype":"Stock Entry",
					# 'purpose': 'Material Transfer',
					'posting_date': self.date,
					'stock_entry_type': m_type,
					'items': stock_entry_item,
					'custom_cost_center': maintainance_addon_settings.cost_center
				})
				stock_entry.insert()
				stock_entry.save()
				stock_entry.submit()
				item.stock_entry = stock_entry.name 
				item.stock_entry_marked = 1

				# frappe.errprint("Stock Entry created successfully")
				# self.db_set('stock_entry', stock_entry.name)
			# except Exception as e:
				# frappe.errprint(f"Error in send_data_from_mpi_to_si: {e}")
			
			except Exception as e:
				frappe.errprint(f"Error in send_data_from_mpi_to_si: {e}")
		else:
			frappe.msgprint('test')
	
@frappe.whitelist(allow_guest=True)

def add_machine_part_row(docname, item_code, qty):
    doc = frappe.get_doc('Machine Parts Issuance', docname)

    if doc.docstatus != 1:
        frappe.throw("This operation is only allowed on submitted documents.")
    qty = float(qty)
    # Add a new row to the child table
    new_row = doc.append('machine_part_details', {
        'item_code': item_code,
        'issued_qty': qty
		# 'date': today
    })
   
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    
    return f"Added: {item_code} - {qty}"


@frappe.whitelist(allow_guest=True)
def close_document(docname):
    try:
        # Directly update the status to 'Closed'
        frappe.db.set_value('Machine Parts Issuance', docname, 'status', 'Closed')

        # Commit the changes to apply them immediately
        frappe.db.commit()

        return {'status': 'success', 'message': 'Document closed successfully.'}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Close Document Error')
        frappe.throw(_('An error occurred while closing the document: {0}').format(str(e)))
