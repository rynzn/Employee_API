from odoo.addons.base_rest.controllers import main

class PublicRestController(main.RestController):
    _root_path = '/api/'
    _collection_name = "base.rest.public.services"
    _default_auth = "public"