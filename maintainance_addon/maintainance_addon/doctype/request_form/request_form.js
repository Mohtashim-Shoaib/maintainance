// Copyright (c) 2024, mohtashim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Request Form', {
	refresh(frm) {
		cur_frm.fields_dict["items"].grid.get_field("item_code").get_query = function (doc) {
			return {
				filters: {
					"item_group": "General"
				}
			}
		}
	}
})


// Define the get_prompt_fields function first
var get_prompt_fields = () => {
	return [
		{
			label: __("Item Code"),
			fieldname: "item_code",
			fieldtype: "Link",
			options: "Item"
		}
	];
};

// Then define the client script for the form
// frappe.ui.form.on('Request Form', {
// 	refresh: function (frm) {
// 		frm.trigger("prepare_custom_button");
// 	},
// 	prepare_custom_button(frm) {
// 		frm.add_custom_button(__('Get Available Stock'), () => {
// 			let fields = get_prompt_fields();
// 			frappe.prompt(fields, (values) => {
// 				// Handle the values from the prompt
// 				console.log('Prompt values:', values);
// 				// Call the method to get available stock based on the item_code from prompt
// 				get_available_stock(frm, values.item_code);
// 				get_available_stock_1(frm, values.item_code);
// 			}, __("Set Values"), __("Get Stock"));
// 		});
// 	}
// });

// function get_available_stock(frm, item_code) {
//     console.log("Fetching available stock for item_code:", item_code);
//     frappe.db.get_doc("Item", item_code).then(doc => {
//         console.log(doc.item_group);
//         var group = doc.item_group;

//         // Define the logic for adding items based on their group
//         const addItemToTable = (itemCode, balanceQty) => {
//             let child = frm.add_child("items", {
//                 "item_code": itemCode,
//                 "balance_qty": balanceQty ? balanceQty : 0 // Use balanceQty if available, otherwise default to 0
//             });
//             frm.refresh_field("items");
//         };

//         // Check the item group and apply logic accordingly
//         if (["ELECTRIC ITEMS", "MACHINE SPARE PARTS", "TOOLS"].includes(group)) {
//             // For ELECTRIC ITEMS and MACHINE SPARE PARTS, fetch available quantity
//             frappe.call({
//                 method: 'get_available_qty',
//                 args: { item_code: item_code },
//                 callback: function (r) {
//                     addItemToTable(item_code, r.message);
//                     if (r.message) {
//                         // frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
//                     } else {
//                         // frappe.msgprint("No stock available for the selected item.");
//                     }
//                 }
//             });
//         }
//     });
// }
// function get_available_stock_1(frm, item_code) {
//     console.log("Fetching available stock for item_code:", item_code);
//     frappe.db.get_doc("Item", item_code).then(doc => {
//         console.log(doc.item_group);
//         var group = doc.item_group;

//         // Define the logic for adding items based on their group
//         const addItemToTable = (itemCode, balanceQty) => {
//             let child = frm.add_child("item", {
//                 "item_code": itemCode,
//                 "balance_qty": balanceQty ? balanceQty : 0 // Use balanceQty if available, otherwise default to 0
//             });
//             frm.refresh_field("item");
//         };

//         // Check the item group and apply logic accordingly
//         if (["STATIONERY ITEMS", "GENERAL ITEM"].includes(group)) {
//             // For ELECTRIC ITEMS and MACHINE SPARE PARTS, fetch available quantity
//             frappe.call({
//                 method: 'get_available_qty',
//                 args: { item_code: item_code },
//                 callback: function (r) {
//                     addItemToTable(item_code, r.message);
//                     if (r.message) {
//                         // frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
//                     } else {
//                         // frappe.msgprint("No stock available for the selected item.");
//                     }
//                 }
//             });
//         }
//     });
// }

// 	frappe.ui.form.on('Request Form', {
// 		refresh: function (frm) {
// 			frm.set_df_property('item', 'cannot_add_rows', true); // Hide add row button
// 			frm.set_df_property('items', 'cannot_add_rows', true);
// 			// frm.set_df_property('dimensions', 'cannot_delete_rows', true); // Hide delete button
// 			// frm.set_df_property('dimensions', 'cannot_delete_all_rows', true); // Hide delete all button
// 		}
// 	});

