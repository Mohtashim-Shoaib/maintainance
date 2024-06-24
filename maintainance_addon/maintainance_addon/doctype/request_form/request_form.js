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


// frappe.ui.form.on('Parts Request CT', {
// 	item_code: function (frm, cdt, cdn) {
// 		var d = locals[cdt][cdn];
// 		frappe.call({
// 			method: 'maintainance_addon.maintainance_addon.doctype.machine_parts.machine_parts.get_balance_qty',
// 			args: {
// 				item: d.item_code
// 			},
// 			callback: function (r) {
// 				console.log(r)
// 				d.balance_qty = r.message

// 				frm.refresh_field("machine_part_details")
// 			}
// 		})
// 	},
// });

// frappe.ui.form.on('Parts Request CT', {
// 	item_code(frm, cdt, cdn) {
// 		set_rate(frm, cdt, cdn);

// 	},
// 	qty(frm, cdt, cdn) {
// 		set_order(frm, cdt, cdn);

// 	}

// });
// function set_order(frm, cdt, cdn) {
// 	var d = locals[cdt][cdn];
// 	if (d.qty > d.balance_qty) {
// 		frappe.model.set_value(d.doctype, d.name, "required_qty", d.qty - d.balance_qty)
// 	}
// 	else {
// 		frappe.model.set_value(d.doctype, d.name, "required_qty", 0)
// 	}
// }
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


// frappe.ui.form.on('Request Form', {
// 	refresh: function (frm) {
// 		var me = frm
// 		frm.add_custom_button(__('Create MR'),
// 			function () {
// 				frappe.call({
// 					method: 'maintainance_addon.maintainance_addon.doctype.request_form.request_form.make_mr',
// 					args: {
// 						request_form: frm.doc.name
// 					},
// 					callback: function (r) {
// 						if (r.message) {
// 							frappe.msgprint(__('Items updated successfully.'));
// 							frm.reload_doc();
// 							console.log("test")
// 						}

// 					}
// 				});



// 			}, __("Create"));
// 		frm.add_custom_button(__('Parts Issuance'),
// 			function () {
// 				frappe.call({
// 					method: 'maintainance_addon.maintainance_addon.doctype.request_form.request_form.make_issuance',
// 					args: {
// 						request_form: frm.doc.name
// 					},
// 					callback: function (r) {
// 						if (r.message) {
// 							frappe.msgprint(__('Items updated successfully.'));
// 							frm.reload_doc();
// 						}
// 					}
// 				});



// 			}, __("Create"));
// 	}
// });


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
frappe.ui.form.on('Request Form', {
	refresh: function (frm) {
		frm.trigger("prepare_custom_button");
	},
	prepare_custom_button(frm) {
		frm.add_custom_button(__('Get Available Stock'), () => {
			let fields = get_prompt_fields();
			frappe.prompt(fields, (values) => {
				// Handle the values from the prompt
				console.log('Prompt values:', values);
				// Call the method to get available stock based on the item_code from prompt
				get_available_stock(frm, values.item_code);
				get_available_stock_1(frm, values.item_code);
			}, __("Set Values"), __("Get Stock"));
		});
	}
});

// Define the function to get available stock
// function get_available_stock(frm, item_code) {
// 	console.log("Fetching available stock for item_code:", item_code);
// 	frappe.db.get_doc("Item", item_code).then(doc => {
// 		console.log(doc.item_group)
// 		var group = doc.item_group

// })
// 	if(group == "ELECTRIC ITEMS"){
// 		// console.log(group)
// 	frappe.call({
// 		method: 'get_available_qty',
// 		args: {
// 			item_code: item_code
// 		},
// 		callback: function (r) {
// 			if (r.message) {
// 				// Add a new child row and set the item code
// 				let child = frm.add_child("items", {
// 					"item_code": item_code
// 				});
// 				// Refresh the child table field
// 				frm.refresh_field("items");	
// 				// Set the balance_qty in the newly added child row
// 				frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

