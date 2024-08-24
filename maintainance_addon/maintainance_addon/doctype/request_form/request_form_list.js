frappe.listview_settings["Request Form"] = {
    add_fields: ["status"],

    get_indicator: function(doc) {
        if (doc.status == "In Progress") {
            return [__('In Progress'), 'blue'];
        }
        if (doc.status == "Completed") {
            return [__('Completed'), 'green'];
        }
        else if (doc.status == "Draft") {
            return [__('Draft'), 'red'];
        }
       
    }
};
