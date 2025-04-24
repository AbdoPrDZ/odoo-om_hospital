# Get Started in Odoo Development

## Create module

- Create a new custom odoo addons folder (ex: `C:/odoo/custom-addons`)
- Add the custom odoo addons to `addons_path` parameter in odoo config file (ex: `C:/odoo/odoo.conf`).
- Create a new odoo module inside the custom addons folder:
  - Automatically using terminal command:
    ```bash
    # Change directory to the custom addons directory
    $ cd C:/odoo/custom-addons
    # Create new module using `odoo-bin`
    $ python "C:/odoo/odoo-bin" scaffold my_module
    ```
  - Create files manually by following this tree:
    ```bash
    my_module/
    ├── __init__.py
    └── __manifest__.py
    ```
- Set module standard configures inside `__manifest__.py` file
  - Set Display `name` that shown in Apps list, Root menu, Settings and many other places:
  ```json
  {
    "name": "My Module"
  }
  ```
  - Set small `summary` description that explains the module:
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module."
  }
  ```
  - Set long `description` that explains the module functions, features...:
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development"
  }
  ```
  - Set the `author` of this module (ex: Github username):
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ"
  }
  ```
  - Set the `website`, (ex: your website, module repo, ...)
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module"
  }
  ```
  - Set the `category` of this module (note: see [ir_module_category_data.xml](https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml))
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module",
    "category": "Technical"
  }
  ```
  - Set a `version` for your module (ex: <odoo.version>.1.0.0)
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module",
    "category": "Technical",
    "version": "14.0.0.1.0.0"
  }
  ```
  <!-- - Set module `depends` as you need (uses for inhering models, views, ... from other modules)
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module",
    "category": "Technical",
    "version": "14.0.0.1.0.0",
    "depends": ["base", "web", "mail", "sale"]
  }
  ``` -->

## Activate Developer Mode

- Method 1: Goto to `Settings`◌`General Settings` then scroll down then click `Activate the developer mode`
- Method 2: Add url query parameter `http://localhost:8069/web?debug=1`.
- Method 3: Use `Odoo Debug` browser extension.

## Install The Module

