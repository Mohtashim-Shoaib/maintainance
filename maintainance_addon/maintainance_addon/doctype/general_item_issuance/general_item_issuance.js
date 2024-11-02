// Copyright (c) 2024, mohtashim and contributors
// For license information, please see license.txt

frappe.ui.form.on('General Item Issuance',{
    refresh(frm){
        frm.add_custom_button('Add Qty', function(){
            console.log("Custom button clicked");
            if(frm.doc.docstatus != 1){
                frappe.msgprint(__('This operation is only valid for submitted documents'));
                return;
            }
            var d = new frappe.ui.Dialog({
                
                fields:[
                    {'label':'Item', 'fieldname':'item','fieldtype':'Link','options':'Item'},
                    {'label':"Qty", 'fieldname':'qty', 'fieldtype': 'Int'}
                ],
                primary_action : function(){
                    var values = d.get_values()
                    d.hide()
                    if(values){
                        frappe.call({
                            method:'maintainance_addon.maintainance_addon.doctype.general_item_issuance.general_item_issuance.add_general_part_row',
                            args:{
                                'docname': frm.doc.name,
                                'item': values.item,
                                'qty': values.qty

                            },
                            callback: function(response) {
								frappe.show_alert({message: response.message, indicator: 'green'});
								frm.reload_doc();
							}
                        })
                    }
                }
            })
            d.show()
        })
    }
})
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

// frappe.ui.form.on('General Item Issuance', {
//     before_save: function(frm) {
//         frm.reload_doc();
//     }
// });


// frappe.ui.form.on('General Item Issuance', {
// 	refresh:function (frm){
// 		frm.set_df_property('general_item_issuance_ct','cannot_add_rows',1)
// 		frm.set_df_property('general_item_request_ct','cannot_add_rows',1)
// 		frm.set_df_property('general_item_issuance_ct','read_only',1)
// 	}
// 	});


