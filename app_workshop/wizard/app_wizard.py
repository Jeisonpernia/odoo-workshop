# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccrualAccountingWizard(models.TransientModel):
    _name = 'app.file.wizard'
    _description = 'Create File Wizard.'

    file = fields.Binary('File', attachment=False, readonly=True)
    file_name = fields.Char('Name', readonly=True)
