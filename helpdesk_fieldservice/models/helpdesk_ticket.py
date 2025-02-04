# Copyright (C) 2021 - TODAY, Open Source Integrators
# Copyright (C) 2021 Pavlov Media
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    fsm_order_ids = fields.One2many("fsm.order", "ticket_id", string="Service Orders")
    fsm_location_id = fields.Many2one("fsm.location", string="FSM Location")

    all_orders_closed = fields.Boolean(compute="_compute_all_closed", store=True)

    @api.depends("fsm_order_ids", "stage_id", "fsm_order_ids.stage_id")
    def _compute_all_closed(self):
        for ticket in self:
            ticket.all_orders_closed = True
            if ticket.fsm_order_ids:
                for order in ticket.fsm_order_ids:
                    if order.stage_id.name not in ["Closed", "Cancelled"]:
                        ticket.all_orders_closed = False
            else:
                ticket.all_orders_closed = False

    def write(self, vals):
        if "stage_id" in vals:
            ticket_stage = self.env["helpdesk.stage"].browse(vals.get("stage_id"))
            if ticket_stage.is_close:
                for ticket in self:
                    if ticket.fsm_order_ids:
                        open_orders = ticket.fsm_order_ids.filtered(
                            lambda x: x.stage_id.is_closed
                        )
                        if open_orders and len(open_orders.ids) != len(
                            ticket.fsm_order_ids
                        ):
                            raise ValidationError(
                                _(
                                    "Please complete all service orders "
                                    "related to this ticket to close it."
                                )
                            )
        return super(HelpdeskTicket, self).write(vals)

    def _location_contact_fill(self, loc):
        """loc is a boolean that lets us know if this is coming from the
        partner onchange or the location onchange"""
        if loc:
            if self.fsm_location_id and self.partner_id:
                if self.partner_id.service_location_id != self.fsm_location_id:
                    self.partner_id = False
        else:
            if self.partner_id:
                if not self.fsm_location_id:
                    self.fsm_location_id = self.partner_id.service_location_id

    @api.onchange("fsm_location_id")
    def _onchange_fsm_location_id_partner(self):
        if self.fsm_location_id:
            self._location_contact_fill(True)
            if self.fsm_location_id and not self.partner_id:
                return {
                    "domain": {
                        "partner_id": [
                            ("service_location_id", "=", self.fsm_location_id.name)
                        ]
                    }
                }
        else:
            return {"domain": {"partner_id": [("id", "!=", None)]}}

    @api.onchange("partner_id")
    def _onchange_partner_id_location(self):
        if self.partner_id:
            self._location_contact_fill(False)

    def action_create_order(self):
        """
        This function returns an action that displays a full FSM Order
        form when creating an FSM Order from a ticket.
        """
        action = self.env.ref("fieldservice.action_fsm_operation_order")
        result = action.read()[0]
        # override the context to get rid of the default filtering
        result["context"] = {
            "default_ticket_id": self.id,
            "default_priority": self.priority,
            "default_location_id": self.fsm_location_id.id,
            "default_origin": self.name,
        }
        res = self.env.ref("fieldservice.fsm_order_form", False)
        result["views"] = [(res and res.id or False, "form")]
        return result
