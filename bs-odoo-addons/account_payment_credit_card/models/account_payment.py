# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_credit_card = fields.Boolean('Es tarjeta de credito',related='journal_id.is_credit_card')
    plan_tarjeta_id = fields.Many2one('account.payment.plan.tarjeta',string='Plan Tarjeta', ondelete='Restrict')
    nro_lote = fields.Char('N° Lote')
    nro_cupon = fields.Char('N° Cupon')

    @api.constrains('nro_cupon','nro_lote')
    def _check_pago_tarjeta(self):
        for rec in self:
            if rec.is_credit_card:
                if (not rec.nro_cupon) or (not rec.nro_lote) or (not rec.plan_tarjeta_id):
                    raise ValidationError("Debe ingresar los datos de pago de tarjeta")

    @api.onchange('journal_id')
    def _journal_id_onchange(self):
        res = {}
        res['domain']={'plan_tarjeta_id':[('journal_id', '=', self.journal_id.id)]}
        return res

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_ids = fields.One2many('account.payment', 'move_id')

    @api.depends('payment_ids.journal_id', 'payment_ids.plan_tarjeta_id', 'payment_ids.nro_lote')
    def _compute_ref(self):
        for record in self:
            refs = []
            for payment in record.payment_ids:
                ref_parts = [str(payment.journal_id.name or '')]
                if payment.plan_tarjeta_id.name:
                    ref_parts.append(str(payment.plan_tarjeta_id.name))
                if payment.nro_lote:
                    ref_parts.append(f"Lote {payment.nro_lote}")
                refs.append(", ".join(ref_parts))
            record.ref = ", ".join(refs)

    #Agrego moneda
    @api.depends('payment_ids.amount', 'payment_ids.currency_id')
    def _compute_amount_signed(self):
        for record in self:
            if record.payment_ids:
                # Calcula el monto total de los pagos
                total_amount = sum(payment.amount for payment in record.payment_ids)
                record.amount_signed = total_amount
                # Asigna la moneda del primer pago, si existe
                record.currency_id = record.payment_ids[0].currency_id
            else:
                # Asegúrate de que currency_id nunca esté vacío
                record.currency_id = self.env.company.currency_id


    ref = fields.Char(compute='_compute_ref', store=True, readonly=False, force_save=True)
    #Agrego Moneda
    amount_signed = fields.Float(compute='_compute_amount_signed', store=True, readonly=False, force_save=True)
    currency_id = fields.Many2one('res.currency', compute='_compute_amount_signed', store=True, readonly=False, force_save=True)






