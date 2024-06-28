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


	# def validate(self):
	# 	issued_quantities = {}
	# 	frappe.msgprint(1)
	# 	# Collecting issued quantities
	# 	for issuance in self.general_item_issuance_ct:
	# 		item_code = issuance.part_name  # Ensure this is the correct field name
	# 		frappe.errprint(issuance)
	# 		frappe.errprint("issuance")
	# 		if item_code in issued_quantities:
	# 			issued_quantities[item_code] += issuance.qty
	# 		else:
	# 			issued_quantities[item_code] = issuance.qty

	# 	# # Debugging: Print issued quantities to verify correct accumulation
	# 	frappe.errprint(f"Issued Quantities: {issued_quantities}")

	# 	for request in self.general_item_request_ct:
	# 		requested_item_code = request.item_code  # Ensure this matches the field name in your child table
	# 		issued_qty = issued_quantities.get(requested_item_code, 0)
	# 		if request.qty > issued_qty:
	# 			frappe.throw(f"You have selected an incorrect value for the item {requested_item_code}. Requested quantity ({request.qty}) cannot be greater than issued quantity ({issued_qty}).")


		
	# def validate(self):
	# 	issued_quantities = {}
	# 	# Collecting issued quantities
	# 	for issuance in self.general_item_issuance_ct:
	# 		item_code = issuance.part_name  # Ensure this is the correct field name
	# 		frappe.errprint(issuance)
	# 		if item_code in issued_quantities:
	# 			issued_quantities[item_code] += issuance.balance_qty
	# 		else:
	# 			issued_quantities[item_code] = issuance.balance_qty

	# 	# # Debugging: Print issued quantities to verify correct accumulation
	# 	frappe.errprint(f"Issued Quantities: {issued_quantities}")

	# 	for request in self.general_item_request_ct:
	# 		requested_item_code = request.item_code  # Ensure this matches the field name in your child table
	# 		issued_qty = issued_quantities.get(requested_item_code, 0)
	# 		if request.qty > issued_qty:
	# 			frappe.throw(f"You have selected an incorrect value for the item {requested_item_code}. Issue Qty quantity ({request.qty}) cannot be greater than balanced quantity ({issued_qty}).")

	def onload(self):
		self.calculate_total_requested()
		self.calculate_total_issued()

	def validate(self):
		self.calculate_total_requested()
		self.calculate_total_issued()

	def calculate_total_requested(self):
		total_quantity = 0
		for item in self.general_item_issuance_ct:
			total_quantity += item.qty
		self.total_requested = total_quantity

	def calculate_total_issued(self):
		total_quantity = 0
		for item in self.general_item_request_ct:
			total_quantity += item.qty
		self.total_issued = total_quantity

	
	def validate(self):
		# Initialize dictionaries for requested and balance quantities
		general_item_issuance_ct = {}
		balance_quantities = {}

		# Populate dictionaries with total request and balance quantities for each item
		for item in self.general_item_issuance_ct:
			item_code = item.part_name
			# Update requested quantities
			if item_code in general_item_issuance_ct:
				general_item_issuance_ct[item_code] += item.qty
			else:
				general_item_issuance_ct[item_code] = item.qty
			# Update balance quantities
			if item_code in balance_quantities:
				balance_quantities[item_code] += item.balance_qty
			else:
				balance_quantities[item_code] = item.balance_qty

		# Validate issued quantities against requested and balance quantities
		for detail in self.general_item_request_ct:
			item_code = detail.item_code
			issued_qty = detail.qty  # Assuming detail.issued_qty is already an integer
			# Get the total requested and balance quantity for the item, defaulting to 0 if not found
			total_requested_qty = general_item_issuance_ct.get(item_code, 0)
			total_balance_qty = balance_quantities.get(item_code, 0)

			# Check if issued quantity exceeds requested quantity
			if issued_qty > total_requested_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than requested quantity ({total_requested_qty}).")
			# Check if issued quantity exceeds balance quantity
			if issued_qty > total_balance_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than balance quantity ({total_balance_qty}).")