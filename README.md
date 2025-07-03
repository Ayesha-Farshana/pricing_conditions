### Pricing Conditions

Setup Pricing Structure for differnt Doctypes

A configurable, rule-based pricing system inspired by ERPNext's Salary Structure. Define pricing logic using formulas, constants, conditions, and dynamic server-side scripts — entirely through the UI.


### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app pricing_conditions
```

---

## 📦 Features

- Create reusable **Pricing Components**
- Group them using **Pricing Structures**
- Supports:
  - Constants
  - Conditional logic (e.g. `row.item_group == "Raw Material"`)
  - Safe formula evaluation
  - Dynamic values from Server Scripts
- Apply logic to:
  - Parent fields (e.g. `price_list_rate` on `Item Price`)
  - Child table fields (e.g. `rate` on `Sales Order Item`)

---
## 🧩 Step-by-Step Setup

### 1. Create Pricing Components

Navigate to **Pricing Component** and add components.

| Field            | Description                                               |
|------------------|-----------------------------------------------------------|
| Label            | Name of the component                                     |
| Constant         | Static number to apply (optional)                         |
| Condition        | (Optional) Python condition using `row.` or `doc.` fields |
| Formula          | Python-safe formula (e.g. `base_rate * 0.9`)              |
| Variable Name    | Variable inserted into the formula context (e.g. `royalty`) |
| Is Dynamic       | Check if this value comes from a Server Script            |
| API Function     | Name of the Server Script (type: API)                     |

> 💡 You can use dynamic values and formulas together in one component.
---

### 2. Create a Pricing Structure

Go to **Pricing Structure** and create a new structure.

| Field               | Description                                              |
|--------------------|----------------------------------------------------------|
| Reference Doctype  | Target Doctype (e.g. `Sales Order`)                      |
| Target Field       | Currency field in the parent document to update (optional) |
| Child Table Field  | Fieldname of the child table (e.g. `items`)              |
| Child Target Field | Currency field inside child row to update (e.g. `rate`)  |
| Components         | Add components in the correct order                      |

---
### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/pricing_conditions
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