// 				// Optional: show a message
// 				frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
// 			} else {
// 				frappe.msgprint("No stock available for the selected item.");
// 			}
// 		}

// 	});
// }
// }



function get_available_stock(frm, item_code) {
	console.log("Fetching available stock for item_code:", item_code);
	frappe.db.get_doc("Item", item_code).then(doc => {
		console.log(doc.item_group)
		var group = doc.item_group
		if (group == "ELECTRIC ITEMS"){
			frappe.call({
				method: 'get_available_qty',
				args: {
					item_code: item_code
				},
				callback: function (r) {
					if (r.message) {
						// Add a new child row and set the item code
						let child = frm.add_child("items", {
							"item_code": item_code
						});
						// Refresh the child table field
						frm.refresh_field("items");
						// Set the balance_qty in the newly added child row
						frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

						// Optional: show a message
						// frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
					} else {
						frappe.msgprint("No stock available for the selected item.");
					}
				}
			});
		}
		if (group == "MACHINE SPARE PARTS"){
			frappe.call({
				method: 'get_available_qty',
				args: {
					item_code: item_code
				},
				callback: function (r) {
					if (r.message) {
						// Add a new child row and set the item code
						let child = frm.add_child("items", {
							"item_code": item_code
						});
						// Refresh the child table field
						frm.refresh_field("items");
						// Set the balance_qty in the newly added child row
						frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

						// Optional: show a message
						frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
					} else {
						frappe.msgprint("No stock available for the selected item.");
					}
				}
			});
		}
		if (group == "TOOLS"){
			frappe.call({
				method: 'get_available_qty',
				args: {
					item_code: item_code
				},
				callback: function (r) {
					if (r.message) {
						// Add a new child row and set the item code
						let child = frm.add_child("items", {
							"item_code": item_code
						});
						// Refresh the child table field
						frm.refresh_field("items");
						// Set the balance_qty in the newly added child row
						frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

						// Optional: show a message
						frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
					} else {
						frappe.msgprint("No stock available for the selected item.");
					}
				}
			});
		}
	})
}




