frappe.listview_settings["Machine Parts Issuance"] = {
    add_fields: [
        "date",
        "user",
        "total_requested_item",
        "total_issued_item",
        "status",
        "qty_to_be_provided"
    ],

    get_indicator: function(doc) {
        const status_colors = {
            "Draft": "gray",
            "In Progress": "red",
            "Completed": "green",
            "Cancelled": "gray"
        };
        return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
    //     if (status_colors[doc.status]) {
    //         return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
    //     } else {
    //         return [__("Unknown"), "darkgray", "status,=," + doc.status];
    //     }
    }
};
