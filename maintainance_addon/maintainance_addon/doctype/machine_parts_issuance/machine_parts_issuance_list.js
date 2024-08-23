frappe.listview_settings["Machine Parts Issuance"] = {
    add_fields: ["status"],

    get_indicator: function(doc) {
        if (doc.status == "In Progress") {
            return [__('In Progress'), 'blue'];
        }
        if (doc.status == "Completed") {
            return [__('Completed'), 'green'];
        }
        else if (doc.status == "Draft") {
            return [__('Draft'), 'green'];
        }
       
    }
};
