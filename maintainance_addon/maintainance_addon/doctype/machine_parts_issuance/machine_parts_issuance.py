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
		self.set_status()

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
		
	def set_status(self):
		if self.total_issued_item == 0:
			self.status = "Draft"
		elif self.total_issued_item < self.total_requested_item:
			self.status = "In Progress"
		elif self.qty_to_be_provided == 0:
			self.status = "Completed"
		# title = self.status
		# self.db_set('title', title)


	def onload(self):
		# Assuming 'self.name' gives the document name
		doc = frappe.get_doc('Machine Parts Issuance', self.name)
		if doc.docstatus != 1:
			self.update_balance_qty(self.name)

	# @frappe.whitelist()
	# def update_balance_qty(self, docname):
	# 	doc = frappe.get_doc('Machine Parts Issuance', docname)

	# 	if doc.docstatus == 1:
	# 		frappe.throw('Cannot update balance quantity after submission.')
	# 		return

	# 	changes_made = False
	# 	for item in doc.requested_items:
	# 		item_code = item.item_code
	# 		bin_doc = frappe.get_doc('Bin', {'item_code': item_code})
	# 		balance_qty = bin_doc.actual_qty

	# 		if item.balance_qty != balance_qty:
	# 			item.balance_qty = balance_qty
	# 			changes_made = True

	# 	if changes_made:
	# 		try:
	# 			doc.save()
	# 		except frappe.DocstatusTransitionError:
	# 			frappe.msgprint('Document status has changed, please reload and try again.')


	@frappe.whitelist()
	def update_balance_qty(self, docname):
		doc = frappe.get_doc('Machine Parts Issuance', docname)

		if doc.docstatus == 1:
			frappe.throw('Cannot update balance quantity after submission.')
			return

		changes_made = False
		for item in doc.requested_items:
			item_code = item.item_code
			# Check if Bin exists for the item_code
			bin_exists = frappe.db.exists('Bin', {'item_code': item_code})
			if not bin_exists:
				# frappe.msgprint(f'Bin for item_code {item_code} not found. Skipping update for this item.')
				continue  # Skip this item and continue with the next one

			bin_doc = frappe.get_doc('Bin', {'item_code': item_code})
			balance_qty = bin_doc.actual_qty

			if item.balance_qty != balance_qty:
				item.balance_qty = balance_qty
				changes_made = True

		if changes_made:
			try:
				doc.save()
			except frappe.DocstatusTransitionError:
				frappe.msgprint('Document status has changed, please reload and try again.')