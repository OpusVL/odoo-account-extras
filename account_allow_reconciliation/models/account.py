# -*- coding = utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.multi
    def write(self, vals):
        # Dont allow changing the company_id when account_move_line already exist
        if vals.get('company_id', False):
            move_lines = self.env['account.move.line'].search([('account_id', 'in', self.ids)], limit=1)
            for account in self:
                if (account.company_id.id != vals['company_id']) and move_lines:
                    raise UserError(
                        _('You cannot change the owner company of an account that already contains journal items.'))

        # If we already have account move lines with the account we want to be able to select reconcile therefore we
        # have to remove the existing constraint on account.py

        '''Warning If you try to inherit AccountAccount.write in anywhere else it will be ignored.'''
        return super(models.Model, self).write(vals)
