// Copyright (c) 2024, mohtashim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Machine Parts Issuance', {
	refresh(frm) {
		frm.fields_dict['machine_part_returned'].grid.get_field('part_name').get_query = function (doc, cdt, cdn) {
			var part_name_related = get_part_name_related(frm);
			return {
				filters: [
					["Item", "item_code", "in", part_name_related]
				]
			};
		}
	}
});


frappe.ui.form.on('Machine Parts Issuance', {
    refresh(frm) {
        frm.add_custom_button('Add Qty', function() {
            if (frm.doc.docstatus != 1) {
                frappe.msgprint(__('This operation is only allowed on submitted documents.'));
                return;
            }

            var d = new frappe.ui.Dialog({
                'fields': [
                    {'label': 'Item', 'fieldname': 'item', 'fieldtype': 'Link', 'options': 'Item'},
                    {'label': 'Qty', 'fieldname': 'qty', 'fieldtype': 'Int'},
                    // {'fieldname': 'today', 'fieldtype': 'Date', 'default': frappe.datetime.nowdate()}
                ],
                primary_action: function() {
                    var values = d.get_values();
                    d.hide();
                  if (values) {
                        frappe.call({
							method: 'maintainance_addon.maintainance_addon.doctype.machine_parts_issuance.machine_parts_issuance.add_machine_part_row',
							args: {
								docname: frm.doc.name,
								item_code: values.item,
								qty: values.qty
								// today: values.today
							},
							callback: function(response) {
								frappe.show_alert({message: response.message, indicator: 'green'});
								frm.reload_doc();
							}
						});
                    }
                }
            });
            d.show();
        });
    }
});

frappe.ui.form.on('Machine Parts Issuance', {
	refresh(frm) {
		frm.fields_dict['machine_part_details'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
			var requested_items = get_requested_items(frm);
			return {
				filters: [
					["Item", "item_code", "in", requested_items]
				]
			};
		}
	}
});

function get_requested_items(frm) {
	var requested_items = [];
	frm.doc.requested_items.forEach(row => {
		if (row.item_code) {
			requested_items.push(row.item_code);
			console.log(requested_items)
		}
	});
	return requested_items;
}


// Function to get related part names from machine_part_details
function get_part_name_related(frm) {
	var part_name_related = [];
	frm.doc.machine_part_details.forEach(row => {
		if (row.item_code) {
			part_name_related.push(row.item_code);
		}
	});
	return part_name_related;
}

	// frappe.ui.form.on('Machine Parts Issuance', {
	// refresh:function (frm){
	// 	frm.set_df_property('requested_items','cannot_add_rows',1)
	// 	frm.set_df_property('requested_items','read_only',1)
	// }
	// });

	// frappe.ui.form.on('Machine Parts Issuance', {
	// 	refresh: function(frm) {
	// 		// Call calculate totals on form refresh
	// 		frm.trigger('calculate_totals');
	// 		frm.trigger('qty_to_provided');
	// 		frm.trigger('set_status');
	// 	},
	
	// 	// Trigger calculation when form is loaded or fields are updated
	// 	onload: function(frm) {
	// 		frm.trigger('calculate_totals');
	// 		frm.trigger('qty_to_provided');
	// 		frm.trigger('set_status');
	// 	},
	
	// 	calculate_totals: function(frm) {
	// 		let requested_total = 0;
	// 		let issued_total = 0;
	
	// 		// Sum requested quantities
	// 		frm.doc.requested_items.forEach(item => {
	// 			requested_total += flt(item.request_quantity);
	// 		});
	
	// 		// Sum issued quantities
	// 		frm.doc.machine_part_details.forEach(item => {
	// 			issued_total += flt(item.issued_qty);
	// 		});
	
	// 		// Set the total fields
	// 		frm.set_value('total_requested_item', requested_total);
	// 		frm.set_value('total_issued_item', issued_total);
	
	// 		// Optionally, you can refresh the fields or the form
	// 		frm.refresh_field('total_requested_item');
	// 		frm.refresh_field('total_issued_item');
	// 	},
		
	// 	// qty to be provided function
	// 	qty_to_provided : function(frm){
	// 		let qty_to_provided = frm.doc.total_requested_item - frm.doc.total_issued_item
	// 		frm.set_value('qty_to_be_provided', qty_to_provided);
	// 		frm.refresh_field('qty_to_be_provided');
	// 	},
	// 	// set status
	// 	set_status: function(frm){
	// 		if (frm.doc.qty_to_be_provided == 0){
	// 			frm.doc.status = "Completed"
	// 		}
	// 		else if (frm.doc.total_issued_item < frm.doc.total_requested_item){
	// 			frm.doc.status = "In Progress"
	// 		}
	// 		else if (frm.doc.qty_to_be_provided < 0){
	// 			frm.doc.status = "Draft"
	// 		}
	// 	}
	// });
	
	// frappe.ui.form.on('Machine Parts Issuance', {
	// 	refresh: function(frm) {
	// 		// Add a button to trigger balance quantity update if needed
	// 		frm.add_custom_button(__('Update Balance Quantity'), function() {
	// 			frm.trigger('update_balance_qty');
	// 		});
	// 	},
	
	// 	update_balance_qty: function(frm) {
	// 		frm.doc.requested_items.forEach(async function(item) {
	// 			if (!item.item_code) return;
	
	// 			// Query the Bin doctype for the item_code
	// 			let response = await frappe.call({
	// 			method: 'frappe.client.get_list',
	// 				args: {
	// 					doctype: 'Bin',
	// 					filters: {
	// 						item_code: item.item_code
	// 					},
	// 					fields: ['actual_qty'],
	// 					limit_page_length: 1
	// 				},
	// 				callback: function(r) {
	// 					if (r.message && r.message.length > 0) {
	// 						let bin_doc = r.message[0];
	// 						let balance_qty = bin_doc.actual_qty || 0;
							
	// 						// Update the item in the child table
	// 						frappe.model.set_value(item.doctype, item.name, 'balance_qty', balance_qty);
	// 						frm.refresh_field('requested_items');
	// 					} 
	// 					// else {
	// 					// 	console.error(`Bin not found for item code: ${item.item_code}`);
	// 					// }
	// 				}
	// 			});
	// 		});
	// 	}
	// });
		

