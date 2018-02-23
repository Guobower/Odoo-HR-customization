from odoo import api, fields, models

@api.model
def location_name_search(self, name='', args=None, operator='ilike', limit=100):
    if args is None:
        args = []

    records = self.browse()
    if len(name) == 2:
        records = self.search([('code', 'ilike', name)] + args, limit=limit)

    search_domain = [('name', operator, name)]
    if records:
        search_domain.append(('id', 'not in', records.ids))
    records += self.search(search_domain + args, limit=limit)

    # the field 'display_name' calls name_get() to get its value
    return [(record.id, record.display_name) for record in records]

class Constituency(models.Model):
    _name = 'res.country.constituency'
    _description = "Country constituency"
    _order = 'code'    
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    name = fields.Char(string='Constituency', required=True,
               help='Federal Constituencies in the Country. E.g. Ado-Odo/Ota, Boluwaduro/Ifedayo/Ila')
    code = fields.Char(string='Constituency Code', help='The state code.', required=True)

    name_search = location_name_search

    _sql_constraints = [
        ('name_code_uniq', 'unique(country_id, code)', 'The code of the constituency must be unique per country!')
    ]

class Employee(models.Model):
    """This body of code add the constituency field to the hr.employee model"""
    _inherit = 'hr.employee'
    constituency_id = fields.Many2one('res.country.constituency', string='Constituency', domain="[('state_id', '=', stateoforigin)]")