# Copyright (c) 2024, mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RequestForm(Document):
    def before_submit(self):
        self.send_data_from_request_form_to_general_issance_form()
        self.send_data_from_request_form_to_material_request()
        self.send_data_from_request_form_to_part()
        # self.make_part_issuance()
        # self.make_gi_issuance()


    def send_data_from_request_form_to_part(self):
        # frappe.msgprint("test")
        request_form = self

        part_issuance_items = []
        for item in request_form.items:
            frappe.msgprint(f"Machine Part Issuance had been created for {item.item_code}")
            part_issuance_items.append({
                    'item_code': item.item_code,
                    'item_name': item.item_code,
                    'requested_qty': item.qty,
                    'remarks':item.remarks,
                    'balance_qty':item.balance_qty
                })
            # frappe.errprint(part_issuance_items)
            
        general_item = frappe.get_doc({
                'doctype': 'Machine Parts Issuance',
                'date': request_form.posting_date,
                "user": request_form.request_by,
                "by_hand":"ABDUL REHMAN",
                "requested_items": part_issuance_items,
            })     
        general_item.insert(ignore_permissions=True)
        general_item.save()

         # Update the part_request field with the name of the newly created document
        request_form.db_set('part_request', general_item.name)
        request_form.db_set('part_request_form', general_item.name)

    # Fetch the updated value from the database to confirm the update
        updated_part_request = frappe.db.get_value('Request Form', request_form.name, 'part_request_form')

        # Print the updated value to verify
        frappe.errprint(updated_part_request)



    def send_data_from_request_form_to_material_request(self):
        request_form = self
        material_request_items = []
        for item in request_form.items:
            if item.balance_qty ==  0:
                balance_qty_not_available = True
                frappe.msgprint(f"Balance Qty is not available for item {item.item_code}")
                material_request_items.append({
                        'item_code': item.item_code,
                        'qty': item.qty,
                        'schedule_date': request_form.posting_date,
                        'uom': frappe.db.get_value('Item', item.item_code, 'stock_uom'),
                    })
        for item in request_form.item:
            if item.balance_qty ==  0:
                balance_qty_not_available = True
                frappe.msgprint(f"Balance Qty is not available for item {item.item_code}")
                material_request_items.append({
                        'item_code': item.item_code,
                        'qty': item.qty,
                        'schedule_date': request_form.posting_date,
                        'uom': frappe.db.get_value('Item', item.item_code, 'stock_uom'),
                    })
                material_request = frappe.get_doc({
                        'doctype': 'Material Request',
                        'material_request_type': 'Purchase',
                        'transaction_date': request_form.posting_date,
                        'set_warehouse': 'Stores - SAH',
                        'items': material_request_items,
                        'title': f"Material Request for {request_form.name}",
                    })
                material_request.insert(ignore_permissions=True)
                material_request.save()
                frappe.msgprint("Material Request created!")





    def send_data_from_request_form_to_general_issance_form(self):
        # frappe.msgprint("test")
        request_form = self

        general_issuance_items = []
        for item in request_form.item:
            frappe.msgprint(f"General Issuance Item had been created for {item.item_code}")
            general_issuance_items.append({
                    'part_name': item.item_code,
                    'qty': item.qty,
                    'balance_qty':item.balance_qty,
                })
            frappe.errprint(general_issuance_items)
            
        general_item = frappe.get_doc({
                'doctype': 'General Item Issuance',
                'date': request_form.posting_date,
                "user": request_form.request_by,
                "by_hand":"ABDUL REHMAN",
                "general_item_issuance_ct": general_issuance_items,
            })     
        general_item.insert(ignore_permissions=True)
        general_item.save()

        request_form.db_set('general_request_form',general_item.name)
        

    
    # def make_part_issuance(self):
    #     relevant_items_exist = False
    #     for row in self.items:
    #         item_group = frappe.db.get_value('Item', row.item_code, 'item_group')
    #         if item_group == "MACHINE SPARE PARTS":
    #             relevant_items_exist = True
    #             break
    #     if relevant_items_exist:
    #         mr = frappe.new_doc("Machine Parts")
    #         mr.date = self.posting_date
    #         mr.by_hand = "ABDUL REHMAN"
    #         for row in self.items:
    #             item_group = frappe.db.get_value('Item', row.item_code, ['item_group'])
    #             if item_group == "MACHINE SPARE PARTS":
    #                 mri= mr.append('requested_items')
    #                 mri.item_code = row.item_code
    #                 mri.requested_qty = row.required_qty
    #         mr.save()
    # def make_gi_issuance(self):
    #     relevant_items_exist = False
    #     for row in self.items:
    #         item_group = frappe.db.get_value('Item', row.item_code, 'item_group')
    #         if item_group == "ELECTRIC ITEMS" or "GENERAL ITEM" or "STATIONERY ITEMS" or "TOOLS":
    #             relevant_items_exist = True
    #             break
    #     if relevant_items_exist:
    #         mr = frappe.new_doc("General Item Issuance")
    #         mr.date = self.posting_date
    #         mr.by_hand = "ABDUL REHMAN"
    #         mr.user = self.request_by
    #         for row in self.items:
    #             item_group = frappe.db.get_value('Item', row.item_code, 'item_group')
    #             if item_group in ["ELECTRIC ITEMS", "GENERAL ITEM", "STATIONERY ITEMS", "TOOLS"]:
    #                 mri= mr.append('general_item_issuance_ct')
    #                 mri.part_name = row.item_code
    #                 mri.qty = row.required_qty
    #                 mri.department = "Production - SAH"
    #         mr.save()
            

# @frappe.whitelist()
# def make_mr(request_form):
#     doc = frappe.get_doc("Request Form", request_form)
#     mr = frappe.new_doc("Material Request")
#     mr.material_request_type = "Purchase"
#     mr.transaction_date = doc.posting_date
#     mr.set_warehouse = "Stores - SAH"
#     mri= mr.append('items')
#     for row in doc.items:
#         if row.required_qty > 0:
#             mri.item_code = row.item_code
#             mri.qty = row.required_qty
#             mri.schedule_date = doc.posting_date
#             mri.uom = frappe.db.get_value('item', row.item_code, 'stock_uom')
#     mr.save()
#     frappe.msgprint("Material Request created!")
    


# @frappe.whitelist()
# def make_issuance(request_form):
#     doc = frappe.get_doc("Request Form", request_form)
#     mr = frappe.new_doc("Machine Parts Issuance")
#     mr.date = doc.posting_date
#     mr.by_hand = "ABDUL REHMAN"
#     mri= mr.append('machine_part_details')
#     for row in doc.items:
#         mri.item_code = row.item_code
#         mri.required_qty = row.balance_qty
#         mri.department = "Production - SAH"
#     mr.save()
#     frappe.msgprint("Parts Issurance created!")

@frappe.whitelist()
def get_available_qty(item_code):
    payload_data = frappe.form_dict
    # frappe.errprint(payload_data)
    frappe.response["message"] = frappe.db.get_value("Bin",{"item_code":payload_data.item_code},"actual_qty")
    # b = frappe.db.get_value("Item",{"item_code" : payload_data.item_code},['item_name','item_group','stock_uom'])
    # frappe.errprint(b)