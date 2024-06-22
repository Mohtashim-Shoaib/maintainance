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

