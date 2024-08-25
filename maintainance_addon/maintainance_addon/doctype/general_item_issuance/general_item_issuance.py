# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GeneralItemIssuance(Document):
	def validate(self):
		self.calculate_total_requested()
		self.calculate_total_issuance()
		self.set_qty_to_provided()
		self.set_remarks()
		self.update_balance_qty()
		self.condition()

	def on_submit(self):
		self.send_data_from_gii_to_si()
	
	def calculate_total_requested(self):
		total = 0
		for item in self.general_item_issuance_ct:
			total += item.qty
		self.total_requested = total
	
	def calculate_total_issuance(self):
		total = 0
		for item in self.general_item_request_ct:
			total += item.qty
		self.total_issued = total

	def set_qty_to_provided(self):
		if self.total_issued is not None and self.total_requested is not None:
			self.qty_to_provided = (self.total_requested - self.total_issued)
		# if self.total_issued == 0:
		# 	self.qty_to_provided = self.total_requested
	
	def set_remarks(self):
		if self.qty_to_provided == 0:
			self.status = "Completed"
		elif self.total_issued < self.total_requested:
			self.status = "In Progress"
		elif self.total_issued == 0:
			self.status = "Draft"
		
	def update_balance_qty(self):
		if self.docstatus == 1:
			frappe.throw('Cannot update balance quantity after submission.')
			return
		for item in self.general_item_issuance_ct:
			item_code = item.part_name
			bin_exists = frappe.db.exists('Bin', {'item_code': item_code})
			if not bin_exists:
				continue 
			bin_doc = frappe.get_doc('Bin', {'item_code': item_code})
			balance_qty = bin_doc.actual_qty
			item.balance_qty = balance_qty
			item.db_set('balance_qty', balance_qty)

	def condition(self):
			general_item_issuance_ct = {}
			balance_quantities = {}
			# total_quantity = 0
			# for item in self.general_item_issuance_ct:
			# 	total_quantity += item.qty
			# self.total_requested = total_quantity
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
		try:
			frappe.errprint("Starting send_data_from_mpi_to_si")
			stock_entry_item = []
			for item in self.general_item_request_ct:
				stock_entry_item.append({
					'item_code': item.item_code,
					'qty': item.qty,
					's_warehouse': "Stores - SAH",
					# 'basic_rate': item.rate,
					# 'warehouse': item.warehouse
				})
			stock_entry= frappe.get_doc({
				'doctype': 'Stock Entry',
				'posting_date': self.date,
				'stock_entry_type': 'Material Issue',
				# 'posting_time': self.posting_time,
				'from_warehouse': "Stores - SAH",
				# 'to_warehouse': "Work In Progress - SAH",
				'items': stock_entry_item
			})
			stock_entry.insert()
			stock_entry.save()
			stock_entry.submit()
			frappe.errprint('Stock Entry created Successfully')
			# frappe.errrint(item)
		except Exception as e:
			frappe.throw(f"Error in send_data_from_gii_to_si: {e}")