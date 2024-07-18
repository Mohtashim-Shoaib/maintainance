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


frappe.ui.form.on('Machine Parts Issuance', {
    onload: function(frm) {
        update_total_qty1(frm);
    },
    refresh: function(frm) {
        update_total_qty1(frm);
    },
    requested_items_add: function(frm) {
        update_total_qty1(frm);
    },
    requested_items_remove: function(frm) {
        update_total_qty1(frm);
    },
	// before_save:function(frm){
	// 	update_total_qty1(frm)
	// },
	// validate:function(frm){
	// 	update_total_qty1(frm)
	// }
});

function update_total_qty1(frm) {
	console.log("test")
    let total_qty = 0;
    frm.doc.requested_items.forEach(function(row) {
        total_qty += row.request_quantity || 0; // Assuming 'qty' is the field name for quantity in the child table
		console.log(total_qty)
    });

    // Assuming 'total_quantity' is the field name in the parent doctype where you want to show the sum
    frm.set_value('total_requested_item', total_qty);
    refresh_field('total_requested_item'); // Refresh the field to show the updated value

	// frm.set_value('total_request', total_qty);
    // refresh_field('total_request');
	// frappe.msgprint('issued')
}





frappe.ui.form.on('Machine Parts Issuance', {
    onload: function(frm) {
        update_total_qty(frm);
    },
    refresh: function(frm) {
        update_total_qty(frm);
    },
    machine_part_details_add: function(frm) {
        update_total_qty(frm);
    },
	before_save: function(frm) {
		update_total_qty(frm);
	},
    machine_part_details_remove: function(frm) {
        update_total_qty(frm);
    }
});

function update_total_qty(frm) {
    let total_qty = 0;
    frm.doc.machine_part_details.forEach(function(row) {
        total_qty += row.issued_qty || 0; // Assuming 'qty' is the field name for quantity in the child table
    });

    // Assuming 'total_quantity' is the field name in the parent doctype where you want to show the sum
    frm.set_value('total_issued_item', total_qty);
    refresh_field('total_issued_item'); // Refresh the field to show the updated value

	// frm.set_value('total_issue', total_qty);
    // refresh_field('total_issue');
}




// frappe.ui.form.on('Machine Parts Issuance', {
// 	onload: function(frm) {
// 		update_total_qty(frm);
// 	},
// 	before_save:function(frm){
// 		update_total_qty(frm);
// 	},
// 	refresh: function(frm) {
// 		update_total_qty(frm);
// 	},
// 	validate:function(frm){
// 		update_total_qty(frm);
// 	},
// })

// function set_qty(frm){
// 	let requested_qty = frm.doc.total_requested_item;
// 	let issued_qty = frm.doc.total_issued_item;
// 	let qty = requested_qty - issued_qty;
// 	frm.set_value('qty_to_be_provided',90);
// }

frappe.ui.form.on('Machine Parts Issuance', {
    after_save: function(frm) {
        frm.reload_doc();
    }
});

// frappe.ui.form.on('Machine Parts Issuance', {
//     refresh: function(frm) {
//         console.log(frm); // For debugging, consider removing for production
//         var totalRequested = frm.doc.total_requested_item;
//         var totalIssued = frm.doc.total_issued_item;
//         var balanceQty = totalRequested - totalIssued;
//         // frappe.msgprint('Balance Quantity: ' + balanceQty);
// 		frm.set_value('qty_to_be_provided', balanceQty);
//         if (balanceQty === 0) {
//             frm.set_value('status', 'Completed');
//         }
// 		else if (totalIssued === 0) {
//             frm.set_value('status', 'Draft');
//         }
// 		else if (totalIssued < totalRequested) {
//             frm.set_value('status', 'In Progress');
//         }
//     }
// });

frappe.ui.form.on('Machine Parts Issuance', {
	    refresh: function(frm) {
			set_status(frm)
		},
		total_issued_item: function(frm) {
			set_status(frm)
		}
	})

function set_status(frm){
	var totalRequested = frm.doc.total_requested_item;
        var totalIssued = frm.doc.total_issued_item;
        var balanceQty = totalRequested - totalIssued;
        // frappe.msgprint('Balance Quantity: ' + balanceQty);
		frm.set_value('qty_to_be_provided', balanceQty);
        if (balanceQty === 0) {
            frm.set_value('status', 'Completed');
        }
		else if (totalIssued === 0) {
            frm.set_value('status', 'Draft');
        }
		else if (totalIssued < totalRequested) {
            frm.set_value('status', 'In Progress');
        }
}
