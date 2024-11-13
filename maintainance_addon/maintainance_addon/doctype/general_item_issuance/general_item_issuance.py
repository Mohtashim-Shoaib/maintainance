# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document

class GeneralItemIssuance(Document):
	def before_update_after_submit(self):
		self.calculate_total_requested()
		self.calculate_total_issuance()
		self.set_qty_to_provided()
		# self.set_remarks()
		self.set_remarks()
		self.update_balance_qty()
		self.condition()
		self.update_status()
		self.send_data_from_gii_to_si()

	def on_cancel(self):
		pass

	def validate(self):
		self.calculate_total_requested()
		self.update_balance_qty()
		self.calculate_total_issuance()
		self.set_qty_to_provided()
		self.set_remarks()

	# def on_submit(self):
	# 	self.send_data_from_gii_to_si()
	
	def update_status(self):
		try:
			frappe.db.sql("""UPDATE `tabRequest Form`
				SET status = %s,
					general_item_status = %s
				WHERE name = %s""", (self.status, self.status, self.request_form))
			frappe.db.commit()  # Ensure the changes are committed
			
		except Exception as e:
			frappe.log_error(message=str(e), title='Update Status Error')

	
	def calculate_total_requested(self):
		total = 0
		for item in self.general_item_issuance_ct:
			total += item.qty
		self.total_requested = total
	
	def calculate_total_issuance(self):
		total = 0
		for item in self.general_item_request_ct:
			total += item.qty if item.qty else 0
		self.total_issued = total

	def set_qty_to_provided(self):
		if self.total_issued is not None and self.total_requested is not None:
			self.qty_to_provided = (self.total_issued - self.total_requested)
	
	def set_remarks(self):
		if self.qty_to_provided == 0:
			self.status = "Completed"
		elif self.total_issued < self.total_requested:
			self.status = "In Progress"
		elif self.total_issued == 0:
			self.status = "Draft"
	
	def update_balance_qty(self):
		for item in self.general_item_issuance_ct:
			item_code = item.part_name
			bin_exists = frappe.db.exists('Bin',{'item_code':item_code})
			if not bin_exists:
				continue
			bin_doc = frappe.get_doc('Bin',{'item_code':item_code})
			balance_qty = bin_doc.actual_qty
			item.balance_qty = balance_qty
			item.db_set('balance_qty', balance_qty)

	def condition(self):
		general_item_issuance_ct = {}
		balance_quantities = {}
		for item in self.general_item_issuance_ct:
			item_code = item.part_name
			if item_code in general_item_issuance_ct:
				general_item_issuance_ct[item_code] += item.qty
			else:
				general_item_issuance_ct[item_code] = item.qty
			if item_code in balance_quantities:
				balance_quantities[item_code] += item.balance_qty
			else:
				balance_quantities[item_code] = item.balance_qty
		for detail in self.general_item_request_ct:
			item_code = detail.item_code
			issued_qty = detail.qty 
			total_requested_qty = general_item_issuance_ct.get(item_code, 0)
			total_balance_qty = balance_quantities.get(item_code, 0)
			if issued_qty > total_requested_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than requested quantity ({total_requested_qty}).")
			if issued_qty > total_balance_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than balance quantity ({total_balance_qty}).")

	def send_data_from_gii_to_si(self):
		if 1 == 1:  # This should ideally be a meaningful condition, like self.docstatus == 1
			try:
				frappe.errprint("Starting send_data_from_mpi_to_si")
				stock_entry_item = []
				
				# Collect items for Stock Entry
				for item in self.general_item_request_ct:
					if item.stock_entry_marked == 0:
						stock_entry_item.append({
							'item_code': item.item_code,
							'qty': item.qty,
							's_warehouse': "Stores - SAH",
						})

				if not stock_entry_item:
					frappe.errprint("No valid stock entry items to create")
					return

				# Create Stock Entry
				stock_entry = frappe.get_doc({
					'doctype': 'Stock Entry',
					'posting_date': self.date,
					'stock_entry_type': 'Material Issue',
					'from_warehouse': "Stores - SAH",
					'items': stock_entry_item
				})
				stock_entry.insert()
				stock_entry.submit()

				# Set stock entry name for relevant items
				for item in self.general_item_request_ct:
					if item.stock_entry_marked == 0:
						item.stock_entry = stock_entry.name
						item.stock_entry_marked = 1
				
				# Save stock entry reference in the main document
				self.db_set('stock_entry', stock_entry.name)
			
			except Exception as e:
				frappe.throw(f"Error in send_data_from_gii_to_si: {e}")
	# def add_general_part_row(self, item_code, qty):
	# 	new_row = self.append('general_item_request_ct', {})
	# 	new_row.item_code = item_code
	# 	new_row.qty = qty
	# 	new_row.is_new = True  # Mark as new
	# 	self.save(ignore_permissions=True)
	# 	frappe.db.commit()

# @frappe.whitelist(allow_guest=True)
# def add_general_part_row(docname, item, qty):
# 	doc = frappe.get_doc('General Item Issuance', docname)
# 	if doc.docstatus != 1:
# 		frappe.throw('This operation is only valid for submitted Documents')
# 	qty = float(qty)
# 	new_row = doc.append('general_item_request_ct',{
# 		'item_code':item,
# 		'qty':qty,
# 		'is_new': True
# 	})
# 	# doc.save(ignore_permission=True)
# 	doc.save(ignore_permissions=True)
# 	frappe.db.commit()
# 	return f"Added {item} - {qty}"
	
	
@frappe.whitelist(allow_guest=True)
def add_general_part_row(docname, item, qty):
    try:
        doc = frappe.get_doc('General Item Issuance', docname)
        
        if doc.docstatus != 1:
            frappe.throw('This operation is only valid for submitted documents')
        
        qty = float(qty)
        # doc.add_general_part_row(item, qty)
        # Use the doctype method to add the row
        # doc.add_general_part_row(item, qty)

        new_row = doc.append('general_item_request_ct', {
        'item_code': item,
        'qty': qty
		# 'date': today
    	})
		# Save and commit the document
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Return success message
        return f"Added {item} - {qty}"

    except Exception as e:
        frappe.log_error(f"Error in add_general_part_row: {e}", "Add General Part Row")
        frappe.throw(f"Error occurred: {e}")
