# ©  2008-2018 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import fields, models

import odoo.addons.base as base

GEO_VIEW = ("gmaps", "GMaps")

if "gmaps" not in base.models.ir_actions.VIEW_TYPES:
    base.models.ir_actions.VIEW_TYPES.append(GEO_VIEW)


class IrUIView(models.Model):
    _inherit = "ir.ui.view"

    type = fields.Selection(selection_add=[GEO_VIEW])

    def _get_view_info(self):
        return {'gmaps': {'icon': 'fa fa-map-marker'}} | super()._get_view_info()


class IrActionsActWindowView(models.Model):
    _inherit = "ir.actions.act_window.view"

    view_mode = fields.Selection(selection_add=[GEO_VIEW])