function get_available_stock_1(frm, item_code) {
	console.log("Fetching available stock for item_code:", item_code);
	frappe.db.get_doc("Item", item_code).then(doc => {
		console.log(doc.item_group)
		var group = doc.item_group
		if (group == "GENERAL ITEM"){
			frappe.call({
				method: 'get_available_qty',
				args: {
					item_code: item_code
				},
				callback: function (r) {
					if (r.message) {
						// Add a new child row and set the item code
						let child = frm.add_child("item", {
							"item_code": item_code
						});
						// Refresh the child table field
						frm.refresh_field("item");
						// Set the balance_qty in the newly added child row
						frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

						// Optional: show a message
						frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
					} else {
						frappe.msgprint("No stock available for the selected item.");
					}
				}
			});
		}
		else if (group == "STATIONERY ITEMS"){
			frappe.call({
				method: 'get_available_qty',
				args: {
					item_code: item_code
				},
				callback: function (r) {
					if (r.message) {
						// Add a new child row and set the item code
						let child = frm.add_child("item", {
							"item_code": item_code
						});
						// Refresh the child table field
						frm.refresh_field("item");
						// Set the balance_qty in the newly added child row
						frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

						// Optional: show a message
						frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
					} else {
						frappe.msgprint("No stock available for the selected item.");
					}
				}
			});
		}
		
	})
}

	// function get_available_stock(frm, item_code) {
	// 	console.log("Fetching available stock for item_code:", item_code);
	// 	frappe.db.get_doc("Item", item_code).then(doc => {
	// 		console.log(doc.item_group)
	// 		var group = doc.item_group
	// 		if(group == "ELECTRIC ITEMS"){
	// 			frappe.call({
	// 				method: 'get_available_qty',
	// 				args: {
	// 					item_code: item_code
	// 				},
	// 				callback: function (r) {
	// 					if (r.message) {
	// 						// Add a new child row and set the item code
	// 						let child = frm.add_child("item", {
	// 							"item_code": item_code
	// 						});
	// 						// Refresh the child table field
	// 						frm.refresh_field("item");
	// 						// Set the balance_qty in the newly added child row
	// 						frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);

	// 						// Optional: show a message
	// 						frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
	// 					} else {
	// 						frappe.msgprint("No stock available for the selected item.");
	// 					}
	// 				}
	// 			});
	// 		}
	// 	})
	// frappe.call({
	// 	method: 'get_available_qty',
	// 	args: {
	// 		item_code: item_code
	// 	},
	// 	callback: function (r) {
	// 		if (r.message) {
	// 			frappe.db.get_doc("Item", item_code).then(doc => {
	// 				console.log(doc)
	// 			})
	// 			if(item_group == "General"){
	// 			let child = frm.add_child("item", {
	// 				"item_code": item_code
	// 			});
	// 			frm.refresh_field("item");
	// 			frappe.model.set_value(child.doctype, child.name, "balance_qty", r.message);
	// 			frappe.msgprint(`Available stock for ${item_code}: ${r.message}`);
	// 		} else {
	// 			frappe.msgprint("No stock available for the selected item.");
	// 		}
	// 	}
	// 	}
	// });






	frappe.ui.form.on('Request Form', {
		refresh: function (frm) {
			frm.set_df_property('item', 'cannot_add_rows', true); // Hide add row button
			frm.set_df_property('items', 'cannot_add_rows', true);
			// frm.set_df_property('dimensions', 'cannot_delete_rows', true); // Hide delete button
			// frm.set_df_property('dimensions', 'cannot_delete_all_rows', true); // Hide delete all button
		}
	});



	// frappe.ui.form.on('Parts Request CT',{
	// 	qty: function(frm, cdt, cdn){
	// 		let row = locals[cdt][cdn]	
	// 		if(row.qty){
	// 				let total= 0
	// 				for (let i in frm.doc.items){
	// 					total += frm.doc.items[i].qty
	// 				}
	// 				frm.set_value('total_parts', total)
	// 				frm.refresh()
	// 		}
	// 	},
	// 	qty:function(frm, cdt, cdn){  // amount replace it with your amount fieldname
	// 		frm.script_manager.trigger('qty', cdt, cdn)  // the above item_code function is calling here
	// 	},
	// 	items_remove(frm,cdt,cdn){ // items is the child table fieldname so here you put your childtable-fieldname_remove
	// 		frm.script_manager.trigger('qty', cdt,cdn)
	// 	}
		
	// })


	frappe.ui.form.on("Parts Request CT", {
		qty:function(frm,cdt, cdn){
			let row= locals[cdt][cdn]
			console.log(row)
			let total=0
			for(let i in frm.doc.items){
				total += frm.doc.items[i].qty
			}
		  
			frm.set_value('total_parts',total)
			// console.log(total)
			frm.refresh()
		},
		items:function(frm,cdt,cdn){
			frm.script_manager.trigger("qty",cdt,cdn)
			// console.log("test1")
		},
		items_remove(frm,cdt,cdn){
			frm.script_manager.trigger('qty',cdt,cdn)
			// console.log("test2")
			
		}
		
	})

	frappe.ui.form.on('General Request CT', {
		qty:function(frm,cdt,cdn){
				let row = locals[cdt][cdn]
				console.log(row)
				let total=0
				for (let i in frm.doc.item){
					total += frm.doc.item[i].qty
				}
				frm.set_value('total_generals',total)
				frm.refresh()
			},
			item:function(frm,cdt,cdn){
				frm.script_manager.trigger('qty',cdt,cdn)
				console.log(1)
			},
			item_remove(frm,cdt,cdn){
				frm.script_manager.trigger('qty',cdt,cdn)
				console.log(2)
			}
	})