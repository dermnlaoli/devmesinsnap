from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class DataInspector(models.Model):
    _name = 'data.inspector'
    _description = 'Data Inspector'

    nama = fields.Char(string="Nama", required=True)
    tanggal = fields.Datetime(string="Tanggal", readonly=True, required=True, default=fields.Datetime.now)
    shift = fields.Selection([
        ('1', 'Shift 1'),
        ('2', 'Shift 2'),
        ('3', 'Shift 3')
    ], string='Shift', required=True)

    putaran = fields.Selection([
            ('1', 'Putaran 1'),
            ('2', 'Putaran 2'),
            ('3', 'Putaran 3')
        ], string='Putaran', required=True)

    block_id = fields.Many2one('blok.mesin.urw', string='Block')
    
    @api.model
    def create(self, values):
        # Menghapus nilai `block` sebelum membuat catatan baru
        values['block_id'] = ''
        return super(DataInspector, self).create(values)
        
    deret = fields.Char(string="Deret")

    snap_qc_line = fields.One2many('data.snap.qc.line', 'snap_qc_id')
    mesin_id = fields.Many2one('data.mesin.urw', string="No Mesin")
    block_id = fields.Many2one('blok.mesin.urw', string="Blok Mesin")
    putus_pakan=fields.Boolean(string='Putus Pakan')
    putus_lusi = fields.Boolean(string="Putus Lusi")
    naik_beam = fields.Boolean(string="Naik Beam")
    hb = fields.Boolean(string="Habis Beam / Beam Baru")
    troble_kualitas = fields.Boolean(string="Trouble Kualitas")
    tunggu_beam_cucuk = fields.Boolean(string="Tunggu Beam/Cucuk")
    pick_finding = fields.Boolean(string="Pick Finding")
    troble_mekanik = fields.Boolean(string="Trouble Mekanik")
    troble_elektrik = fields.Boolean(string="Trouble Elektrik")
    tunggu_konfirmasi = fields.Boolean(string="Tunggu Konfirmasi")
    preventif = fields.Boolean(string="Preventif")
    pakan_habis = fields.Boolean(string="Pakan Habis")
    ambrol = fields.Boolean(string="Ambrol")
    dedel=fields.Boolean(string="Dedel")
    rantas=fields.Boolean(string="Rantas")
    oh = fields.Boolean(string="Over Houle")
    bendera_merah = fields.Boolean(string="Bendera Merah")
    bendera_biru = fields.Boolean(string="Bendera Biru") 
    rpm = fields.Integer(string='RPM')
    keterangan = fields.Text(string="Lain Lain")  
        
    def name_get(self):
        result = []
        for record in self:
            nama = record.nama 
            result.append((record.id, nama))
        return result
    
    hitung_mesin = fields.Integer(string='Mesin', compute='_compute_hitung_mesin', store=True)

    @api.depends('snap_qc_line')
    def _compute_hitung_mesin(self):
        for inspector in self:
            inspector.hitung_mesin = len(inspector.snap_qc_line)
            
    total_mesin = fields.Integer(string='Total Mesin', compute='_compute_total_mesin', store=True)

    @api.depends('mesin_id')  # Pastikan untuk menambahkan field yang dibutuhkan di sini
    def _compute_total_mesin(self):
        for inspector in self:
            mesin_model = self.env['data.mesin.urw']
            inspector.total_mesin = mesin_model.search_count([])  # Mengambil jumlah total mesin dari model data.mesin.urw

    persentase = fields.Float(string="Persentase Diperiksa", compute='_compute_persentase', store=True)

    @api.depends('snap_qc_line')
    def _compute_persentase(self):
        for inspector in self:
            total_mesin = inspector.total_mesin
            mesin_terinspeksi = len(inspector.snap_qc_line)
            print(f"Total Mesin: {total_mesin}, Mesin Terinspeksi: {mesin_terinspeksi}")
            if total_mesin > 0:
                inspector.persentase = (mesin_terinspeksi / total_mesin)
            else:
                inspector.persentase = 0.0
            print(f"Percentage Inspected: {inspector.persentase}")


    # total_mesin = fields.Integer(string="Total Mesin", compute='_compute_total_mesin', store=True)

    # @api.depends('mesin_id')
    # def _compute_total_mesin(self):
    #     for inspector in self:
    #         inspector.total_mesin = len(inspector.mesin_id)
    
    hitung_putus_pakan = fields.Integer(string="Putus Pakan Count", compute='_compute_hitung_putus_pakan', store=True)

    @api.depends('snap_qc_line.putus_pakan')
    def _compute_hitung_putus_pakan(self):
        for inspector in self:
            inspector.hitung_putus_pakan = sum(1 for line in inspector.snap_qc_line if line.putus_pakan)

    hitung_putus_lusi = fields.Integer(string="Putus Lusi Count", compute='_compute_hitung_putus_lusi', store=True)

    @api.depends('snap_qc_line.putus_lusi')
    def _compute_hitung_putus_lusi(self):
        for inspector in self:
            inspector.hitung_putus_lusi = sum(1 for line in inspector.snap_qc_line if line.putus_lusi)

    hitung_ambrol = fields.Integer(string="Ambrol Count", compute='_compute_hitung_ambrol', store=True)

    @api.depends('snap_qc_line.ambrol')
    def _compute_hitung_ambrol(self):
        for inspector in self:
            inspector.hitung_ambrol = sum(1 for line in inspector.snap_qc_line if line.ambrol)

    hitung_dedel = fields.Integer(string="Dedel Count", compute='_compute_hitung_dedel', store=True)

    @api.depends('snap_qc_line.dedel')
    def _compute_hitung_dedel(self):
        for inspector in self:
            inspector.hitung_dedel = sum(1 for line in inspector.snap_qc_line if line.dedel)

    hitung_rantas = fields.Integer(string="Rantas Count", compute='_compute_hitung_rantas', store=True)

    @api.depends('snap_qc_line.rantas')
    def _compute_hitung_rantas(self):
        for inspector in self:
            inspector.hitung_rantas = sum(1 for line in inspector.snap_qc_line if line.rantas)

    hitung_preventif = fields.Integer(string="Preventif Count", compute='_compute_hitung_preventif', store=True)

    @api.depends('snap_qc_line.preventif')
    def _compute_hitung_preventif(self):
        for inspector in self:
            inspector.hitung_preventif = sum(1 for line in inspector.snap_qc_line if line.preventif)

    hitung_oh = fields.Integer(string="OH Count", compute='_compute_hitung_oh', store=True)

    @api.depends('snap_qc_line.oh')
    def _compute_hitung_oh(self):
        for inspector in self:
            inspector.hitung_oh = sum(1 for line in inspector.snap_qc_line if line.oh)
    
    hitung_naik_beam = fields.Integer(string="Naik Beam Count", compute='_compute_hitung_naik_beam', store=True)

    @api.depends('snap_qc_line.naik_beam')
    def _compute_hitung_naik_beam(self):
        for inspector in self:
            inspector.hitung_naik_beam = sum(1 for line in inspector.snap_qc_line if line.naik_beam)

    hitung_hb = fields.Integer(string="HB Count", compute='_compute_hitung_hb', store=True)

    @api.depends('snap_qc_line.hb')
    def _compute_hitung_hb(self):
        for inspector in self:
            inspector.hitung_hb = sum(1 for line in inspector.snap_qc_line if line.hb)

    hitung_bendera_merah = fields.Integer(string="Bendera Merah Count", compute='_compute_hitung_bendera_merah', store=True)

    @api.depends('snap_qc_line.bendera_merah')
    def _compute_hitung_bendera_merah(self):
        for inspector in self:
            inspector.hitung_bendera_merah = sum(1 for line in inspector.snap_qc_line if line.bendera_merah)


class SnapQcLine(models.Model):
    _name='data.snap.qc.line'
    _description='Hasil Snap'

    snap_qc_id = fields.Many2one('data.inspector', string='Snap QC', ondelete='cascade', index=True, copy=False)
    mesin = fields.Many2one('data.mesin.urw', string='Mesin')

    putus_pakan=fields.Boolean(string='Putus Pakan')
    putus_lusi = fields.Boolean(string="Putus Lusi")
    ambrol = fields.Boolean(string="Ambrol")
    dedel=fields.Boolean(string="Dedel")
    rantas=fields.Boolean(string="Rantas")
    preventif = fields.Boolean(string="Preventif")
    oh = fields.Boolean(string="Over Houle")
    naik_beam = fields.Boolean(string="Naik Beam")
    hb = fields.Boolean(string="Habis Beam / Beam Baru")
    bendera_merah = fields.Boolean(string="Bendera Merah")
    keterangan = fields.Text(string="Lain Lain")
    
    


    




    

    
  
