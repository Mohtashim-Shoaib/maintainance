frappe.listview_settings["Request Form"] = {
    add_fields: ["status", "per_ordered1", "per_received"],

    get_indicator: function(doc) {
        if (doc.status === "Initialize") {
            return [__("Initialize"), "green", "status,=,Initialize"];
        }
        if (doc.status === "In Progress") {
            return [__("In Progress"), "blue", "status,=,In Progress"];
        }
        if (doc.status == "Closed") {
            return [__("Closed"), "yellow", "status,=,Closed"];
        }
        if (doc.status === "Completed") {
            return [__("Completed"), "green", "status,=,Completed"];
        }
        if (doc.status === "Stopped") {
            return [__("Stopped"), "red", "status,=,Stopped"];
        }
        if (doc.status === "Cancelled") {
            return [__("Cancelled"), "red", "status,=,Cancelled"];
        }
        if (doc.status === "Ordered") {
            return [__("Ordered"), "green", "status,=,Ordered"];
        }
        if (doc.status === "Not Started") {
            return [__("Not Started"), "orange", "status,=,Not Started"];
        }
        if (doc.status === "In Transit") {
            return [__("In Transit"), "yellow", "status,=,In Transit"];
        }
        if (doc.status === "Pending") {
            return [__("Pending"), "orange", "status,=,Pending"];
        }
        if (doc.status === "Partially Received") {
            return [__("Partially Received"), "yellow", "status,=,Partially Received"];
        }
        if (doc.status === "Received") {
            return [__("Received"), "green", "status,=,Received"];
        }
        if (doc.status === "Transferred") {
            return [__("Transferred"), "green", "status,=,Transferred"];
        }
        if (doc.status === "Issued") {
            return [__("Issued"), "green", "status,=,Issued"];
        }
        if (doc.status === "Manufactured") {
            return [__("Manufactured"), "green", "status,=,Manufactured"];
        }
        if (doc.status === "Partially Ordered") {
            return [__("Partially Ordered"), "green", "status,=,Partially Ordered"];
        }
    }
};
