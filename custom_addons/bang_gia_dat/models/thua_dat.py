from odoo import models, fields, api
from odoo.tools.populate import compute


class ThuaDat(models.Model):
    _name = 'thua.dat'
    _description = 'Thông tin thửa đất'

    active = fields.Boolean('Active', default=True)
    code = fields.Char(string="Số hồ sơ")
    note = fields.Char(string="Ghi chú")

    so_thua = fields.Char(string="Thửa")
    so_to = fields.Char(string="Tờ")
    diachi_thuadat = fields.Char(string="Địa chỉ thửa")

    nguoi_su_dung_dat = fields.Char(string="Người SDĐ")
    diachi_nguoi_sdd = fields.Char(string="Địa chỉ người SDĐ")
    mst_canhan = fields.Char(string="MST")
    thoi_diem = fields.Date(string="Ngày PC")

    # Xã phường cũ
    xa_phuong = fields.Char(string="Xã cũ")
    quan_huyen = fields.Many2one('dm.quanhuyen', string="Huyện cũ", compute="_compute_quan_huyen_cu", store=True)


    @api.depends('xa_phuong', 'duong_id')
    def _compute_quan_huyen_cu(self):
        QuanHuyen = self.env['dm.quanhuyen']
        for rec in self:
            rec.quan_huyen = False
            if not rec.xa_phuong:
                continue

            xa_clean = rec.xa_phuong.lower().strip()
            xa_clean = xa_clean.replace('xã ', '').replace('phường ', '').replace('thị trấn ', '').replace('TT. ', '').strip()

            # Tìm tất cả xã mới có merged_from
            all_xa = self.env['dm.xaphuong'].search([('merged_from', '!=', False)])

            found = False
            for xa in all_xa:
                for item in xa.merged_from.split(','):
                    item = item.strip().lower()
                    if '-' in item:
                        parts = item.split('-')
                        ten_cu = parts[0].strip()
                        huyen_cu = parts[1].strip()
                        if ten_cu == xa_clean:
                            huyen_obj = QuanHuyen.search([('name', 'ilike', huyen_cu)], limit=1)
                            if huyen_obj:
                                rec.quan_huyen = huyen_obj.id
                                found = True
                                break
                    else:
                        # Fallback: trường hợp không có hậu tố
                        if item.strip() == xa_clean:
                            rec.quan_huyen = xa.quan_huyen_id.id if xa.quan_huyen_id else False
                            found = True
                            break
                if found:
                    break

    # Trường xã/phường mới
    xa_phuong_moi_id = fields.Many2one('dm.xaphuong', string="Xã/Phường (mới)", compute="_compute_xa_moi", store=True)
    tinh_thanh_moi_id = fields.Many2one('dm.tinhthanh', string="Tỉnh/Thành (mới)", compute="_compute_xa_moi",
                                        store=True)

    loai_dat = fields.Char(string="Loại đất")
    dien_tich_dat = fields.Float(string="Diện tích đất", compute='_compute_dien_tich', store=True)
    gia_nnt_khai_tong = fields.Float(string="Giá NNT (Tổng)", digits=(16, 0))
    gia_nnt_khai_nha = fields.Float(string="Giá NNT (Nhà)", digits=(16, 0))
    gia_nnt_khai_dat = fields.Float(string="Giá NNT (Đất)", digits=(16, 0))
    gia_nn_tong = fields.Float(string="Giá NN (Tổng)", digits=(16, 0))
    gia_nn_nha = fields.Float(string="Giá NN (Nhà)", digits=(16, 0))
    gia_nn_dat = fields.Float(string="Giá NN (Đất)", digits=(16, 0))
    gia_nn = fields.Float(string="Giá nhà nước", digits=(16, 0))


    duong_id = fields.Many2one('duong.giadat', string="Tên đường", tracking=True)
    diem_dau = fields.Char(string="Từ", tracking=True)
    diem_cuoi = fields.Char(string="Đến", tracking=True)
    doan_duong = fields.Char(
        string="Đoạn đường",
        compute="_compute_doan_duong",
        store=True
    )

    @api.onchange('duong_id')
    def _compute_diem(self):
        for rec in self:
            rec.diem_dau = rec.duong_id.diem_dau
            rec.diem_cuoi = rec.duong_id.diem_cuoi

    # Thêm các trường trong danh sách nộp thuế
    so_phieu_chuyen = fields.Char(string="Số phiếu chuyển")
    dien_tich_nha = fields.Float(string="Diện tích nhà")
    dien_tich_odt = fields.Float(string="Đất ở đô thị")
    dien_tich_ont = fields.Float(string="Đất ở nông thôn")
    dien_tich_cln = fields.Float(string="Đất trồng cây lâu năm")
    dien_tich_chn = fields.Float(string="Đất trồng cây hàng năm")
    dien_tich_nts = fields.Float(string="Đất nuôi trồng thủy sản")

    @api.depends('dien_tich_odt', 'dien_tich_ont', 'dien_tich_cln', 'dien_tich_chn', 'dien_tich_nts')
    def _compute_dien_tich(self):
        for rec in self:
            rec.dien_tich_dat = rec.dien_tich_odt + rec.dien_tich_ont + rec.dien_tich_cln + rec.dien_tich_chn + rec.dien_tich_nts

    @api.depends('diem_dau', 'diem_cuoi')
    def _compute_doan_duong(self):
        for rec in self:
            if rec.diem_dau and rec.diem_cuoi:
                rec.doan_duong = f"{rec.diem_dau} - {rec.diem_cuoi}"
            else:
                rec.doan_duong = f"{rec.diem_dau}"

    # Đặc điểm tài sản
    mat_tien_hem_id = fields.Many2one('dm.mattienhem', string="Mặt tiền/hẻm", tracking=True)
    do_rong_hem_id = fields.Many2one('dm.doronghem', string="Độ rộng hẻm", tracking=True)
    chieu_sau_id = fields.Many2one('dm.chieusau', string="Chiều sâu lô đất", tracking=True)
    ket_cau_duong_id = fields.Many2one('dm.ketcauduong', string="Kết cấu đường", tracking=True)
    khu_vuc_id = fields.Many2one('dm.khuvuc', string="Khu vực", tracking=True)
    vi_tri_id = fields.Many2one('dm.vitri', string="Vị trí", tracking=True)

    nguoi_nhap_lieu = fields.Many2one(
        'res.users', string='Người nhập liệu'
    )

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    # Trường mới để đánh dấu đã xác nhận
    da_xac_nhan = fields.Boolean(string="Đã xác nhận", default=False)

    # Nút hành động xác nhận
    def action_xac_nhan(self):
        for record in self:
            record.da_xac_nhan = True

    @api.depends('xa_phuong')
    def _compute_xa_moi(self):
        for rec in self:
            if rec.xa_phuong:
                # ➤ Chuẩn hóa: bỏ tiền tố "xã", "phường", "thị trấn" và khoảng trắng
                xa_clean = rec.xa_phuong.lower().strip()
                xa_clean = xa_clean.replace('xã ', '').replace('thị trấn ', '').replace('phường ', '').strip()

                # Tìm xã/phường mới có chứa tên chuẩn hóa trong merged_from
                xa_moi = self.env['dm.xaphuong'].search([
                    ('merged_from', 'ilike', xa_clean)
                ], limit=1)

                rec.xa_phuong_moi_id = xa_moi.id if xa_moi else False
                rec.tinh_thanh_moi_id = xa_moi.tinh_thanh_id.id if xa_moi else False
            else:
                rec.xa_phuong_moi_id = False
                rec.tinh_thanh_moi_id = False



    @api.model
    def action_tinh_lai_toan_bo_quan_huyen(self):
        records = self.search([])
        for rec in records:
            rec._compute_quan_huyen_cu()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    he_so_so_sanh = fields.Float(string="Hệ số", compute='_he_so_so_sanh', store=True, group_operator='avg')

    @api.depends('gia_nnt_khai_tong', 'gia_nn_tong')
    def _he_so_so_sanh(self):
        for rec in self:
            if rec.gia_nn_tong != 0:
                rec.he_so_so_sanh = rec.gia_nnt_khai_tong / rec.gia_nn_tong
            else:
                rec.he_so_so_sanh = 0


    # Tính giá
    don_gia = fields.Float(string="Giá đất")
    max_don_gia = fields.Float(string="Giá cao nhất")
    min_don_gia = fields.Float(string="Giá thấp nhất")
    avg_don_gia = fields.Float(string="Giá trung bình")