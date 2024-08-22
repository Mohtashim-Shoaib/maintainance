frappe.listview_settings["General Item Issuance"] = {
    add_fields: [
        "status",
        "date",
        "user",
        "total_requested",
        "total_issued",
        "qty_to_provided"
    ],
    get_indicator: function(doc) {
    console.log('Document Status:', doc.status); // Debugging line
    const status_colors = {
        "Draft": "orange",
        "In Progress": "red",
        "Completed": "green",
        "":""
    };
    return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
    // if (status_colors[doc.status]) {
    //     return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
    // } 
    // else {
    //     return [__("Unknown"), "darkgray", "status,=," + doc.status];
    // }
}

};
