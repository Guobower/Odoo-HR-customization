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

    	# If both the birtday and the date of first appointment are supplied, compute the date of retirement based on the two

    	#else
    	if self.birthday and self.first_appointment_date:
    		if date_retirement_string1 < date_retirement_string2:
    			self.date_retirement = fields.Date.to_string(date_retirement_string1)
    		else:
    			self.date_retirement = fields.Date.to_string(date_retirement_string2)
        
    	
class employee_nextofkin(models.Model):
    _name = "employee.nextofkin"
    image = fields.Binary('Passport')
    name = fields.Char('Name')
    rel_staff = fields.Char("Relationship of Next of Kin")
    mobile_phone = fields.Char('GSM No.', readonly=False)   
    address = fields.Char('Street Name/Address')
    emp_nextofkin = fields.Many2one('hr.employee','Employee')

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
    designation_from = fields.Selection([
        ('chief_adm_officer','Chief Admin Officer'),
        ('assit_chief_adm_officer','Assistant Chief Admin Officer'),
        ('principal','Principal'),
        ('senior','Senior'),
        ('officer_i','Officer I'),
        ('officer_ii','Officer II')
        ],'Designation(From)')
    designation_from_date = fields.Date('Date')
    designation_to = fields.Selection([
        ('chief_adm_officer','Chief Admin Officer'),
        ('assit_chief_adm_officer','Assistant Chief Admin Officer'),
        ('principal','Principal'),
        ('senior','Senior'),
        ('officer_i','Officer I'),
        ('officer_ii','Officer II')
        ],'Designation To')
    designation_to_date = fields.Date('Date')
    employee_id = fields.Many2one('hr.employee','Employee')

class employment_medical_history(models.Model):
    _name="medical.history"
    nature = fields.Char('Medical Condition')
    date_from = fields.Date('From')
    date_to = fields.Date('To')
    employee_id = fields.Many2one('hr.employee', 'Employee')

class commendation(models.Model):
    _name = "employee.commendation"
    description = fields.Char('Descritption')
    by_whom = fields.Char('By whom')
    date_commendation = fields.Date('Date', widget='date')
    result = fields.Selection([
        ('Promotion','Promotion'),
        ('Transfer','Transfer')
        ],"Outcome")
    employee_id = fields.Many2one('hr.employee',"Employee")

class censure(models.Model):
    _name = "employee.censure"
    description = fields.Char('Descritption')
    by_whom = fields.Char('By whom')
    date_censure = fields.Date('Date', widget='date')
    result = fields.Selection([
        ('Promotion','Promotion'),
        ('Demotion','Demotion'),
        ('Suspension','Suspension')
        ], 'Outcome')
    employee_id = fields.Many2one('hr.employee',"Employee")
