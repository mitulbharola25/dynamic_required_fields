from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccessRequiredFields(models.Model):
    _name = 'access.required.fields'
    _description = "Access Required Fields"
    _rec_name = "model_id"

    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        ondelete="cascade", store=True  # ✅ Fixed issue
    )
    field_id = fields.Many2many(
        "ir.model.fields",
        string="Field",
        ondelete="cascade", store=True # ✅ Fixed issue
    )
    is_required = fields.Boolean(string="Is Required", default=True)

    @api.constrains('model_id', 'field_id')
    def _check_unique_field(self):
        for record in self:
            existing = self.search([
                ('model_id', '=', record.model_id.id),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(_("This field is already set as required for the selected model."))
            else:
                pass


class BaseModel(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _get_required_fields(self):
        """Fetch required fields for the current model dynamically."""
        required_fields = self.env["access.required.fields"].search([
            ("model_id.model", "=", self._name),
            ("is_required", "=", True)
        ])
        return {field.name: field.field_description for field in required_fields.field_id}

    @api.model_create_multi
    def create(self, vals_list):
        """Validate required fields before creating a record."""
        for vals in vals_list:
            if self._context.get("default_get"):  # ✅ Ignore validation when opening a new form
                continue

            required_fields = self._get_required_fields()
            missing_fields = []  # ✅ Collect missing fields

            for field_name, field_description in required_fields.items():
                if field_name in self._fields and not vals.get(field_name):  # Field is empty
                    missing_fields.append(f"➡ {field_description} (`{field_name}`)")  # 🔹 Format message

            if missing_fields:
                raise ValidationError(
                    _("The following required fields must be filled:\n%s") % "\n".join(missing_fields)
                )

        return super().create(vals_list)

    def write(self, vals):
        """Validate required fields before updating a record."""
        if not vals:
            return super().write(vals)

        required_fields = self._get_required_fields()
        missing_fields = []  # ✅ Collect missing fields

        for field_name, field_description in required_fields.items():
            if field_name in self._fields:
                new_value = vals.get(field_name, self[field_name])  # ✅ Check new value or existing value

                # ✅ Ignore validation in list view (prevents errors on 'New' button click)
                if not new_value and self.env.context.get("params", {}).get("view_type") == "list":
                    continue

                if not new_value:
                    missing_fields.append(f"➡ {field_description} (`{field_name}`)")  # 🔹 Format message

        if missing_fields:
            raise ValidationError(
                _("The following required fields must be filled:\n%s") % "\n".join(missing_fields)
            )

        return super().write(vals)

