from odoo import api, fields, models
from datetime import datetime, date
from odoo import tools, _
from odoo import exceptions

class hr_employee(models.Model):
    _inherit = 'hr.employee'
    pensionno = fields.Char('Pension Number')
    bvn = fields.Integer('BVN', size=11)
    fileno = fields.Char('File Number')
    first_appointment_date = fields.Date('Date of First Appointment')
    present_appointment_date = fields.Date('Date of Present Appointment')
    appointment_terms = fields.Selection([
        ('permanent','Permanent'),
        ('contract','Contract'),
        ('secondment','Secondment'),
        ('internship','Internship')
        ],'Terms of Appointment')
    date_retirement = fields.Date('Date of Retirement', compute='_compute_date_of_retirement', store=True)
    nextofkin_ids = fields.One2many('employee.nextofkin','emp_nextofkin', String='Next of Kin')
    education_ids = fields.One2many('educational.history','emp_education', String='Educational History')
    salary_grade_level = fields.Selection([
        ('one','Grade Level 1'),
        ('two','Grade Level 2'),
        ('three','Grade Level 3'),
        ('four','Grade Level 4'),
        ('five','Grade Level 5'),
        ('six','Grade Level 6'),
        ('seven','Grade Level 7'),
        ('eight','Grade Level 8'),
        ('nine','Grade Level 9'),
        ('ten','Grade Level 10'),
        ('eleven','Grade Level 11'),
        ('twelve','Grade Level 12'),
        ('thirteen','Grade Level 13'),
        ('fourteen','Grade Level 14'),
        ('fifteen','Grade Level 15'),
        ('sixteen','Grade Level 16'),
        ('seventeen','Grade Level 17')
        ],'Salary Grade Level')

    def default_country(self):
        country_obj = self.env['res.country']
        def_country = country_obj.search([('name','like','Nigeria')]).id
        return def_country if def_country else False

    domicile = fields.Char('Registered Domicile')
    nationality = fields.Many2one('res.country', string='Nationality', default=default_country)
    stateoforigin = fields.Many2one('res.country.state','State Of Origin', domain="[('country_id', '=', nationality)]")
    languages_spoken = fields.Char('Languages Spoken')
    name_of_spouse = fields.Char('Name of Spouse')
    place_of_birth = fields.Char('Place of Birth')
    village = fields.Char('Town/Village')
    spouse_nationality = fields.Char('Nationality of Spouse')
    emp_referees_ids = fields.One2many('employee.referees','emp_referees',string='Referee')
    type_of_appointment = fields.Selection([
        ('contract','Contract'),
        ('secondment','Secondment'),
        ('transfer','Transfer'),
        ('fresh','Fresh')
        ],'Type of Appointment')
    full_resi_address = fields.Char('Full Residential Address')
    promotion_record_ids = fields.One2many('promotion.records','employee_id', string='Promotion/Transfer')
    medical_history_ids = fields.One2many('medical.history','employee_id', string="Medical History")
    commendation_ids = fields.One2many('employee.commendation','employee_id', string='Commendation')
    censure_ids = fields.One2many("employee.censure",'employee_id', string='Censure')
    remarks = fields.Text("Remarks")
    station = fields.Char('Station of Deployment')

    @api.one
    @api.depends('first_appointment_date', 'birthday')
    def _compute_date_of_retirement(self):

    	"""
        If only the birthday is supplied, calculate the date of retirement based on this field only
        """	
    	if self.birthday and not self.first_appointment_date:
    		birthday_date = fields.Date.from_string(self.birthday)
    		add_max_age = birthday_date.year + 60
    		date_retirement_string1 = birthday_date.replace(year=add_max_age)
    		self.date_retirement = fields.Date.to_string(date_retirement_string1) 

    	# Compute the date of retirement using only the date of first appointment
    	#else if 
    	if self.first_appointment_date and not self.birthday:
    		appointment_date = fields.Date.from_string(self.first_appointment_date)
    		add_year_of_service = appointment_date.year + 35
    		date_retirement_string2 = appointment_date.replace(year=add_year_of_service)
    		self.date_retirement = fields.Date.to_string(date_retirement_string2)

    	#else
        # If both the birthday and the date of first appointment are supplied, compute the date of retirement based on the two
    	if self.birthday and self.first_appointment_date:

            # By birth
            date_birth = fields.Date.from_string(self.birthday)
            length_by_age = date_birth.year + 60
            string_date_retirement_by_birth = date_birth.replace(year=length_by_age)
            date_retirement_by_birth = fields.Date.to_string(string_date_retirement_by_birth)

            # By years of service
            date_first_appoint = fields.Date.from_string(self.first_appointment_date)
            length_by_service = date_first_appoint.year + 35
            string_date_retirement_by_appoint = date_first_appoint.replace(year=length_by_service)
            date_retirement_by_appoint = fields.Date.to_string(string_date_retirement_by_appoint)

            #Compare the smaller of the dates and use as the retirement date
            self.date_retirement = date_retirement_by_birth if date_retirement_by_birth < date_retirement_by_appoint \
            else date_retirement_by_appoint

    	
