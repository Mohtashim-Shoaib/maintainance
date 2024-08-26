import frappe
from frappe.model.document import Document

class MaterialRequest(Document):
    def validate(self):
        check_status(self)
    def on_update(self):
        check_status(self)
    def on_change(self):
        check_status(self)

def check_status(self, method=None):
    frappe.msgprint('11')
    frappe.db.sql("""
    update `tabRequest Form` 
    set status=%s 
    where name = %s
    """,(self.status,self.custom_request_form))
    frappe.msgprint('1')
    frappe.db.commit()

    doc = frappe.get_doc("Request Form", self.custom_request_form)
    frappe.msgprint('111')
    doc.save()
    frappe.msgprint('1111')