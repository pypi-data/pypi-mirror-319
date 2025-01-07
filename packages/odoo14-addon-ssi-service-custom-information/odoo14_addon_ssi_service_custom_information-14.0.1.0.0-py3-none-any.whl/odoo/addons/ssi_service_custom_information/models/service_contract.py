# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.custom_info",
    ]
    _custom_info_create_page = True

    @api.onchange(
        "type_id",
    )
    def onchange_custom_info_template_id(self):
        self.custom_info_template_id = False
        if self.type_id:
            self.custom_info_template_id = self._get_template_custom_info()
