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

frappe.ui.form.on('Parts Request CT', {
	item_code(frm, cdt, cdn) {
		set_rate(frm, cdt, cdn);

	},
	qty(frm, cdt, cdn) {
		set_order(frm, cdt, cdn);

	}

});
function set_order(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.qty > d.balance_qty) {
		frappe.model.set_value(d.doctype, d.name, "required_qty", d.qty - d.balance_qty)
	}
	else {
		frappe.model.set_value(d.doctype, d.name, "required_qty", 0)
	}
}
function set_rate(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.call({
		method: "frappe.client.get_value",
		args: {
			doctype: "Item Price",
			filters: {
				item_code: d.part_name,
				price_list: "Standard Buying"
			},
			fieldname: ["price_list_rate"]
		},
		callback: function (r) {
			frappe.model.set_value(d.doctype, d.name, "rate", r.message["price_list_rate"])

		}
	});
}


frappe.ui.form.on('Request Form', {
	refresh: function (frm) {
		var me = frm
		frm.add_custom_button(__('Create MR'),
			function () {
				frappe.call({
					method: 'maintainance_addon.maintainance_addon.doctype.request_form.request_form.make_mr',
					args: {
						request_form: frm.doc.name
					},
					callback: function (r) {
						if (r.message) {
							frappe.msgprint(__('Items updated successfully.'));
							frm.reload_doc();
							console.log("test")
						}

					}
				});



			}, __("Create"));
		frm.add_custom_button(__('Parts Issuance'),
			function () {
				frappe.call({
					method: 'maintainance_addon.maintainance_addon.doctype.request_form.request_form.make_issuance',
					args: {
						request_form: frm.doc.name
					},
					callback: function (r) {
						if (r.message) {
							frappe.msgprint(__('Items updated successfully.'));
							frm.reload_doc();
						}
					}
				});



			}, __("Create"));
	}
});


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
			}, __("Set Values"), __("Get Stock"));
		});
	}
});

// Define the function to get available stock
function get_available_stock(frm, item_code) {
	console.log("Fetching available stock for item_code:", item_code);
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

