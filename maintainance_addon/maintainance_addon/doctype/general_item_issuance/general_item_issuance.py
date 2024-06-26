# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GeneralItemIssuance(Document):
	def validate(self):
		self.calculate_total_requested()
		self.calculate_total_issuance()
		self.set_remarks()
		self.calculate_qty_to_provided()
		self.set_title()

	def calculate_total_requested(self):
		total_quantity = 0
		for item in self.general_item_issuance_ct:
			total_quantity += item.qty
		self.total_requested = total_quantity

	def calculate_total_issuance(self):
		total_quantity = 0
		for item in self.general_item_request_ct:
			total_quantity += item.qty
		self.total_issued = total_quantity

	def calculate_qty_to_provided(self):  # Method renamed here
		qty_to_provided = self.total_requested - self.total_issued
		self.qty_to_provided = qty_to_provided
        # frappe.errprint(f"Qty to be provided: {qty_to_provided}")
        # frappe.db_set('qty_to_provided', qty_to_provided)


	def set_remarks(self):
		if self.total_requested == self.total_issued:
			self.remarks = "Completed"
		elif self.total_requested > self.total_issued:
			self.remarks = "In Progress"
		elif self.total_requested < self.total_issued:
			self.remarks = "Draft"

	def set_title(self):
		title = self.remarks
		self.title = title