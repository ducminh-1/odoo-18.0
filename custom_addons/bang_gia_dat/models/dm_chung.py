from odoo import models, fields

class MatTienHem(models.Model):
    _name = 'dm.mattienhem'
    _description = 'Mặt tiền / Hẻm'
    name = fields.Char(string="Loại", required=True)

class DoRongHem(models.Model):
    _name = 'dm.doronghem'
    _description = 'Độ rộng hẻm'
    name = fields.Char(string="Loại", required=True)

class ChieuSau(models.Model):
    _name = 'dm.chieusau'
    _description = 'Chiều sâu lô đất'
    name = fields.Char(string="Loại", required=True)

class KetCauDuong(models.Model):
    _name = 'dm.ketcauduong'
    _description = 'Kết cấu đường'
    name = fields.Char(string="Loại", required=True)

class KhuVuc(models.Model):
    _name = 'dm.khuvuc'
    _description = 'Khu vực'
    name = fields.Char(string="Loại", required=True)

class ViTri(models.Model):
    _name = 'dm.vitri'
    _description = 'Vị trí'
    name = fields.Char(string="Loại", required=True)
