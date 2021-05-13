# -*- coding: utf-8 -*-
import io
import base64
import logging

import xlsxwriter
from xlsxwriter.workbook import Workbook

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, remove_accents
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _, tools


_logger = logging.getLogger(__name__)

class AppApp(models.Model):
    _name = "app.app"
    _description = "App"

    name = fields.Char(string='Name', required=True, translate=True)
    line_ids = fields.One2many(
        string="Lines",
        comodel_name="app.line",
        inverse_name="app_id", copy=False,)

    def action_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        f_name = '%s_%s' % (self._description, self.name)

        sheet = workbook.add_worksheet(self.name)
        sheet.write(0, 0, self.name, )

        workbook.close()
        xlsx_data = output.getvalue()
        export_id = self.env['app.file.wizard'].create(
            {'file':base64.encodestring(xlsx_data),
             'file_name':f_name + '.xlsx'})
        return {
            'view_mode':'form',
            'res_id':export_id.id,
            'res_model':'app.file.wizard',
            'view_type':'form',
            'type':'ir.actions.act_window',
            'target':'new',
        }


class AppLines(models.Model):
    _name = "app.line"
    _description = "App Line"

    app_id = fields.Many2one('app.app', string='App')
    partner_id = fields.Many2one('res.partner', string='Partner')
    amount = fields.Float(required=True, digits=(16, 4))