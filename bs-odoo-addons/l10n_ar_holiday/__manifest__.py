# -*- coding: utf-8 -*-
{
    'name': 'Argentina Feriados en Calendario',
    'category': 'Human Resources',
    'version': '17.0.1.0.0',
    'summary': """Holidays automatically apply for all employees""",
    'description': """
    This module applies automatically a holiday for all employees in the company
    """,
    'author': 'Berisoft',
    'website': 'https://berisoft.com.ar',
    'depends': ['hr_holidays'],
    'data': [
        'views/calendar_event_views.xml',
    ],
    'license' : 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}