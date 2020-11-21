# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

import logging

import time
from datetime import date
from datetime import datetime
from datetime import timedelta

from openerp import api, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _


_logger = logging.getLogger(__name__)

class app_date_default(osv.osv):
    _name = "app.date.default"
    _description = "App Default"
    _rec_name = "date_start"
    
    _columns = {
        'date_start': fields.date(string='Date From',
            help="Keep empty to use the current date", copy=False),
        'days': fields.integer('Days', required=True,),
        'date_end': fields.date('Date To', required=True, readonly=True, ),
    }
    
    _defaults = {
        'date_start': lambda *a: str(datetime.now())[:10],
    }

    def onchange_date(self, cr, uid, ids, date_start, days, context=None):
        date_start = datetime.strptime(date_start, "%Y-%m-%d")
        res = {
            'value': {
                'days': days,
                'date_end': date_start + timedelta(days=days),
            }
        }
        return res
    
    def create(self, cr, uid, data, context=None):
        date_start = datetime.strptime(data['date_start'], "%Y-%m-%d")
        days = data['days']
        data['date_end'] = date_start + timedelta(days=days)
        return super(app_date_default, self).create(cr, uid, data, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        date_id = self.browse(cr, uid, ids, context=context)
        if 'date_start' in vals and not 'days' in vals:
            date_start = datetime.strptime(vals['date_start'], "%Y-%m-%d")
            vals['date_end'] = date_start + timedelta(days=date_id.days)
        elif 'days' in vals and not 'date_start' in vals:
            date_start = datetime.strptime(date_id.date_start, "%Y-%m-%d")
            days = int(vals.get('days', 0))
            vals['date_end'] = date_start + timedelta(days=days)
        elif 'days' in vals and 'date_start' in vals:
            date_start = datetime.strptime(vals['date_start'], "%Y-%m-%d")
            days = int(vals.get('days', 0))
            vals['date_end'] = date_start + timedelta(days=days)
        return super(app_date_default, self).write(cr, uid, ids, vals, context=context)


