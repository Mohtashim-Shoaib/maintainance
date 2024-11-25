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
    # pass
    if self.per_ordered is not None and self.custom_request_form is not None:
        frappe.db.sql("""
            UPDATE `tabRequest Form`
            SET status = %s,
                per_ordered1 = %s,
                per_received = %s
            WHERE name = %s
        """, (self.status, self.per_ordered, self.per_received, self.custom_request_form))

        # Commit the changes to the database
        frappe.db.commit()

        # Fetch and save the Request Form document
        doc = frappe.get_doc("Request Form", self.custom_request_form)
        doc.save()
