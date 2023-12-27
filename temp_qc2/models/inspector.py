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
    
    hitung_putus_pakan = fields.Integer(string="Putus Pakan Count", compute='_compute_hitung_putus_pakan', store=True)
    @api.depends('snap_qc_line.putus_pakan')
    def _compute_hitung_putus_pakan(self):
        for inspector in self:
            inspector.hitung_putus_pakan = sum(1 for line in inspector.snap_qc_line if line.putus_pakan)
    
    rata_rata_putus_pakan = fields.Float(string="Rata-rata Putus Pakan", compute='_compute_rata_rata_putus_pakan', store=True)
    @api.depends('snap_qc_line.putus_pakan', 'hitung_putus_pakan')
    def _compute_rata_rata_putus_pakan(self):
        for inspector in self:
            total_putus_pakan = inspector.hitung_putus_pakan
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_putus_pakan = round(total_putus_pakan / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_putus_lusi = fields.Integer(string="Putus Lusi Count", compute='_compute_hitung_putus_lusi', store=True)
    @api.depends('snap_qc_line.putus_lusi')
    def _compute_hitung_putus_lusi(self):
        for inspector in self:
            inspector.hitung_putus_lusi = sum(1 for line in inspector.snap_qc_line if line.putus_lusi)

    rata_rata_putus_lusi = fields.Float(string="Rata-rata Putus Lusi", compute='_compute_rata_rata_putus_lusi', store=True)
    @api.depends('snap_qc_line.putus_lusi', 'hitung_putus_lusi')
    def _compute_rata_rata_putus_lusi(self):
        for inspector in self:
            total_putus_lusi = inspector.hitung_putus_lusi
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_putus_lusi = round(total_putus_lusi / total_snap_qc_lines, 2) if total_snap_qc_lines else 0    

    hitung_ambrol = fields.Integer(string="Ambrol Count", compute='_compute_hitung_ambrol', store=True)
    @api.depends('snap_qc_line.ambrol')
    def _compute_hitung_ambrol(self):
        for inspector in self:
            inspector.hitung_ambrol = sum(1 for line in inspector.snap_qc_line if line.ambrol)

    rata_rata_ambrol = fields.Float(string="Rata-rata Ambrol", compute='_compute_rata_rata_ambrol', store=True)
    @api.depends('snap_qc_line.ambrol', 'hitung_ambrol')
    def _compute_rata_rata_ambrol(self):
        for inspector in self:
            total_ambrol = inspector.hitung_ambrol
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_ambrol = round(total_ambrol / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_dedel = fields.Integer(string="Dedel Count", compute='_compute_hitung_dedel', store=True)
    @api.depends('snap_qc_line.dedel')
    def _compute_hitung_dedel(self):
        for inspector in self:
            inspector.hitung_dedel = sum(1 for line in inspector.snap_qc_line if line.dedel)

    rata_rata_dedel = fields.Float(string="Rata-rata Dedel", compute='_compute_rata_rata_dedel', store=True)
    @api.depends('snap_qc_line.dedel', 'hitung_dedel')
    def _compute_rata_rata_dedel(self):
        for inspector in self:
            total_dedel = inspector.hitung_dedel
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_dedel = round(total_dedel / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_rantas = fields.Integer(string="Rantas Count", compute='_compute_hitung_rantas', store=True)
    @api.depends('snap_qc_line.rantas')
    def _compute_hitung_rantas(self):
        for inspector in self:
            inspector.hitung_rantas = sum(1 for line in inspector.snap_qc_line if line.rantas)
    
    rata_rata_rantas = fields.Float(string="Rata-rata Rantas", compute='_compute_rata_rata_rantas', store=True)
    @api.depends('snap_qc_line.rantas', 'hitung_rantas')
    def _compute_rata_rata_rantas(self):
        for inspector in self:
            total_rantas = inspector.hitung_rantas
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_rantas = round(total_rantas / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_preventif = fields.Integer(string="Preventif Count", compute='_compute_hitung_preventif', store=True)
    @api.depends('snap_qc_line.preventif')
    def _compute_hitung_preventif(self):
        for inspector in self:
            inspector.hitung_preventif = sum(1 for line in inspector.snap_qc_line if line.preventif)
    
    rata_rata_preventif = fields.Float(string="Rata-rata Preventif", compute='_compute_rata_rata_preventif', store=True)
    @api.depends('snap_qc_line.preventif', 'hitung_preventif')
    def _compute_rata_rata_preventif(self):
        for inspector in self:
            total_preventif = inspector.hitung_preventif
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_preventif = round(total_preventif / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_oh = fields.Integer(string="OH Count", compute='_compute_hitung_oh', store=True)
    @api.depends('snap_qc_line.oh')
    def _compute_hitung_oh(self):
        for inspector in self:
            inspector.hitung_oh = sum(1 for line in inspector.snap_qc_line if line.oh)
    
    rata_rata_oh = fields.Float(string="Rata-rata OH", compute='_compute_rata_rata_oh', store=True)
    @api.depends('snap_qc_line.oh', 'hitung_oh')
    def _compute_rata_rata_oh(self):
        for inspector in self:
            total_oh = inspector.hitung_oh
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_oh = round(total_oh / total_snap_qc_lines,2) if total_snap_qc_lines else 0
    
    hitung_naik_beam = fields.Integer(string="Naik Beam Count", compute='_compute_hitung_naik_beam', store=True)
    @api.depends('snap_qc_line.naik_beam')
    def _compute_hitung_naik_beam(self):
        for inspector in self:
            inspector.hitung_naik_beam = sum(1 for line in inspector.snap_qc_line if line.naik_beam)
    
    rata_rata_naik_beam = fields.Float(string="Rata-rata Naik Beam", compute='_compute_rata_rata_naik_beam', store=True)
    @api.depends('snap_qc_line.naik_beam', 'hitung_naik_beam')
    def _compute_rata_rata_naik_beam(self):
        for inspector in self:
            total_naik_beam = inspector.hitung_naik_beam
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_naik_beam = round(total_naik_beam / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_hb = fields.Integer(string="HB Count", compute='_compute_hitung_hb', store=True)
    @api.depends('snap_qc_line.hb')
    def _compute_hitung_hb(self):
        for inspector in self:
            inspector.hitung_hb = sum(1 for line in inspector.snap_qc_line if line.hb)

    rata_rata_hb = fields.Float(string="Rata-rata HB", compute='_compute_rata_rata_hb', store=True)
    @api.depends('snap_qc_line.hb', 'hitung_hb')
    def _compute_rata_rata_hb(self):
        for inspector in self:
            total_hb = inspector.hitung_hb
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_hb = round(total_hb / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    hitung_bendera_merah = fields.Integer(string="Bendera Merah Count", compute='_compute_hitung_bendera_merah', store=True)
    @api.depends('snap_qc_line.bendera_merah')
    def _compute_hitung_bendera_merah(self):
        for inspector in self:
            inspector.hitung_bendera_merah = sum(1 for line in inspector.snap_qc_line if line.bendera_merah)

    rata_rata_bendera_merah = fields.Float(string="Rata-rata Bendera Merah", compute='_compute_rata_rata_bendera_merah', store=True)
    @api.depends('snap_qc_line.bendera_merah', 'hitung_bendera_merah')
    def _compute_rata_rata_bendera_merah(self):
        for inspector in self:
            total_bendera_merah = inspector.hitung_bendera_merah
            total_snap_qc_lines = len(inspector.snap_qc_line)
            inspector.rata_rata_bendera_merah = round(total_bendera_merah / total_snap_qc_lines, 2) if total_snap_qc_lines else 0

    
    
    total_rata_rata_snap = fields.Float(string="Total Rata-rata Snap", compute='_compute_total_rata_rata_snap', store=True)
    @api.depends('rata_rata_putus_lusi', 'rata_rata_ambrol', 'rata_rata_dedel', 'rata_rata_rantas',
        'rata_rata_preventif', 'rata_rata_oh', 'rata_rata_naik_beam', 'rata_rata_hb', 'rata_rata_bendera_merah')
    def _compute_total_rata_rata_snap(self):
        for inspector in self:
            total_rata_rata_snap = round(
                inspector.rata_rata_putus_lusi +
                inspector.rata_rata_ambrol +
                inspector.rata_rata_dedel +
                inspector.rata_rata_rantas +
                inspector.rata_rata_preventif +
                inspector.rata_rata_oh +
                inspector.rata_rata_naik_beam +
                inspector.rata_rata_hb +
                inspector.rata_rata_bendera_merah
            , 2)
            inspector.total_rata_rata_snap = total_rata_rata_snap

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
    
    


    




    

    
  
