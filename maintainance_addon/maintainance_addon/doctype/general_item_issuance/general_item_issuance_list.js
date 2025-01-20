frappe.listview_settings["General Item Issuance"] = {
    add_fields: ["status"],
    get_indicator: function(doc) {
        if (doc.status == "In Progress") {
            return [__("In Progress"), 'yellow'];
        }
        if (doc.status == "Completed") {
            return [__('Completed'), 'green'];
        }
        if (doc.status == "Draft") {
            return [__('Draft'), 'red'];
        }
        if (doc.status == "Closed") {
            return [__('Closed'), 'yellow'];
        }
    }
};
