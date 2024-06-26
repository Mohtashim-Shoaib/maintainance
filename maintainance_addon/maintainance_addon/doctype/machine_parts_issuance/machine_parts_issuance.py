# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MachinePartsIssuance(Document):
	def before_save(self):
		self.qty_to_provided()

	def on_save(self):
		self.qty_to_provided()

	def refresh(self):
		self.qty_to_be_provided()

	def validate(self):
		self.qty_to_provided()

	def on_load(self):
		self.qty_to_provided()

	def validate(self):
		self.qty_to_provided()

	def after_save(self):
		self.qty_to_provided()

	def qty_to_provided(self):
		# Inside the qty_to_provided method, before the subtraction operation
		if self.total_requested_item is None:
			self.total_requested_item = 0.0

		if self.total_issued_item is None:
			self.total_issued_item = 0.0
		qty_to_be_provided = self.total_requested_item - self.total_issued_item
		# qty_to_be_provided = self.total_requested_item - self.total_issued_item 
		self.db_set('qty_to_be_provided',qty_to_be_provided)
		# frappe.db.commit()
		if qty_to_be_provided == 0:
			self.status = "Completed"
		elif qty_to_be_provided < self.total_requested_item:
			self.status = "In Progress"
		elif qty_to_be_provided == self.total_requested_item:
			self.status = "Draft"
		title = self.status
		self.db_set('title', title)
