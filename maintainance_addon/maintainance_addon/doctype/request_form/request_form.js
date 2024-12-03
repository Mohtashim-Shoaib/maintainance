frappe.ui.form.on('Request Form', {
    refresh(frm) {
        cur_frm.fields_dict["items"].grid.get_field("item_code").get_query = function (doc) {
            return {
                filters: {
                    "item_group": "General"
                }
            }
        };

        frm.add_custom_button(__('Get Available Stock'), () => {
            let fields = get_prompt_fields();
            frappe.prompt(fields, (values) => {
                get_available_stock(frm, values.item_code, values.qty);
                get_available_stock_1(frm, values.item_code, values.qty);
            }, __("Set Values"), __("Get Stock"));
        });
    }
});

var get_prompt_fields = () => {
    return [
        {
            label: __("Item Code"),
            fieldname: "item_code",
            fieldtype: "Link",
            options: "Item"
        },
        {
            label: __("Quantity"),
            fieldname: "qty",
            fieldtype: "Int"
        }
    ];
};

function get_available_stock(frm, item_code, qty) {
    frappe.db.get_doc("Item", item_code).then(doc => {
        var group = doc.item_group;
        const addItemToTable = (itemCode, balanceQty, qty) => {
            let child = frm.add_child("items", {
                "item_code": itemCode,
                "balance_qty": balanceQty ? balanceQty : 0,
                "qty": qty 
            });
            frm.refresh_field("items");
        };

        if (["MACHINE SPARE PARTS"].includes(group)) {
            frappe.call({
                method: "maintainance_addon.maintainance_addon.doctype.request_form.request_form.get_available_qty",
                args: { item_code: item_code },
                args: { item_code: item_code },
                callback: function (r) {
                    addItemToTable(item_code, r.message, qty);
                }
            });
        }
    });
}

function get_available_stock_1(frm, item_code, qty) {
    frappe.db.get_doc("Item", item_code).then(doc => {
        var group = doc.item_group;
        const addItemToTable = (itemCode, balanceQty, qty) => {
            let child = frm.add_child("item", {
                "item_code": itemCode,
                "balance_qty": balanceQty ? balanceQty : 0,
                "qty": qty 
            });
            frm.refresh_field("item");
        };

        if (["STATIONERY ITEMS", "GENERAL ITEM" , "ELECTRIC ITEMS", "TOOLS"].includes(group)) {
            frappe.call({
                method: "maintainance_addon.maintainance_addon.doctype.request_form.request_form.get_available_qty",
                args: { item_code: item_code },
                callback: function (r) {
                    addItemToTable(item_code, r.message, qty);
                }
            });
        }
    });
}

