from odoo import fields, models, api

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    quotation_date = fields.Date(string='Ngày báo giá', tracking=True)
    quotation_assets = fields.Text(string='Tài sản thẩm định giá', tracking=True)
    time_of_valuation = fields.Text(string='Thời điểm thẩm định giá', tracking=True)
    area_of_valuation = fields.Text(string='Địa điểm thẩm định giá', tracking=True)
    quotation_purpose = fields.Text(string='Mục đích thẩm định giá', tracking=True)
    valuation_fee_number = fields.Float(string='Phí dịch vụ thẩm định giá', digits=(15, 0), tracking=True)
    valuation_fee_text = fields.Text(string='Bằng chữ', tracking=True)
    valuation_fee_vat = fields.Text(string='Ghi chú VAT', default='Mức phí trên đã bao gồm VAT', tracking=True)
    pay = fields.Html('Thanh toán', default='<p>- <b>Lần 1:</b> 50% giá trị hợp đồng, tương ứng với số tiền ... đồng, ngay sau khi ký Hợp đồng</p><p>- <b>Lần 2:</b> Phần còn lại của giá trị hợp đồng sau khi MHD bàn giao kết quả thẩm định giá</p>')
    execution_time = fields.Text(string='Thời gian thực hiện', tracking=True)
    signer = fields.Text(string='Người ký báo giá', default='TRẦN KHÁNH DU', tracking=True)
    signer_position = fields.Text(string='Chức vụ người ký', default='Giám đốc', tracking=True)
    list_assets = fields.Html('Danh sách tài sản', tracking=True)
    hide_list_assets = fields.Boolean(string='Ẩn danh mục tài sản', default=True, help='Bỏ chọn nếu muốn hiện danh mục tài sản')
    person_support = fields.Text(string='Người hỗ trợ', default='Liên hệ 0909.630.504 để được tư vấn, hỗ trợ')
    # Tách ngày tháng năm báo giá
    quotation_day = fields.Text(string='Ngày', compute='_compute_date_parts')
    quotation_month = fields.Text(string='Tháng', compute='_compute_date_parts')
    quotation_year = fields.Text(string='Năm', compute='_compute_date_parts')
    hide_quotation_date = fields.Boolean(string='Ẩn ngày báo giá', default=False, help='Bấm chọn nếu muốn ẩn')

    @api.depends('quotation_date')
    def _compute_date_parts(self):
        for record in self:
            if record.quotation_date:
                record.quotation_day = record.quotation_date.day
                record.quotation_month = record.quotation_date.month
                record.quotation_year = record.quotation_date.strftime('%Y')
