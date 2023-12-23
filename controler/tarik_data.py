from odoo import http
from odoo.http import request

class KanbanClickController(http.Controller):

    @http.route('/kanban_click/<model("data.mesin.urw"):machine>', type='http', auth="public", website=True)
    def kanban_click(self, machine, **kwargs):
        snap_qc_line_form = request.env['ir.ui.view'].search([('model', '=', 'data.snap.qc.line'), ('type', '=', 'form')])
        vals = {
            'no_mesin': machine.no_mesin,
        }
        action = {
            'name': 'Kanban Click',
            'type': 'ir.actions.act_window',
            'res_model': 'data.snap.qc.line',
            'view_mode': 'form',
            'view_id': snap_qc_line_form.id,
            'target': 'main',
            'context': vals,
        }
        return action
