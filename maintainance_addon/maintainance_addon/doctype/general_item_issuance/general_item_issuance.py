# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GeneralItemIssuance(Document):
	def validate(self):
		self.calculate_total_requested()
		self.calculate_total_issuance()
		# self.set_remarks()
		self.set_title()
		self.set_check()
		self.set_qty_to_provided()
		self.test1()
		self.my_python_method()

	def test1(self):
		frappe.msgprint("testing./././")
	
	def on_submit(self):
		self.send_data_from_gii_to_si()


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
			frappe.errprint('Stock Entry created Successfully')
			# frappe.errrint(item)
		except Exception as e:
			frappe.throw(f"Error in send_data_from_gii_to_si: {e}")

	@frappe.whitelist()
	def my_python_method(self):
		frappe.msgprint('This is a message from Python')

	def onload(self):
		self.calculate_total_requested()
		self.calculate_total_issuance()
		# self.set_remarks()
		self.set_status()
	def set_qty_to_provided(self):
		try:
			total_requested = float(self.total_requested)  if self.total_requested else 0
			total_issued = float(self.total_issued)  if self.total_issued else 0
			self.qty_to_provided = total_requested - total_issued
		except ValueError as e:
			frappe.throw(f"Error in set_qty_to_provided: {e}")
		except Exception as e:
			frappe.throw(f"Unexpected error in set_qty_to_provided: {e}")
			


	def set_status(self):
		if self.total_issued == 0:
			self.remarks = "Draft"
		elif self.total_issued < self.total_requested:
			self.remarks = "In Progress"
		elif self.total_issued == self.total_requested:
			self.remarks = "Completed"

	# def set_remarks(self):
	# 	if self.total_issued == 0:
	# 		self.remarks = "Draft"
	# 	elif self.total_issued < self.total_requested:
	# 		self.remarks = "In Progress"
	# 	elif self.total_issued == self.total_requested:
	# 		self.remarks = "Completed"





	def calculate_total_requested(self):
		# frappe.msgprint('hello world')
		total_quantity = 0
		for item in self.general_item_issuance_ct:
			total_quantity += item.qty
		self.total_requested = total_quantity

	def calculate_total_issuance(self):
		total_quantity = 0
		for item in self.general_item_request_ct:
			total_quantity += item.qty
		self.total_issued = total_quantity
		
	

	# def before_save(self):
	# 	self.set_remarks() 
	# 	# self.save()
	# def validate(self):
	# 	self.set_remarks()
	# def onload(self):
	# 	self.set_remarks()
	
	# def set_remarks(self):
	# 	pass
		# frappe.errprint(f"Total Issued: {self.total_issued}, Total Requested: {self.total_requested}")  # Debugging print
		# # if self.total_issued < self.total_requested:
		# # 	self.remarks = "In Progress"
		# if self.qty_to_provided == 0:
		# 	self.remarks = "Completed"
		# elif self.total_issued ==0 :
		# 	self.remarks = "Draft"
		# frappe.errprint(f"Remarks set to: {self.remarks}")  # Debugging print
		# self.save()


	def set_title(self):
		title = self.remarks if self.remarks is not None else "No Remarks"
		self.title = title
	def onload(self):
		self.test()

	def test(self):
		frappe.msgprint('test')

	def onload(self):
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
			bin_doc = frappe.db.get_value('Bin', {'item_code': item_code}, '*', as_dict=True)
			if not bin_doc:
				frappe.msgprint(f'Bin for item_code {item_code} not found. Skipping update for this item.')
				continue

			balance_qty = bin_doc.actual_qty
			if item.balance_qty != balance_qty:
				item.balance_qty = balance_qty
				changes_made = True

		if changes_made:
			try:
				doc.save()
				frappe.msgprint('Balance quantities updated successfully.')
			except Exception as e:
				frappe.log_error(f'Error saving document: {str(e)}', 'Update Balance Quantity Error')
				frappe.msgprint('An error occurred while saving the document. Please check the error log for details.')


	# def onload(self):
	# 	# Assuming 'self.name' gives the document name
	# 	doc = frappe.get_doc('General Item Issuance', self.name)
	# 	if doc.docstatus != 1:
	# 		self.update_balance_qty(self.name)

	# @frappe.whitelist()
	# def update_balance_qty(self, docname):
	# 	frappe.msgprint('Document status has changed, please reload and try again.')
	# 	doc = frappe.get_doc('General Item Issuance', docname)

	# 	if doc.docstatus == 1:
	# 		frappe.throw('Cannot update balance quantity after submission.')
	# 		return

	# 	changes_made = False
	# 	for item in doc.general_item_issuance_ct:
	# 		item_code = item.part_name
	# 		bin_exists = frappe.db.exists('Bin', {'item_code': item_code})
	# 		if not bin_exists:
	# 			frappe.msgprint(f'Bin for item_code {item_code} not found. Skipping update for this item.')
	# 			continue  # Skip this item and continue with the next one

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
		frappe.msgprint("1")
		total_quantity = 0
		for item in self.general_item_issuance_ct:
			total_quantity += item.qty
		self.total_requested = total_quantity

	def validate(self):
		frappe.msgprint("2")
	def calculate_total_issued(self):
		# pass
		total_quantity = 0
		for item in self.general_item_request_ct:
			total_quantity += item.qty
		self.total_issued = total_quantity
		
	def onload(self):
		total_quantity = 0
		for item in self.general_item_request_ct:
			total_quantity += item.qty
		self.total_issued = total_quantity
		# frappe.msgprint('hello')
		# qty_to_provided = self.total_requested - self.total_issued
		# self.qty_to_provided = qty_to_provided
		
	
	def validate(self):
		total_quantity = 0
		for item in self.general_item_issuance_ct:
			total_quantity += item.qty
		self.total_requested = total_quantity
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