// 	frappe.ui.form.on("Parts Request CT", {
// 		qty:function(frm,cdt, cdn){
// 			let row= locals[cdt][cdn]
// 			console.log(row)
// 			let total=0
// 			for(let i in frm.doc.items){
// 				total += frm.doc.items[i].qty
// 			}
		  
// 			frm.set_value('total_parts',total)
// 			// console.log(total)
// 			frm.refresh()
// 		},
// 		items:function(frm,cdt,cdn){
// 			frm.script_manager.trigger("qty",cdt,cdn)
// 			// console.log("test1")
// 		},
// 		items_remove(frm,cdt,cdn){
// 			frm.script_manager.trigger('qty',cdt,cdn)
	
			
// 		}
		
// 	})

// 	frappe.ui.form.on('General Request CT', {
// 		qty:function(frm,cdt,cdn){
// 				let row = locals[cdt][cdn]
// 				console.log(row)
// 				let total=0
// 				for (let i in frm.doc.item){
// 					total += frm.doc.item[i].qty
// 				}
// 				frm.set_value('total_general',total)
// 				frm.refresh()
// 			},
// 			item:function(frm,cdt,cdn){
// 				frm.script_manager.trigger('qty',cdt,cdn)
// 				console.log(1)
// 			},
// 			item_remove(frm,cdt,cdn){
// 				frm.script_manager.trigger('qty',cdt,cdn)
// 				console.log(2)
// 			}
// 	})

// Ensure this script is linked in your Frappe hooks or included in the custom scripts section

frappe.ui.form.on('Request Form', {
    refresh(frm) {
        // Setup filter
        cur_frm.fields_dict["items"].grid.get_field("item_code").get_query = function (doc) {
            return {
                filters: {
                    "item_group": "General"
                }
            }
        };

        // Prepare custom button
        frm.add_custom_button(__('Get Available Stock'), () => {
            let fields = get_prompt_fields();
            frappe.prompt(fields, (values) => {
                // Handle the values from the prompt
                get_available_stock(frm, values.item_code);
                get_available_stock_1(frm, values.item_code);
            }, __("Set Values"), __("Get Stock"));
        });
    }
});

// Define the get_prompt_fields function
var get_prompt_fields = () => {
    return [
        {
            label: __("Item Code"),
            fieldname: "item_code",
            fieldtype: "Link",
            options: "Item"
        }
    ];
};

// Define the get_available_stock function
function get_available_stock(frm, item_code) {
    frappe.db.get_doc("Item", item_code).then(doc => {
        var group = doc.item_group;
        const addItemToTable = (itemCode, balanceQty) => {
            let child = frm.add_child("items", {
                "item_code": itemCode,
                "balance_qty": balanceQty ? balanceQty : 0
            });
            frm.refresh_field("items");
        };

        if (["ELECTRIC ITEMS", "MACHINE SPARE PARTS", "TOOLS"].includes(group)) {
            frappe.call({
                method: "maintainance_addon.maintainance_addon.doctype.request_form.request_form.get_available_qty",
                args: { item_code: item_code },
                callback: function (r) {
                    addItemToTable(item_code, r.message);
                }
            });
        }
    });
}

// Define the get_available_stock_1 function
function get_available_stock_1(frm, item_code) {
    frappe.db.get_doc("Item", item_code).then(doc => {
        var group = doc.item_group;
        const addItemToTable = (itemCode, balanceQty) => {
            let child = frm.add_child("item", {
                "item_code": itemCode,
                "balance_qty": balanceQty ? balanceQty : 0
            });
            frm.refresh_field("item");
        };

        if (["STATIONERY ITEMS", "GENERAL ITEM"].includes(group)) {
            frappe.call({
                method: "maintainance_addon.maintainance_addon.doctype.request_form.request_form.get_available_qty",
                args: { item_code: item_code },
                callback: function (r) {
                    addItemToTable(item_code, r.message);
                }
            });
        }
    });
}
