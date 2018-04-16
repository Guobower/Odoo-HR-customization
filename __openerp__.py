{
    "name" : "Additional Human Resources Fields",
    "version" : "1.0",
    "author" : "MgB Computers",
    "website" : "http://www.mgbcomputers.com",
    "category": "Others",
    "complexity": "easy",
    "description": """Additional Human Resources Fields.
        -salary grade levels
        -promotion management
        -retirement management
        - pension management 
    """,
    "depends": ["base","hr","hr_payroll"],
    "data": [
        "security/ir.model.access.csv",
        "views/additional_fields_view.xml",
        "views/designation_view.xml",
        "views/constituency_view.xml",
        "views/res_state_lga_view.xml",
        "data/menus.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: