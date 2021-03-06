# -*- coding: utf-8 -*-
import time

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import netsvc

'''
class apl_mro_defect_type(osv.osv):
    _name='uis.papl.defect.type'
    _description='Transformer Types'
    name=fields.Char(string='Name')
    f_apl=fields.Boolean(string='APL')
    f_pillar=fields.Boolean(string="Pillar")
    f_trans=fields.Boolean(string="Pillar")
  '''  
class apl_mro_defect(osv.osv):
    """
    Defects
    """
    _name = 'uis.papl.mro.defect'
    _description = 'Defects'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    STATE_SELECTION = [
        ('draft', 'DRAFT'),
        ('confirmed', 'CONFIRMED'),
        ('planed', 'PLANED'),
        ('work', 'WORK'),
        ('done', 'DONE'),
        ('cancel', 'CANCELED')
    ]

    DEFECT_CATEGORY = [
        ('0', 'No Category'),
        ('1', 'Critical'),
        ('2', 'Normal'),
        ('3', 'Not critical')
    ]
    def _defect_total_labor(self,cr,uid,ids,field_name,arg,context=None):
        res =dict.fromkeys(ids,0)
        for defect in self.browse(cr,uid,ids,context=context):
            res[defect.id]=defect.labor_cost*defect.qnty
        return res
    
    _columns = {
        'number': fields.char('Defect No', readonly=True),
        'name': fields.char('Defect name', size=64),
        #'defect_type':fields.many2one('uis.papl.mro.defect.type','Defect type',required=False, readonly=True, states={'draft': [('readonly', False)]}),
        'apl_id': fields.many2one('uis.papl.apl', 'Air power line', readonly=True, required=False, states={'draft': [('readonly', False)]}),
        'tap_id': fields.many2one('uis.papl.tap', 'Tap of APL', required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'pillar_id': fields.many2one('uis.papl.pillar', 'Pillar',required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'transformer_id': fields.many2one('uis.papl.transformer','Transformer',required=False, readonly=True, domain="[('apl_id','in',[apl_id])]",states={'draft':[('readonly',False)]}),
        'unicode': fields.char('UniCode'),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True),
        'category': fields.selection(DEFECT_CATEGORY,'Category', readonly=True),
        'qnty':fields.integer('Qnt'),
        'labor_cost':fields.integer('Labor Cost per defect'),
        'total_labor_cost':fields.function(_defect_total_labor, string='Total laborcost', type='integer'),
        'defect_description': fields.text('Defect Description'),
    }
    _defaults = {
        'state': lambda *a: 'draft',
        'qnty':1,
        'category': lambda *a: '2'
    }