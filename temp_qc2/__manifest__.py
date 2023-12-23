{
    'name': 'Snap Qc',
    'version': '1.0',
    'website': "https://urwastex.blogspot.com/2018/03/profile-company.html",
    'company': 'PT. Unggulrejo Wasiono',
    'summary': 'Snap Quality Control',
    'description': """
        This module allows you to Snap and Manage Machines within your organization.
    """,
    'author': 'Dermawan Laoli - Magang UKRIM Yogyakarta',
    'category': 'Industry',
    'depends': ['base', 'web'],
    'data': [
        'views/data_mesin.xml',
        'views/dashboard_inspector.xml',
        'views/view_block.xml',
        'views/view_inspector.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/report_menu.xml',
        # 'report/report_mesin_produksi.xml',
        'report/report_inspector.xml'
        
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
