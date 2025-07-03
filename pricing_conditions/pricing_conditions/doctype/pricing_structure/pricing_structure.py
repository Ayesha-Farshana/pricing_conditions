# Copyright (c) 2025, Ayesha-Farshana and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class PricingStructure(Document):
# 	pass


import frappe
from frappe.model.document import Document
from frappe.utils.safe_exec import safe_eval


def dispatch_pricing_if_needed(doc, method):
    structures = frappe.get_all("Pricing Structure", filters={
        "reference_doctype": doc.doctype
    }, order_by="creation desc", limit=1)

    if not structures:
        return

    structure_doc = frappe.get_doc("Pricing Structure", structures[0].name) #currently took 1
    structure_doc.apply_pricing(doc)


class PricingStructure(Document):
    def apply_pricing(self, doc):
        """Apply pricing logic to parent or child rows"""
        if self.child_table_field:
            # Child-level application
            table = getattr(doc, self.child_table_field, []) #getattr ( will fetch the row details)
            for row in table:
                result = self.evaluate(runtime_doc=doc, row=row)
                target = self.child_target_field
                if target and hasattr(row, target):
                    setattr(row, target, result.get("final_price"))
        else:
            # Parent-level application
            result = self.evaluate(runtime_doc=doc)
            if self.target_field and hasattr(doc, self.target_field):
                setattr(doc, self.target_field, result.get("final_price"))

    def evaluate(self, runtime_doc=None, row=None):
        ctx = {}

        # Inject parent doc and optional child row into context
        if runtime_doc:
            ctx.update(runtime_doc.as_dict())
        if row:
            ctx.update(row.as_dict())
            ctx['row'] = row.as_dict()
        ctx['doc'] = runtime_doc.as_dict() if runtime_doc else {}

        total = 0
        applied_components = {}

        for row_ref in self.sequence:
            try:
                component = frappe.get_doc("Pricing Component", row_ref.pricing_component) 
                label_key = component.label.strip().lower().replace(" ", "_") #can use variable name too since we have include it in doctype

                # Dynamic variable logic
                if component.is_dynamic and component.api_function and component.variable_name:
                    try:
                    
                        # only done for ui APIs but can extend to whitlist method
                        script = frappe.get_doc("Server Script", component.api_function)
                        if script.disabled:
                            frappe.throw(_("Server Script {0} is disabled").format(component.api_function))

                        frappe.local.form_dict.doc = runtime_doc 
                        frappe.local.form_dict.row = row

                        dynamic_value = script.execute_method()
                        ctx[component.variable_name] = dynamic_value
                    except Exception as e:
                        frappe.log_error(f"Dynamic API error in '{component.label}': {e}")
                        continue

                # Condition evaluation
                apply = True
                if component.condition:
                    try:
                        apply = safe_eval(component.condition, ctx)  #safe evaal from slaary slip code
                    except Exception as e:
                        frappe.log_error(f"Condition error in '{component.label}': {e}")
                        apply = False

                if not apply:
                    continue

                # Formula or constant
                amount = 0
                if component.formula:
                    try:
                        amount = safe_eval(component.formula, ctx)
                    except Exception as e:
                        frappe.log_error(f"Formula error in '{component.label}': {e}")
                        amount = 0
                elif component.constant is not None:
                    amount = component.constant

                ctx[label_key] = amount
                total += amount
                applied_components[component.label] = amount

            except Exception as e:
                frappe.log_error(f"Component evaluation failed: {e}")
                continue

        self.final_price = total
        ctx["final_price"] = total

        return {
            "final_price": total,
            "components": applied_components,
            "context": ctx
        }
