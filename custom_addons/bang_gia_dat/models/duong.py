from odoo import models, fields, api


class DuongGiaDat(models.Model):
    _name = 'duong.giadat'
    _description = 'Danh mục Đường phục vụ bảng giá đất'

    name = fields.Char(string="Tên đường")
    diem_dau = fields.Char(string="Từ điểm (A)")
    diem_cuoi = fields.Char(string="Đến điểm (B)")

    tinh_thanh_id = fields.Many2one('dm.tinhthanh', string="Tỉnh")
    quan_huyen_id = fields.Many2one('dm.quanhuyen', string="Thuộc huyện (cũ)")
    xa_phuong_ids = fields.Many2many('dm.xaphuong', 'duong_xaphuong_rel', 'duong_id', 'xaphuong_id', string="Thuộc xã/phường")

    gia_dat_hien_huu = fields.Float(string="Giá đất (đ/m²)", digits=(16, 0))
    gia_dat_du_kien = fields.Float(string="Giá dự kiến (đ/m²)", digits=(16, 0))

    doan_duong = fields.Char(
        string="Đoạn đường",
        compute="_compute_doan_duong",
        store=False
    )
    note = fields.Selection([
        ('hien_huu', 'Hiện hữu'),
        ('dieu_chinh', 'Điều chỉnh'),
        ('them_moi', 'Thêm mới'),
    ], string='Ghi chú')

    @api.depends('diem_dau', 'diem_cuoi')
    def _compute_doan_duong(self):
        for rec in self:
            if rec.diem_dau and rec.diem_cuoi:
                rec.doan_duong = f"({rec.diem_dau} - {rec.diem_cuoi})"
            else:
                rec.doan_duong = f"({rec.diem_dau})"

    @api.depends('name', 'diem_dau', 'diem_cuoi')
    def name_get(self):
        result = []
        for rec in self:
            if rec.diem_dau and rec.diem_cuoi:
                name = f"{rec.name or ''} ({rec.diem_dau or ''} - {rec.diem_cuoi or ''})"
            else:
                name = f"{rec.name or ''} ({rec.diem_dau or ''})"
            result.append((rec.id, name))
        return result

        # Quan hệ đoạn cũ (trước khi sát nhập)
    doan_cu_ids = fields.Many2many('duong.giadat',
                                   'duong_doan_mapping_rel',
                                   'doan_moi_id', 'doan_cu_id',
                                   string="Đoạn cũ")

    ghi_chu_chinh_sua = fields.Text(string="Ghi chú thay đổi", help="Mô tả lý do thay đổi, sát nhập...")
    ten_ke_thua = fields.Char(string="Kế thừa đoạn cũ", compute="_compute_ten_ke_thua")

    @api.depends('doan_cu_ids')
    def _compute_ten_ke_thua(self):
        for rec in self:
            rec.ten_ke_thua = ", ".join(rec.doan_cu_ids.mapped('name'))

    @api.constrains('doan_cu_ids')
    def _check_self_reference(self):
        for rec in self:
            if rec.id and rec.id in rec.doan_cu_ids.ids:
                raise ValidationError("Không được chọn chính bản thân làm đoạn cũ.")

    def action_open_wizard_tao_doan_moi(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tạo đoạn mới từ đoạn cũ',
            'res_model': 'wizard.tao.doan.moi',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doan_cu_ids': [self.id],
            }
        }

# Wizard tạo đoạn mới từ nhiều đoạn cũ
class TaoDoanMoiWizard(models.TransientModel):
    _name = 'wizard.tao.doan.moi'
    _description = 'Tạo đoạn mới từ đoạn cũ'

    doan_cu_ids = fields.Many2many('duong.giadat', string="Chọn đoạn cũ")
    name = fields.Char(string="Tên đoạn mới")
    duong_id = fields.Many2one('duong.giadat', string="Đường")
    diem_dau = fields.Char(string="Từ")
    diem_cuoi = fields.Char(string="Đến")
    ghi_chu_chinh_sua = fields.Text(string="Ghi chú")

    def tao_doan_moi(self):
        self.env['duong.giadat'].create({
            'name': self.name,
            'diem_dau': self.diem_dau,
            'diem_cuoi': self.diem_cuoi,
            'doan_cu_ids': [(6, 0, self.doan_cu_ids.ids)],
            'ghi_chu_chinh_sua': self.ghi_chu_chinh_sua
        })
        return {'type': 'ir.actions.act_window_close'}
