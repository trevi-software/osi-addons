# Copyright (c) 2019 Open Source Integrators
# Copyright (C) 2019 Konos
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    motive_id = fields.Many2one(
        "helpdesk.ticket.motive", string="Motive", help="Motive")

    @api.multi
    @api.onchange('team_id', 'user_id')
    def _onchange_motive(self):
        self.motive_id = False
