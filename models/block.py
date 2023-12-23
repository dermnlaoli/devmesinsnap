from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class BlokMesinUrw(models.Model):
    _name='blok.mesin.urw'
    _description='Blok Mesin Produksi'

    block = fields.Char(string='Nama Block')

    def name_get(self):
        result = []
        for record in self:
            block = record.block 
            result.append((record.id, block))
        return result