class employee_nextofkin(models.Model):
    _name = "employee.nextofkin"
    image = fields.Binary('Passport')
    name = fields.Char('Name')
    rel_staff = fields.Many2one(comodel_name="relationship.employee", string="Relationship of Next of Kin")
    mobile_phone = fields.Char('GSM No.', readonly=False)   
    address = fields.Char('Street Name/Address')
    emp_nextofkin = fields.Many2one('hr.employee','Employee')

class relationship_employee(models.Model):
    """Defines relationship shared with next of kins etc"""
    _name = 'relationship.employee'
    _description = 'Employee\'s Relationships'

    name = fields.Char("Name")

class educational_history(models.Model):
    _name = "educational.history"
    school_name = fields.Char('Name of Institution')
    date_from = fields.Date('From')
    date_to = fields.Date('To')
    cert_date = fields.Date('Qualifications Date')
    quali = fields.Char('Qualifications')
    course_studied = fields.Char('Course')
    emp_education = fields.Many2one('hr.employee','Employees Educational History')

class employee_referees(models.Model):
    _name = "employee.referees"
    image = fields.Binary('Photo', widget='binary')
    name = fields.Char('Name')
    sex = fields.Selection([('male','Male'),('female','Female')], 'Sex')
    address = fields.Char('Address')
    emp_referees = fields.Many2one('hr.employee','Employee')

class promotion_records(models.Model):
    _name = 'promotion.records'         
    type= fields.Selection([
        ('promotion','Promotion'),
        ('transfer','Transfer')
        ],'Type')
    designation_from = fields.Many2one(comodel_name="hr.job", string='From')
    designation_to = fields.Many2one(comodel_name="hr.job", string='To')
    date_promotion = fields.Date('Date')
    employee_id = fields.Many2one('hr.employee','Employee')

class employment_medical_history(models.Model):
    _name="medical.history"
    nature = fields.Char('Medical Condition')
    date_from = fields.Date('From')
    date_to = fields.Date('To')
    employee_id = fields.Many2one('hr.employee', 'Employee')

class commendation(models.Model):
    _name = "employee.commendation"

    def domain(self):
        """Return the domain for this record"""
        current_employee = self.env.get('hr.employee').browse(self._context.get('default_employee_id'))
        all_employees = self.env.get('hr.employee').search([])
        diff = all_employees - current_employee
        return [('id','in', diff.ids)]

    description = fields.Char('Descritption')
    by_whom = fields.Many2one('hr.employee','By whom', domain=domain)
    date_commendation = fields.Date('Date', widget='date')
    result = fields.Selection([
        ('Promotion','Promotion'),
        ('Transfer','Transfer')
        ],"Outcome")
    employee_id = fields.Many2one('hr.employee',"Employee")

class censure(models.Model):
    _name = "employee.censure"

    employee_id = fields.Many2one('hr.employee',"Employee")

    def domain(self):
        """Return the domain for this record"""
        current_employee = self.env.get('hr.employee').browse(self._context.get('default_employee_id'))
        all_employees = self.env.get('hr.employee').search([])
        diff = all_employees - current_employee
        return [('id','in', diff.ids)]

    description = fields.Char('Description')
    by_whom = fields.Many2one('hr.employee','By whom', domain=domain)
    date_censure = fields.Date('Date', widget='date')
    result = fields.Selection([
        ('Promotion','Promotion'),
        ('Demotion','Demotion'),
        ('Suspension','Suspension')
        ], 'Outcome')
