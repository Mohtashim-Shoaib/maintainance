# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RequestForm(Document):
    def before_submit(self):
        frappe.msgprint(test)
        self.make_part_issuance()
        self.make_gi_issuance()
    def make_part_issuance(self):
        relevant_items_exist = False
        for row in self.items:
            item_group = frappe.db.get_value('Item', row.item_code, 'item_group')
            if item_group == "MACHINE SPARE PARTS":
                relevant_items_exist = True
                break
        if relevant_items_exist:
            mr = frappe.new_doc("Machine Parts")
            mr.date = self.posting_date
            mr.by_hand = "ABDUL REHMAN"
            for row in self.items:
                item_group = frappe.db.get_value('Item', row.item_code, ['item_group'])
                if item_group == "MACHINE SPARE PARTS":
                    mri= mr.append('requested_items')
                    mri.item_code = row.item_code
                    mri.requested_qty = row.required_qty
            mr.save()
    def make_gi_issuance(self):
        relevant_items_exist = False
        for row in self.items:
            item_group = frappe.db.get_value('Item', row.item_code, 'item_group')
            if item_group == "ELECTRIC ITEMS" or "GENERAL ITEM" or "STATIONERY ITEMS" or "TOOLS":
                relevant_items_exist = True
                break
        if relevant_items_exist:
            mr = frappe.new_doc("General Item Issuance")
            mr.date = self.posting_date
            mr.by_hand = "ABDUL REHMAN"
            mr.user = self.request_by
            for row in self.items:
                item_group = frappe.db.get_value('Item', row.item_code, 'item_group')
                if item_group in ["ELECTRIC ITEMS", "GENERAL ITEM", "STATIONERY ITEMS", "TOOLS"]:
                    mri= mr.append('general_item_issuance_ct')
                    mri.part_name = row.item_code
                    mri.qty = row.required_qty
                    mri.department = "Production - SAH"
            mr.save()
            

@frappe.whitelist()
def make_mr(request_form):
    doc = frappe.get_doc("Request Form", request_form)
    mr = frappe.new_doc("Material Request")
    mr.material_request_type = "Purchase"
    mr.transaction_date = doc.posting_date
    mr.set_warehouse = "Stores - SAH"
    mri= mr.append('items')
    for row in doc.items:
        if row.required_qty > 0:
            mri.item_code = row.item_code
            mri.qty = row.required_qty
            mri.schedule_date = doc.posting_date
            mri.uom = frappe.db.get_value('item', row.item_code, 'stock_uom')
    mr.save()
    frappe.msgprint("Material Request created!")
    


@frappe.whitelist()
def make_issuance(request_form):
    doc = frappe.get_doc("Request Form", request_form)
    mr = frappe.new_doc("Machine Parts Issuance")
    mr.date = doc.posting_date
    mr.by_hand = "ABDUL REHMAN"
    mri= mr.append('machine_part_details')
    for row in doc.items:
        mri.item_code = row.item_code
        mri.required_qty = row.balance_qty
        mri.department = "Production - SAH"
    mr.save()
    frappe.msgprint("Parts Issurance created!")

@frappe.whitelist()
def get_available_qty(item_code):
    payload_data = frappe.form_dict
    # frappe.errprint(payload_data)
    frappe.response["message"] = frappe.db.get_value("Bin",{"item_code":payload_data.item_code},"actual_qty")