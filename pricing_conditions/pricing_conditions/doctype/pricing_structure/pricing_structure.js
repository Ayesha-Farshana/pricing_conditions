// Copyright (c) 2025, Ayesha-Farshana and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Pricing Structure", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Pricing Structure', {
    reference_doctype: function (frm) {
        frappe.model.with_doctype(frm.doc.reference_doctype, function () {
            const meta = frappe.get_meta(frm.doc.reference_doctype);

            // Populate Currency fields for parent target field
            const currency_fields = meta.fields
                .filter(f => f.fieldtype === 'Currency')
                .map(f => f.fieldname);
           
            frm.set_df_property('parent_target_field', 'options', currency_fields.join('\n'));
            frm.refresh_field('parent_target_field');

            // Populate child table options
            const table_fields = meta.fields
                .filter(f => f.fieldtype === 'Table')
                .map(f => f.fieldname);

            frm.set_df_property('child_table_field', 'options', table_fields.join('\n'));
            frm.refresh_field('child_table_field');
        });
    },

    onload: function (frm) {
        if (frm.doc.reference_doctype) {
            frm.trigger('reference_doctype');
        }

        // If child_table_field already has value, trigger child_target_field logic
        if (frm.doc.child_table_field) {
            frm.trigger('child_table_field');
        }
    },

    child_table_field: function (frm) {
        if (!frm.doc.reference_doctype || !frm.doc.child_table_field) return;

        frappe.model.with_doctype(frm.doc.reference_doctype, function () {
            const parent_meta = frappe.get_meta(frm.doc.reference_doctype);
            const child_field = parent_meta.fields.find(
                f => f.fieldname === frm.doc.child_table_field && f.fieldtype === 'Table'
            );

            if (!child_field || !child_field.options) return;

            // Now load child table Doctype to extract its Currency fields
            frappe.model.with_doctype(child_field.options, function () {
                const child_meta = frappe.get_meta(child_field.options);
                const currency_fields = child_meta.fields
                    .filter(f => f.fieldtype === 'Currency')
                    .map(f => f.fieldname);

                frm.set_df_property('child_target_field', 'options', currency_fields.join('\n'));
                frm.refresh_field('child_target_field');
            });
        });
    }
});
