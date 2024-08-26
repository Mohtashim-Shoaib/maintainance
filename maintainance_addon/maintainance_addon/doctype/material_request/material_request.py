import frappe
from frappe.model.document import Document 

class MaterialRequest(Document):
	def validate(self):
		self.update_request_form_status()
		self.check()
	
	def on_change(self):
		self.check()


	def check(self):
		frappe.msgprint('1')
		if self.custom_request_form:
			frappe.db.sql("""
				UPDATE `tabRequest Form`
				SET status = %s
				WHERE name = %s
				""", (self.status, self.custom_request_form))
			frappe.db.commit()
			doc = frappe.get_doc('Request Form',self.custom_request_form)
			doc.save()

# maintainance_addon.maintainance_addon.maintainance_addon.doctype.material_request.material_request.check

