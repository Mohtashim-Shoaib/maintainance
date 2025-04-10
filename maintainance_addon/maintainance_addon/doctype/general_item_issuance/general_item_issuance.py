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
		# self.close_document()

	def on_cancel(self):
		pass

	def validate(self):
		self.calculate_total_requested()
		self.update_balance_qty()
		self.calculate_total_issuance()
		self.set_qty_to_provided()
		self.set_remarks()
		self.update_status()
		# self.send_data_from_gii_to_si()

	def on_update_after_submit(self):
		# Update balance quantities
		self.update_balance_qty()
		self.send_data_from_gii_to_si()

		# Validate issuance conditions
		self.condition()
		self.update_status()

	
	def close_document(self):
		# frappe.throw("Function Started")  # Debugging message
		
		if self.status == "Closed":
			frappe.throw("Inside Closed Check")  # Debugging message
			
			request = frappe.get_doc("Request Form", self.request_form)
			
			if request:
				frappe.throw(f"Request Form Found: {self.request_form}")  # Debugging message
				
				request.status = "Closed"
				request.save()  # ✅ Save changes to Request Form
				
				frappe.db.commit()  # ✅ Commit changes
				
				frappe.msgprint("Request Form closed successfully.")
			else:
				frappe.throw("Request Form Not Found")
		else:
			frappe.throw("Status is not Closed")



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

	

   
	def condition(self):
		# Aggregate issued and balance quantities
		general_item_issuance_ct = {}
		balance_quantities = {}

		for item in self.general_item_issuance_ct:
			item_code = item.part_name

			# Accumulate issued quantity
			general_item_issuance_ct[item_code] = general_item_issuance_ct.get(item_code, 0) + item.qty

			# Track balance quantity correctly (pick lowest value encountered)
			if item_code not in balance_quantities:
				balance_quantities[item_code] = item.balance_qty
			else:
				balance_quantities[item_code] = min(balance_quantities[item_code], item.balance_qty)

		# Validate requested quantities against issued and balance
		for detail in self.general_item_request_ct:
			item_code = detail.item_code
			requested_qty = detail.qty
			issued_qty = general_item_issuance_ct.get(item_code, 0)
			total_balance_qty = balance_quantities.get(item_code, 0)

			# Validate that issued does not exceed requested
			if requested_qty > issued_qty:
				frappe.throw(f"Issued quantity ({issued_qty}) for item {item_code} exceeds the requested quantity ({requested_qty}).")

			# Validate that issued does not exceed available balance
			# if issued_qty > total_balance_qty:
			# 	frappe.throw(f"Issued quantity ({issued_qty}) for item {item_code} exceeds the available balance ({total_balance_qty}).")
	
	def update_balance_qty(self):
		for item in self.general_item_issuance_ct:
			item_code = item.part_name

			# Check if a Bin exists for the item
			bin_exists = frappe.db.exists('Bin', {'item_code': item_code})
			if not bin_exists:
				frappe.msgprint(f"Bin does not exist for Item Code: {item_code}")
				item.balance_qty = 0
				item.db_set('balance_qty', 0)
				continue

			# Fetch the Bin document
			bin_doc = frappe.get_doc('Bin', {'item_code': item_code})

			# Calculate new balance quantity
			# new_balance_qty = bin_doc.actual_qty - item.qty
			new_balance_qty = bin_doc.actual_qty

			# Update the balance quantity in the child table
			item.balance_qty = new_balance_qty
			item.db_set('balance_qty', new_balance_qty)


	def condition(self):
		# Aggregate issued and balance quantities
		general_item_issuance_ct = {}
		balance_quantities = {}

		for item in self.general_item_issuance_ct:
			item_code = item.part_name

			# Accumulate issued quantity
			general_item_issuance_ct[item_code] = general_item_issuance_ct.get(item_code, 0) + item.qty

			# Track balance quantity correctly (pick lowest value encountered)
			if item_code not in balance_quantities:
				balance_quantities[item_code] = item.balance_qty
			else:
				balance_quantities[item_code] = min(balance_quantities[item_code], item.balance_qty)

		# Validate requested quantities against issued and balance
		for detail in self.general_item_request_ct:
			item_code = detail.item_code
			requested_qty = detail.qty
			issued_qty = general_item_issuance_ct.get(item_code, 0)
			total_balance_qty = balance_quantities.get(item_code, 0)

			# Validate that issued does not exceed requested
			if requested_qty > issued_qty:
				frappe.throw(f"Issued quantity ({issued_qty}) for item {item_code} exceeds the requested quantity ({requested_qty}).")

			# Validate that issued does not exceed available balance
			# if issued_qty > total_balance_qty:
			# 	frappe.throw(f"Issued quantity ({issued_qty}) for item {item_code} exceeds the available balance ({total_balance_qty}).")

	def send_data_from_gii_to_si(self):
		if self.docstatus != 1:
			frappe.throw("Document must be submitted before sending data to Stock Entry")

		try:
			# Check if there are any unmarked items first
			unmarked_items = [item for item in self.general_item_request_ct if item.stock_entry_marked == 0]
			if not unmarked_items:
				frappe.msgprint("All items have already been processed")
				return

			# Get items from database (more reliable than UI cache)
			db_items = frappe.get_all(
				"General Item Request CT",
				filters={"parent": self.name, "stock_entry_marked": 0},
				fields=["name", "item_code", "qty", "stock_entry_marked", "stock_entry", "unit", "idx"],
				order_by="idx"
			)
			
			if not db_items:
				frappe.msgprint("No unprocessed items found")
				return

			# Prepare stock entry items
			stock_entry_items = []
			for item in db_items:
				stock_entry_items.append({
					'item_code': item.item_code,
					'qty': item.qty,
					's_warehouse': "Stores - SAH",
					'uom': item.unit or frappe.db.get_value("Item", item.item_code, "stock_uom") or "Nos",
					'conversion_factor': 1.0
				})

			# Create and submit stock entry
			stock_entry = frappe.get_doc({
				'doctype': 'Stock Entry',
				'posting_date': self.date or frappe.utils.nowdate(),
				'stock_entry_type': 'Material Issue',
				'items': stock_entry_items,
				'custom_general_item_issuance': self.name
			})
			
			stock_entry.insert(ignore_permissions=True)
			stock_entry.submit()

			# Update child records
			for item in db_items:
				frappe.db.set_value(
					"General Item Request CT",
					item.name,
					{
						'stock_entry_marked': 1,
						'stock_entry': stock_entry.name
					}
				)

			# Update parent document
			self.db_set('stock_entry', stock_entry.name)
			
			frappe.msgprint(f"Successfully created Stock Entry {stock_entry.name}")
			return stock_entry.name

		except Exception as e:
			frappe.log_error(
				title=f"Stock Entry Creation Error for {self.name}",
				message=frappe.get_traceback()
			)
			frappe.throw(f"Failed to create Stock Entry: {str(e)}")
	# def send_data_from_gii_to_si(self):
	# 	if self.docstatus != 1:
	# 		frappe.throw("Document must be submitted before sending data to Stock Entry")

	# 	try:
	# 		for item in self.general_item_request_ct:
	# 			if item.stock_entry_marked == 0:
			
	# 				# 2. Debug information
	# 				frappe.errprint(f"DEBUG: Processing document {self.name}")
	# 				frappe.errprint(f"DEBUG: DocStatus: {self.docstatus}")
	# 				frappe.errprint(f"DEBUG: Current stock_entry: {self.stock_entry}")

	# 				# 3. Get items from child table - using correct field name
	# 				child_items = self.get("general_item_request_ct") or []
	# 				frappe.errprint(f"DEBUG: Found {len(child_items)} items in child table (UI cache)")

	# 				# 4. Additional check - get from database directly
	# 				db_items = frappe.get_all(
	# 					"General Item Request CT",  # This is the Doctype name
	# 					filters={"parent": self.name},
	# 					fields=["name", "item_code", "qty", "stock_entry_marked", "stock_entry", "unit", "idx"],
	# 					order_by="idx"
	# 				)
	# 				frappe.errprint(f"DEBUG: Found {len(db_items)} items in database")

	# 				if not child_items and not db_items:
	# 					frappe.throw("No items found in the General Item Request CT table")

	# 				# 5. Process items
	# 				stock_entry_items = []
	# 				valid_items = 0
					
	# 				# Use database items if available, fallback to UI items
	# 				items_to_process = db_items if db_items else child_items
					
	# 				for item in items_to_process:
	# 					frappe.errprint(f"DEBUG: Processing item {getattr(item, 'idx', '?')} - {item.item_code}")
						
	# 					stock_entry_items.append({
	# 						'item_code': item.item_code,
	# 						'qty': item.qty,
	# 						's_warehouse': "Stores - SAH",
	# 						'uom': getattr(item, 'unit', None) or frappe.db.get_value("Item", item.item_code, "stock_uom") or "Nos",
	# 						'conversion_factor': 1.0
	# 					})
	# 					valid_items += 1

	# 				if not stock_entry_items:
	# 					if valid_items == 0:
	# 						frappe.msgprint("All items have already been processed")
	# 						return
	# 					frappe.throw("No valid items found to process")

	# 				# 6. Create stock entry
	# 				stock_entry = frappe.get_doc({
	# 					'doctype': 'Stock Entry',
	# 					'posting_date': self.date or frappe.utils.nowdate(),
	# 					'stock_entry_type': 'Material Issue',
	# 					'items': stock_entry_items,
	# 					'custom_general_item_issuance': self.name
	# 				})
	# 				for item in self.general_item_request_ct:
	# 					if item.stock_entry_marked == 0:
	# 						stock_entry.insert(ignore_permissions=True)
	# 						stock_entry.submit()

	# 						# 7. Update child records
	# 						updated = 0
	# 						for item in items_to_process:
	# 							if not getattr(item, 'stock_entry_marked', 0) and item.item_code in [i.item_code for i in stock_entry.items]:
	# 								frappe.db.set_value(
	# 									"General Item Request CT",  # Doctype name
	# 									item.name,
	# 									{
	# 										'stock_entry_marked': 1,
	# 										'stock_entry': stock_entry.name
	# 									}
	# 								)
	# 								updated += 1

	# 								frappe.errprint(f"DEBUG: Updated {updated} child records")
	# 								self.db_set('stock_entry', stock_entry.name)
									
	# 								frappe.msgprint(f"Successfully created Stock Entry {stock_entry.name}")
	# 								return stock_entry.name

	# 	except Exception as e:
	# 		frappe.log_error(
	# 			title=f"Stock Entry Creation Error for {self.name}",
	# 			message=frappe.get_traceback()
	# 		)
	# 		frappe.throw(f"Failed to create Stock Entry: {str(e)}")
	# def send_data_from_gii_to_si(self):
	# 	if self.docstatus != 1:  
	# 		frappe.throw("Document must be submitted before sending data to Stock Entry")

	# 	try:
	# 		frappe.errprint("Starting send_data_from_gii_to_si")

	# 		stock_entry_item = [
	# 			{
	# 				'item_code': item.item_code,
	# 				'qty': item.qty,
	# 				's_warehouse': "Stores - SAH",
	# 			}
	# 			for item in self.general_item_request_ct if item.stock_entry_marked == 0
	# 		]

	# 		if not stock_entry_item:
	# 			frappe.throw("No valid stock entry items to create")

	# 		stock_entry = frappe.get_doc({
	# 			'doctype': 'Stock Entry',
	# 			'posting_date': self.date or frappe.utils.nowdate(),
	# 			'stock_entry_type': 'Material Issue',
	# 			'items': stock_entry_item
	# 		})

	# 		stock_entry.insert()
	# 		stock_entry.submit()  # Ensure it's submitted

	# 		for item in self.general_item_request_ct:
	# 			if item.stock_entry_marked == 0:
	# 				item.stock_entry_marked = 1
	# 				item.stock_entry = stock_entry.name
	# 				item.db_update()  # Save changes

	# 		self.db_set('stock_entry', stock_entry.name)

	# 		frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully")

	# 	except Exception as e:
	# 		frappe.log_error(f"Error in send_data_from_gii_to_si: {e}", "Stock Entry Error")
	# 		frappe.throw(f"Error in processing: {e}")



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



@frappe.whitelist(allow_guest=True)
def close_document(docname):
    try:
        # Directly update the status to 'Closed'
        frappe.db.set_value('General Item Issuance', docname, 'status', 'Closed')
        frappe.db.set_value('Request Form', docname.request_form, 'status', 'Closed')

        # Commit the changes to apply them immediately
        frappe.db.commit()

        return {'status': 'success', 'message': 'Document closed successfully.'}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Close Document Error')
        frappe.throw(('An error occurred while closing the document: {0}').format(str(e)))


