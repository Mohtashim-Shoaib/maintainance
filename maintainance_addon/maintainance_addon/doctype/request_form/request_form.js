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

