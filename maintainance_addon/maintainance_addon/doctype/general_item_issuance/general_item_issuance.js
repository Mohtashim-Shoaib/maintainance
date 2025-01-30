// Copyright (c) 2024, mohtashim and contributors
// For license information, please see license.txt
frappe.ui.form.on('General Item Issuance', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Close Document'), () => frm.events.close_document(frm), __("Status"));
        }
    },

    close_document: function(frm) {
        frappe.confirm(
            __('Are you sure you want to close this document?'),
            function() {
                frappe.call({
                    method:'maintainance_addon.maintainance_addon.doctype.general_item_issuance.general_item_issuance.close_document',
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function(response) {
                        if (!response.exc) {
                            frappe.msgprint(__('The document has been successfully closed.'));
                            frm.reload_doc();
                        } else {
                            frappe.msgprint(__('Error while closing the document.'));
                        }
                    }
                });
            }
        );
    }
});


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
    refresh: function(frm) {
        frm.add_custom_button(__('Refresh'), function() {
            // Get the value of the field 'stock_entry_marked'
            var current_value = frm.doc.check;
            
            // Toggle the value between 0 and 1
            frm.set_value('check', current_value == 0 ? 1 : 0);
            
            // Save the changes
            frm.save()
                .then(() => {
                    // Reload the document to reflect the changes
                    frm.reload_doc();
                })
                .catch((error) => {
                    frappe.msgprint(__('Error while saving changes.'));
                    console.error(error);
                });

        });
        // Add button for Stock Ledger Route with item filtering
        frm.add_custom_button(__('Go to Stock Ledger'), function() {
            let item_codes = frm.doc.general_item_request_ct.map(item => item.item_code).join(',');
            let warehouse = "Stores - SAH"; // Default warehouse, adjust if necessary
            frappe.set_route('query-report', 'Stock Ledger', {
                item_code: item_codes,  // Filter by item codes from the General Item Request
                warehouse: warehouse     // You can customize this based on your logic
            });
        });

        // Add button for Stock Balance Route with item filtering
        frm.add_custom_button(__('Go to Stock Balance'), function() {
            let item_codes = frm.doc.general_item_request_ct.map(item => item.item_code).join(',');
            let warehouse = "Stores - SAH"; // Default warehouse, adjust if necessary
            frappe.set_route('query-report', 'Stock Balance', {
                item_code: item_codes,  // Filter by item codes from the General Item Request
                warehouse: warehouse     // Customize warehouse if necessary
            });
        });
    }
});

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
//         frm.set_df_property('general_item_issuance_ct','cannot_delete_rows',1)
// 	}
// 	});

// frappe.ui.form.on('General Item Issuance', {
//     refresh: function (frm) {
//         // Check if the user is an Administrator or has the System Manager role
//         if (frappe.user.has_role('System Manager') || frappe.user.name === 'Administrator') {
//             // Allow adding rows and make fields editable for privileged users
//             frm.set_df_property('general_item_issuance_ct', 'cannot_add_rows', 0);
//             frm.set_df_property('general_item_request_ct', 'cannot_add_rows', 0);
//             frm.set_df_property('general_item_issuance_ct', 'read_only', 0);
//         } else {
//             // Restrict actions for non-privileged users
//             frm.set_df_property('general_item_issuance_ct', 'cannot_add_rows', 1);
//             frm.set_df_property('general_item_request_ct', 'cannot_add_rows', 1);
//             frm.set_df_property('general_item_issuance_ct', 'read_only', 1);
//         }
//     }
// });
