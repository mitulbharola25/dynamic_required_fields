# -*- coding: utf-8 -*-
{
    "name": "Dynamic Required fields",
    "description": """Set required fields dynamically""",
    "summary": "Dynamically make fields required based on configuration.",
    "category": "Tools",
    "version": "16.0",
    "price": 5,
    "currency": "EUR",
    "author": "CodeCrafters",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/access_required_fields.xml",
    ],
    'images': [
        'static/description/banner.png',
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}
