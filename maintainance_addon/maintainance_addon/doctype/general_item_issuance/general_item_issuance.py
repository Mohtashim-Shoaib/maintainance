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
		self.set_check()

	
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


	# def set_remarks(self):
	# 	if self.qty_to_provided == 0:
	# 		self.remarks = "In Progress"
	# 	elif self.qty_to_provided < self.total_requested:
	# 		self.remarks = "Completed"
	# 	# elif self.total_issued == 0 and self.total_requested > 0:
	# 	# 	self.remarks = "Draft"


	# def set_title(self):
	# 	title = self.remarks
	# 	self.title = 
	
	def set_remarks(self):
		# if self.qty_to_provided == 0;
		# 	self.sta
		if self.total_issued == 0:
			self.remarks = "Draft"
		elif self.total_issued == self.total_requested:
			self.remarks = "Completed"
		else:
			# self.total_issued > 1
			self.remarks = "In Progress"
		# elif self.total_issued < self.total_requested:
		# 	self.remarks = "In Progress"

	def set_title(self):
		title = self.remarks if self.remarks is not None else "No Remarks"
		self.title = title

	def set_check(self):
		pass
		# for i in self.general_item_issuance_ct:
		# 	if i.qty > i.balance_qty:
		# 		i.check = 1
		# 	else:
		# 		i.check = 0



	def onload(self):
		# Assuming 'self.name' gives the document name
		doc = frappe.get_doc('General Item Issuance', self.name)
		if doc.docstatus != 1:
			self.update_balance_qty(self.name)

	@frappe.whitelist()
	def update_balance_qty(self, docname):
		doc = frappe.get_doc('General Item Issuance', docname)

		if doc.docstatus == 1:
			frappe.throw('Cannot update balance quantity after submission.')
			return

		changes_made = False
		for item in doc.general_item_issuance_ct:
			item_code = item.part_name
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