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

class Lga(models.Model):
    _name = 'res.state.lga'
    _description = "Local Government Area"

    def _get_default_country(self):
        return self.env.user.company_id.country_id.id

    country_id = fields.Many2one("res.country", "Country", default=_get_default_country)
    state_id = fields.Many2one('res.country.state', string='State', required=True, domain="[('country_id','=',country_id)]")
    # constituency_id = fields.Many2one('res.country.constituency', string='Fed. constituency', domain="[('state_id','=',state_id)]")
    name = fields.Char(string='LGA', required=True,
               help='Local Governments e.g. Odo-Otin, Boluwaduro')
    name_search = location_name_search
    _sql_constraints = [
        ('name_uniq', 'unique(name, state_id)', 'The local government name must be unique per state!')
    ]

class Employee(models.Model):
    """This body of code add the constituency field to the hr.employee model"""
    _inherit = 'hr.employee'
    lga_id = fields.Many2one('res.state.lga', string='LGA', domain="[('state_id','=', stateoforigin)]")

class State(models.Model):
    """Return a default country for the country_id"""
    _inherit = 'res.country.state'

    def _return_default_country(self):
        return self.env.user.company_id.country_id.id

    country_id = fields.Many2one(default=_return_default_country)