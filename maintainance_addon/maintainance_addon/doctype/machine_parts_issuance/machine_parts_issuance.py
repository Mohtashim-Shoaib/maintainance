# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MachinePartsIssuance(Document):
	def on_load(self):
		self.qty_to_provided()
		self.calculate_total()
		self.set_status()
		# self.send_data_from_mpi_to_si()

	def send_data_from_mpi_to_si(self):
		try:
			frappe.errprint("Starting send_data_from_mpi_to_si")

			stock_entry_item = []
			for item in self.machine_part_details:
				stock_entry_item.append({
					'item_code': item.item_code,
					'qty': item.issued_qty,
					's_warehouse': "Stores - SAH",
					# 'basic_rate': item.rate,
					# 'warehouse': item.warehouse
				})
			stock_entry = frappe.get_doc({
				"doctype":"Stock Entry",
				'purpose': 'Material Transfer',
				'posting_date': self.date,
				'stock_entry_type': 'Material Issue',
				'items': stock_entry_item
			})
			stock_entry.insert()
			stock_entry.save()
			frappe.errprint("Stock Entry created successfully")
		except Exception as e:
			frappe.errprint(f"Error in send_data_from_mpi_to_si: {e}")

	def on_submit(self):
		self.send_data_from_mpi_to_si()

	def validate(self):
		self.qty_to_provided()
		self.set_status()
		self.send_data_from_mpi_to_si()

	def after_save(self):
		self.qty_to_provided()
		self.send_data_from_mpi_to_si()
		
	def calculate_total(self):
		total = 0
		for item in self.requested_items:
			total += item.request_quantity
		self.requested_qty = total


	def qty_to_provided(self):
		qty_to_be_provided = self.requested_qty - self.issued_qty
		# qty_to_be_provided = self.total_requested_item - self.total_issued_item 
		self.db_set('qty_to_be_provided',qty_to_be_provided)

	def set_status(self):
		# pass
			if self.total_issued_item == 0:
				self.status = "Draft"
			elif self.total_issued_item < self.total_requested_item:
				self.status = "In Progress"
			elif self.qty_to_be_provided == 0:
				self.status = "Completed"
			title = self.status
			self.db_set('title', title)


	def onload(self):
		# Assuming 'self.name' gives the document name
		doc = frappe.get_doc('Machine Parts Issuance', self.name)
		if doc.docstatus != 1:
			self.update_balance_qty(self.name)



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
	
	def validate(self):
		# Initialize dictionaries for requested and balance quantities
		requested_quantities = {}
		balance_quantities = {}

		# Populate dictionaries with total request and balance quantities for each item
		for item in self.requested_items:
			item_code = item.item_code
			# Update requested quantities
			if item_code in requested_quantities:
				requested_quantities[item_code] += item.request_quantity
			else:
				requested_quantities[item_code] = item.request_quantity
			# Update balance quantities
			if item_code in balance_quantities:
				balance_quantities[item_code] += item.balance_qty
			else:
				balance_quantities[item_code] = item.balance_qty

		# Validate issued quantities against requested and balance quantities
		for detail in self.machine_part_details:
			item_code = detail.item_code
			issued_qty = detail.issued_qty  # Assuming detail.issued_qty is already an integer
			# Get the total requested and balance quantity for the item, defaulting to 0 if not found
			total_requested_qty = requested_quantities.get(item_code, 0)
			total_balance_qty = balance_quantities.get(item_code, 0)

			# Check if issued quantity exceeds requested quantity
			if issued_qty > total_requested_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than requested quantity ({total_requested_qty}).")
			# Check if issued quantity exceeds balance quantity
			if issued_qty > total_balance_qty:
				frappe.throw(f"Item {item_code}: Issued quantity ({issued_qty}) cannot be greater than balance quantity ({total_balance_qty}).")