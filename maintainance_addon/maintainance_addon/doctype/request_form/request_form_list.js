frappe.listview_settings["Request Form"] = {
    add_fields: ["status","per_ordered1","per_received"],

    get_indicator: function(doc) {
        if (doc.status == "In Progress") {
            return [__('In Progress'), 'blue'];
        }
        if (doc.status == "Completed") {
            return [__('Completed'), 'green'];
        }
        else if (doc.status == "Draft") {
            return [__('Initilize'), 'red'];
        }
        else if (doc.status == "Stopped"){
            return [__("Stopped"), "red"];
        }
        else if (doc.status == "Cancelled"){
            return [__("Cancelled"), "red"];
        }
        else if (doc.status == "Ordered"){
             return [__('Ordered'), 'green'];
        }
        else if (doc.status == "Not Started"){
             return [__("Not Started"), "orange"];
        }
        else if (doc.status == "In Transit"){
            return [__("In Transit"), "yellow"];
        }
        else if (doc.status == "Not Started"){
             return [__("Not Started"), "orange"];
        }
        else if (doc.status == "In Transit"){
            return [__("In Transit"), "yellow"];
        }
        else if (doc.status == "Completed"){
            return [__("Completed"), "green"];
        }
        else if (doc.status == "Pending"){
            return [__("Pending"), "orange"];
        }
        else if (doc.status == "Partially Received"){
            return [__("Partially Received"), "yellow"];
        }
        else if (doc.status == "Received"){
            return [__("Received"), "green"];
        }
        else if (doc.status == "Ordered"){
            return [__("Ordered"), "green"];
        }
        else if (doc.status == "Transferred"){
           return [__("Transfered"), "green"];
        }
        else if (doc.status == "Partially Received"){
            return [__("Partially Received"), "yellow"];
        }
        else if (doc.status == "Issued"){
            return [__("Issued"), "green"];
        }
        else if (doc.status == "Received"){
            return [__("Received"), "green"];
        }
        else if (doc.status == "Manufactured"){
            return [__("Manufactured"), "green"];
        }
        else if (doc.status == "Partially Ordered"){
            return [__("Partially Ordered"), "green"];
        }
    }
};
