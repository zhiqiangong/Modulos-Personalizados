{
    "name": "Web Eboss-Agencia",
    "summary": "Web Eboss-Agencia",
    "description": """
    """,
    "author": "Eco-clic",
    "version": "0.1",
    "depends": [
        "base",
        "website",
    ],
    "data": [
        "views/homepage.xml",
        "views/layout.xml",
        "views/alquileres.xml",       
        "views/contacto.xml",
        "views/faqs.xml",
        "views/nosotros.xml",
        "views/css_loader.xml",
  
    ],
    "assets": {
        'web.assets_frontend': [
            'eboss_agencia_web/static/src/css/estilos.css',
            'eboss_agencia_web/static/src/img/logo.png',
        ],
    },
    "installable": True,
    "application": False,
}