- Restart the server if is running.
- Navigate `Apps` list.
- Update the apps list:
  - [Activate Developer Mode](#activate-developer-mode)
  - Click on `Update Apps List`.
- Search for module `name` or Technical Name (is a module directory name, ex: `my_module`) in search bar.
- Click on Install button.

## Upgrade The Module

- Restart the server if is running.
- Navigate `Apps` list.
- Search for module `name` or Technical Name (is a module directory name, ex: `my_module`) in search bar.
- Click on module menu and click Upgrade.

## Add Module Icon

- Create `my_module/static/description` directory and add `icon.png` image file.
  ```bash
  my_module/
  ├── models
  │   ├── __init__.py
  │   └── first_model.py
  ├── static
  │   └── description
  │       └── icon.png
  ├── __init__.py
  └── __manifest__.py
  ```
- [Install](#install-the-module) or [upgrade](#upgrade-the-module) the module
- Check if the icon is shown in Apps List.

## Create Models Security Access File

- Create `my_module/security/ir.model.access.csv` file
  ```bash
  my_module/
  ├── security
  │   └── ir.model.access.csv
  ├── static
  │   └── description
  │       └── icon.png
  ├── __init__.py
  └── __manifest__.py
  ```
- Set `my_module/security/ir.model.access.csv` file header fields:
  ```csv
  id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
  ```
- Add `my_module/security/ir.model.access.csv` to data in module `my_module/__manifest__.py` file inside data field
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module",
    "category": "Technical",
    "version": "14.0.0.1.0.0",
    "data": ["security/ir.model.access.csv"]
  }
  ```

## Create Model

- Create `my_module/models` directory if not exists
  ```bash
  my_module/
  ├── models
  ├── security
  │   └── ir.model.access.csv
  ├── static
  │   └── description
  │       └── icon.png
  ├── __init__.py
  └── __manifest__.py
  ```
- Create `my_module/models/__init__.py` file.
  ```bash
  my_module/
  ├── models
  │   └── __init__.py
  ├── security
  │   └── ir.model.access.csv
  ├── static
  │   └── description
  │       └── icon.png
  ├── __init__.py
  └── __manifest__.py
  ```
- Make sure to import models inside module `my_module/__init__.py` file:
  ```python
  from . import models
  ```
- Create `my_module/models/first_model.py` model file.
  ```bash
  my_module/
  ├── models
  │   ├── __init__.py
  │   └── first_model.py
  ├── security
  │   └── ir.model.access.csv
  ├── static
  │   └── description
  │       └── icon.png
  ├── __init__.py
  └── __manifest__.py
  ```
- Import the `first_model` file inside `__init__.py` file:
  ```python
  from . import first_model
  ```
- Define the model standard configuration

  ```python
  from odoo import models, fields, api

  class FirstModel(models.Model):
    _name = "First Model"
    _description = "This is a first model in my module"
  ```

- Define the model fields

  ```python
  from odoo import models, fields, api

  class FirstModel(models.Model):
    _name = "my_module.first_name"
    _description = "This is a first model in my module"

    field1 = fields.Char(string="Field 1", required=True)
    field2 = fields.Integer(string="Field 2", required=True, default="10")
    field3 = fields.Text(string="Field 3")
  ```

- Make sure to [set security access](#set-model-security-access) for this model.
- [Check if the model is exists](#check-if-a-model-is-exists)

## Set Model Security Access

- Make sure to [create models security access file](#create-models-security-access-file).
- Add Model access row:
  - Explain:
    | Header Field | Explain | Value Format |
    |--|--|--|
    | id | A unique identifier for the access control rule. Usually prefixed with access\_. | access\_<module\-name>\_<model_name> |
    | name | A readable name for the rule, typically using the module and model name. | <module_name>.<model_name> |
    | model_id:id | The external ID of the model this rule applies to, defined in ir.model. | <module_name>.model\_<model_name> |
    | group_id:id | (Optional) The group this rule applies to. Leave empty for global access. | <module_name>.group\_<group_name> or empty |
    | perm_read | Whether this group can read records from the model. | 1 (allowed) or 0 (denied) |
    | perm_write | Whether this group can edit records. | 1 (allowed) or 0 (denied) |
    | perm_create | Whether this group can create new records. | 1 (allowed) or 0 (denied) |
    | perm_delete | Whether this group can delete records. | 1 (allowed) or 0 (denied) |

## Check if a model is exists

- Reload the server if is running.
- Upgrade the module or install it.
- [Activate a developer mode](#activate-developer-mode).
- Go to `Settings`◌`Database structure`◌`Models`.
- Search in search bar by model `_name` or `_description`.

## Create Root Menu

- Create `views/menu.xml` menu file.
  ```bash
  my_module/
  ├── models
  │   ├── __init__.py
  │   └── first_model.py
  ├── security
  │   └── ir.model.access.csv
  ├── static
  │   └── description
  │       └── icon.png
  ├── views
  │   └── menu.xml
  ├── __init__.py
  └── __manifest__.py
  ```
- Define the `views/menu.xml` view in data field in `__manifest__` file:
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module",
    "category": "Technical",
    "version": "14.0.0.1.0.0",
    "data": ["security/ir.model.access.csv", "views/menu.xml"]
  }
  ```
- Add the `<menuitem>` tag and set the menu id, display `name`, display sequence and display icon.
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <menuitem id="menu_my_module_root"
        name="My Module"
        sequence="10"
        web_icon="my_module,/static/description/icon.png"/>
  </odoo>
  ```
  - (Optional) Make sure to add [module icon](#add-module-icon) module files

## Create Mode View Action

- [Create root menu](#create-root-menu).
- Create `views/model_view.xml` view file:
  ```bash
  my_module/
  ├── models
  │   ├── __init__.py
  │   └── first_model.py
  ├── security
  │   └── ir.model.access.csv
  ├── static
  │   └── description
  │       └── icon.png
  ├── views
  │   ├── menu.py
  │   └── model_view.py
  ├── __init__.py
  └── __manifest__.py
  ```
- Define the `views/model_view.xml` view in data field in `__manifest__` file:
  ```json
  {
    "name": "My Module",
    "summary": "First Odoo Module.",
    "description": "This just a test module to get starting in odoo module development",
    "author": "AbdoPrDZ",
    "website": "https://github.com/AbdoPrDZ/odoo-my_module",
    "category": "Technical",
    "version": "14.0.0.1.0.0",
    "data": [
      "security/ir.model.access.csv",
      "views/menu.xml",
      "views/model_view.xml"
    ]
  }
  ```
  - Note: Make sure to set the `views/menu.xml` before `views/model_view.xml`.
- Create Action for model view:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <record id="action_model_view" model="ir.actions.act_window">
      <field name="name">First Model</field>
      <field name="res_model">my_module.first_model</field>
      <field name="view_mode">tree,form,kanban</field>
      <field name="help" type="html">
        <p class="oe_view_nocontent_create">
          Click to create a new model item.
        </p>
        <p class="oe_view_nocontent_help">
          You can manage your model items here.
        </p>
      </field>
    </record>
  </odoo>
  ```
- [Create the submenu](#create-submenu-for-model-view-action) for this model view action.

## Create Submenu for Model view action

- Create the [model view action](#create-mode-view-action).

- Create Submenu in `views/model_view.xml` related to [root menu](#create-root-menu) with view action.
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <!-- Model View Action -->
    <record id="action_model_view" model="ir.actions.act_window">
      <field name="name">First Model</field>
      <field name="res_model">my_module.first_model</field>
      <field name="view_mode">tree</field>
      <field name="help" type="html">
        <p class="oe_view_nocontent_create">
          Click to create a new model item.
        </p>
        <p class="oe_view_nocontent_help">
          You can manage your model items here.
        </p>
      </field>
    </record>
    <!-- Model View Submenu -->
    <menuitem id="menu_my_module_root"
        name="My Module"
        sequence="20"
        parent="menu_my_module_root"
        action="action_model_view"/>
  </odoo>
  ```
  - Note: Make sure to put the action before the submenu.

## Create a custom tree view

- Create the [model view action](#create-mode-view-action).
- Make sure to add `tree` yo `view_mode` field.
- Create the `<record>` tag and set view `id`, `name`, `model` and display `fileds`.

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <!-- Tree View -->
    <record id="view_first_model_tree">
      <field name="name">my_module.first_model.tree</field>
      <field name="model">mymodule.first_model</field>
      <field name="arch" type="xml">
        <tree>
          <!-- Display Fields -->
          <field name="field1"/>
          <field name="field2"/>
        </tree>
      </field>
    </record>

    <!-- Model View Action -->
    <record id="action_model_view" model="ir.actions.act_window">
      <field name="name">First Model</field>
      <field name="res_model">my_module.first_model</field>
      <field name="view_mode">tree</field>
      <field name="help" type="html">
        <p class="oe_view_nocontent_create">
          Click to create a new model item.
        </p>
        <p class="oe_view_nocontent_help">
          You can manage your model items here.
        </p>
      </field>
    </record>
    <!-- Model View Submenu -->
    <menuitem id="menu_my_module_root"
        name="My Module"
        sequence="20"
        parent="menu_my_module_root"
        action="action_model_view"/>
  </odoo>
  ```

## Create a custom kanban view

- Create the [model view action](#create-mode-view-action).
- Make sure to add `tree` yo `view_mode` field.
- Create the `<record>` tag and set view `id`, `name`, `model` and display `fileds`.

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <!-- Tree View -->
    <record id="view_first_model_tree">
      <field name="name">my_module.first_model.tree</field>
      <field name="model">mymodule.first_model</field>
      <field name="arch" type="xml">
        <tree>
          <!-- Display Fields -->
          <field name="field1"/>
          <field name="field2"/>
        </tree>
      </field>
    </record>

    <!-- Model View Action -->
    <record id="action_model_view" model="ir.actions.act_window">
      <field name="name">First Model</field>
      <field name="res_model">my_module.first_model</field>
      <field name="view_mode">tree</field>
      <field name="help" type="html">
        <p class="oe_view_nocontent_create">
          Click to create a new model item.
        </p>
        <p class="oe_view_nocontent_help">
          You can manage your model items here.
        </p>
      </field>
    </record>
    <!-- Model View Submenu -->
    <menuitem id="menu_my_module_root"
        name="My Module"
        sequence="20"
        parent="menu_my_module_root"
        action="action_model_view"/>
  </odoo>
  ```

## Create a custom form view

- Create the [model view action](#create-mode-view-action).
- Make sure to add `form` yo `view_mode` field.
- Create the `<record>` tag and set view `id`, `name`, `model` and display `fileds`.

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <!-- Tree View -->
    <record id="view_first_model_tree">
      <field name="name">my_module.first_model.tree</field>
      <field name="model">mymodule.first_model</field>
      <field name="arch" type="xml">
        <tree>
          <!-- Display Fields -->
          <field name="field1"/>
          <field name="field2"/>
        </tree>
      </field>
    </record>

    <!-- Form View -->
    <record>
      <field name="name">my_module.first_model.form</field>
      <field name="model">mymodule.first_model</field>
      <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <group>
                <field name="field1"/>
                <field name="field2"/>
              </group>
              <group>
                <field name="field3"/>
              </group>
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <!-- Model View Action -->
    <record id="action_model_view" model="ir.actions.act_window">
      <field name="name">First Model</field>
      <field name="res_model">my_module.first_model</field>
      <field name="view_mode">tree,form,kanban</field>
      <field name="help" type="html">
        <p class="oe_view_nocontent_create">
          Click to create a new model item.
        </p>
        <p class="oe_view_nocontent_help">
          You can manage your model items here.
        </p>
      </field>
    </record>
    <!-- Model View Submenu -->
    <menuitem id="menu_my_module_root"
        name="My Module"
        sequence="20"
        parent="menu_my_module_root"
        action="action_model_view"/>
  </odoo>
  ```

## Hide element

```xml
<element-tag invisible="[('field', '=', 'value')]">
<element-tag invisible="[('field', '&gt;', 'value')]">
<element-tag invisible="[('field', '&lt;', 'value')]">
```

## Confirm before submitting

```xml
  <button id="my_button" type="object" name="my_function" confirm="Confirmation Message"/>
```

## Create a sequence

- Create `my_module/data/ir_sequence_data.xml` file and add it to `my_module/__manifest__.py`.
- Create a sequence in `<record>` tag.
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <odoo>
    <data>
      <record id="seq_my_module_first_model" model="ir.sequence">
        <field name="name">My Module First Model</field>
        <field name="code">my_module.seq_first_model</field>
        <field name="prefix">FM</field>
        <field name="padding">5</field>
        <field name="number_next">1</field>
      </record>
    </data>
  </odoo>
  ```
