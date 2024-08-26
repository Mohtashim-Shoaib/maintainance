// Copyright (c) 2024, mohtashim and contributors
// For license information, please see license.txt


frappe.ui.form.on('General Item Issuance', {
    refresh(frm) {
        frm.fields_dict['general_item_request_ct'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
            var requested_items = get_requested_items(frm);
                return {
                    filters: [
                        ["Item","item_code", "in", requested_items ]
                    ] 
            }
        }
    }
});

function get_requested_items(frm) {
    var requested_items = [];
    frm.doc.general_item_issuance_ct.forEach(row => {
        if (!requested_items.includes(row.part_name)) {
            requested_items.push(row.part_name);
        }
    });
    console.log("Requested Items:", requested_items);
    return requested_items;
}
