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