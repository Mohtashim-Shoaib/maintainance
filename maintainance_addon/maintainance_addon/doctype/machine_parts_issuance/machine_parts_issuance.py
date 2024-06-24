# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MachinePartsIssuance(Document):
	def before_save(self):
		self.qty_to_provided()
		self.set_remarks()

	def on_save(self):
		self.qty_to_provided()
		self.set_remarks()

	def refresh(self):
		self.qty_to_be_provided()
		self.set_remarks()

	def validate(self):
		# self.qty_to_be_provided()
		self.set_remarks()

	def on_load(self):
		self.qty_to_provided()
		self.set_remarks()

	def qty_to_provided(self):
		pass
		# total_qty = self.total_issued_item + self.total_requested_item
		# qty_to_be_provided = self.total_requested_item - self.total_issued_item 
		# # frappe.errprint(f"Total Items are: {total_qty}")
		# # frappe.errprint(f"Qty to be provided: {qty_to_be_provided}")
		# self.db_set('qty_to_be_provided',qty_to_be_provided)
		# update_items = frappe.db.get_value('Machine Parts Issuace', self.name, 'qty_to_be_provided')
		# frappe.errprint(update_items)

		# setting remarks 

	def set_remarks(self):
		pass
		# total_qty = self.total_issued_item + self.total_requested_item
		# qty_to_be_provided = self.total_requested_item - self.total_issued_item
		# if self.total_issued_item == 0:
		# 	self.status = "Draft"
		# elif self.total_issued_item == self.total_requested_item:
		# 	self.status = "Completed"
		# elif self.total_issued_item < self.total_requested_item:
		# 	self.status = "In Progress"