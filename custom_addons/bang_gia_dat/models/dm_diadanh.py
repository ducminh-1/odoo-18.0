from odoo import models, fields

class TinhThanh(models.Model):
    _name = 'dm.tinhthanh'
    _description = 'Tỉnh / Thành phố'
    name = fields.Char(string="Tên tỉnh/thành", required=True)

class QuanHuyen(models.Model):
    _name = 'dm.quanhuyen'
    _description = 'Quận / Huyện'
    name = fields.Char(string="Tên quận/huyện", required=True)
    tinh_thanh_id = fields.Many2one('dm.tinhthanh', string="Thuộc tỉnh/thành")

class XaPhuong(models.Model):
    _name = 'dm.xaphuong'
    _description = 'Xã / Phường'
    name = fields.Char(string="Tên xã/phường", required=True)
    quan_huyen_id = fields.Many2one('dm.quanhuyen', string="Thuộc quận/huyện")
    tinh_thanh_id = fields.Many2one('dm.tinhthanh', string="Thuộc tỉnh/thành")
    merged_from = fields.Char(string="Gộp từ các xã cũ")
