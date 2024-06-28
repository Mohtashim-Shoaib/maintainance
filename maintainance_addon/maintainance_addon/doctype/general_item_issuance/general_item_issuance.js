// Copyright (c) 2024, mohtashim and contributors
// For license information, please see license.txt
/*frappe.ui.form.on('Machine Parts', {
	  refresh(frm) {
		  frm.set_query('part_name', 'machine_part_details', function(doc, cdt, cdn) {
				var d = locals[cdt][cdn];
				return {
					"filters": {
					  "item_group": "Spare Parts"
					}
				};
			});
		  frm.set_query('machine_no', 'machine_part_details', function(doc, cdt, cdn) {
				var d = locals[cdt][cdn];
				return {
					"filters": {
					  "asset_category": "Machine"
					}
				};
			});

		  
	  }
	})
    
	*/

// frappe.ui.form.on("General Item Issuance", "refresh", function (frm) {

// 	if (frappe.user.has_role("Store")) {

// 		frm.fields_dict['general_item_issuance_ct'].grid.get_field('part_name').get_query = function (doc, cdt, cdn) {
// 			var child = locals[cdt][cdn];
// 			//console.log(child);
// 			return {
// 				filters: [
// 					['item_group', 'in', ["ELECTRIC ITEMS", "GENERAL ITEM", "STATIONERY ITEMS", "TOOLS"]]
// 				]
// 			}
// 		}

// 	}



// });


// frappe.ui.form.on("General Item Issuance", "refresh", function (frm) {

// 	if (frappe.user.has_role("Store")) {

// 		frm.fields_dict['machine_part_returned'].grid.get_field('part_name').get_query = function (doc, cdt, cdn) {
// 			var child = locals[cdt][cdn];
// 			//console.log(child);
// 			return {
// 				filters: [
// 					['item_group', 'in', ["ELECTRIC ITEMS", "GENERAL ITEM", "STATIONERY ITEMS"]]
// 				]
// 			}
// 		}

// 	}



// });


// frappe.ui.form.on('General Item Issuance CT', {
// 	part_name: function (frm, cdt, cdn) {
// 		var d = locals[cdt][cdn];
// 		frappe.call({
// 			method: 'erpnext.maintenance.doctype.machine_parts.machine_parts.get_balance_qty',
// 			args: {
// 				item: d.part_name
// 			},
// 			callback: function (r) {
// 				console.log(r)
// 				d.balance_qty = r.message

// 				frm.refresh_field("general_item_issuance_ct")
// 			}
// 		})
// 	},




// });

// frappe.ui.form.on('General Item Issuance CT', {
// 	part_name(frm, cdt, cdn) {
// 		set_rate(frm, cdt, cdn);

// 	}

// });

// function set_rate(frm, cdt, cdn) {
// 	var d = locals[cdt][cdn];
// 	frappe.call({
// 		method: "frappe.client.get_value",
// 		args: {
// 			doctype: "Item Price",
// 			filters: {
// 				item_code: d.part_name,
// 				price_list: "Standard Buying"
// 			},
// 			fieldname: ["price_list_rate"]
// 		},
// 		callback: function (r) {
// 			frappe.model.set_value(d.doctype, d.name, "rate", r.message["price_list_rate"])

// 		}
// 	});
// }



// frappe.ui.form.on('General Item Issuance', {
// 	refresh(frm) {
// 		frm.fields_dict['machine_part_returned'].grid.get_field('part_name').get_query = function (doc, cdt, cdn) {
// 			var requested_items = get_requested_items(frm);
// 			// var requested_items = "STATIONERY ITEMS";
// 			return {
// 				filters: [
// 					["item_code", "=", requested_items]
// 				]
// 			};
// 		}
// 	}
// });

// frappe.ui.form.on('General Item Issuance', {
//     refresh(frm) {
//         frm.fields_dict['general_item_request_ct'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
//             var requested_items = get_requested_items(frm);
//             if (requested_items.length > 0) {
//                 // Use the first item for filtering
//                 return {
//                     filters: [
//                         ["item_code", "=", requested_items[0]]
//                     ]
//                 };
//             } 
// 			// else {
//             //     // Fallback filter if no items are requested
//             //     return {
//             //         filters: [
//             //             ["item_code", "=", "STATIONERY ITEMS"]
//             //         ]
//             //     };
//             // }
//         }
//     }
// });
// frappe.ui.form.on('General Item Issuance', {
//     refresh(frm) {
//         frm.fields_dict['general_item_request_ct'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
//             var requested_items = get_requested_items(frm);
//             var childDoc = locals[cdt][cdn]; // Get the current row's document

//             // Replace 'actual_field_name' with the field you want to check in childDoc
//             if (childDoc && childDoc.part_name && requested_items.length > 0) {
//                 // Assuming you want to filter by the actual value of 'actual_field_name'
//                 return {
//                     filters: [
//                         ["item_code", "=", childDoc.part_name] // Adjust this based on actual logic
//                     ]
//                 };
//             }
//             // If no specific condition is met, you might want to return a default filter or no filter
//             // Example: return {}; for no filter or adjust accordingly
//         }
//     }
// });

// function get_requested_items(frm) {
// 	var requested_items = [];
// 	// console.log(requested_items)
// 	frm.doc.general_item_issuance_ct.forEach(row => {
// 		console.log(row)
// 		console.log(row.part_name)
// 		requested_items.push(row.part_name);
// 		// requested_items.push("STATIONERY ITEMS");
// 		// if (row.item_code) {
// 			// requested_items.push(row.part_name);
// 			console.log(requested_items)
// 		// }
// 	});
// 	return requested_items;
// }

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
// 	refresh:function (frm){
// 		frm.set_df_property('general_item_issuance_ct','cannot_add_rows',1)
// 		frm.set_df_property('general_item_issuance_ct','read_only',1)
// 	}
// 	});

// frappe.ui.form.on('General Item Issuance', {	
// 	quantity: function(frm,cdt,cdn){
// 		calculate_and_set_total(frm)
// 	}

// });

// function calculate_and_set_total(frm){
// 	let total_quantity = 0;
// 	frm.doc.total_requested.forEach(function(d){
// 		total_quantity += d.qty;
// 	})
// 	frm.set_value('total_quantity',total_quantity);
// 	frm.refresh_field('total_requested');

// }
// frappe.ui.form.on('General Item Issuance', {
//     validate: function(frm) {
//         // Create a map for quick lookup of issued quantities by item_code
//         let issuedQuantities = {};
//         frm.doc.general_item_issuance_ct.forEach(function(issuance) {
//             if (issuedQuantities[issuance.item_code]) {
//                 issuedQuantities[issuance.item_code] += issuance.qty;
//             } else {
//                 issuedQuantities[issuance.item_code] = issuance.qty;
//             }
//         });	

//         // Validate requested quantities against issued quantities
//         frm.doc.general_item_request_ct.forEach(function(request) {
//             let issuedQty = issuedQuantities[request.item_code] || 0;
//             if (request.qty > issuedQty) {
//                 frappe.throw(`You have selected an incorrect value for the item ${request.item_code}. Requested quantity (${request.qty}) cannot be greater than issued quantity (${issuedQty}).`);
//             }
//         });
//     }
// });

// frappe.ui.form.on('General Item Issuance', {
//     before_save: function(frm) {
//         frm.reload_doc();
//     }
// });
