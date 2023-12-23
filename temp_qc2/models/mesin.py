from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class DataMesinUrw(models.Model):
    _name = 'data.mesin.urw'
    _description = 'Mesin Produksi'

    inspector_id = fields.One2many('data.inspector', 'mesin_id')
    no_mesin = fields.Char(string="No Mesin")
    kode_kain = fields.Char(string="Kode Kain")
    block_id = fields.Many2one('blok.mesin.urw', string='Block')
    deret = fields.Char(string="Deret")

    def name_get(self):
        result = []
        for record in self:
            no_mesin = record.no_mesin 
            result.append((record.id, no_mesin))
        return result

