from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
import json

class SalaryRuleCategoryService(Component):
    _inherit = 'base.rest.service'
    _name = 'salaryrulecategory.service'
    _usage = 'payroll'
    _collection = 'base.rest.public.services'
    
    #Get Salary Rule Category
    @restapi.method(
        [(["/rule_category/"], "GET")],
        auth="public",
    )
    def getAllRuleCategory(self):
        rule_category = self.env['hr.salary.rule.category'].search([])
        result = []
        for data in rule_category:
            result.append({
                "name" : data.name,
                "code": data.code,
            })
        return {
            "result" : result
        }
    
    #Create Salary Rule Category
    @restapi.method(
        [(["/rule_category/"], "POST")], 
        auth="public",
        input_param=restapi.CerberusValidator("_create_rulecategory_schema")
    )
    def createRuleCategory(self, **params):
        rule_category = self.env['hr.salary.rule.category'].sudo().create(params)
        return {
            "message" : "Success to Create Rule Category",
        }
    def _create_rulecategory_schema(self):
        return{
            "name" : {"type" : "string", "required":True},
            "code" : {"type" : "string", "required":True}
        }
    
    #Update Salary Rule Category
    @restapi.method(
        [(["/rule_category/<string:str>"], "PUT")],
        auth="public",
        input_param=restapi.CerberusValidator("_update_rulecategory_schema")
    )
    def updateRuleCategory(self, _str, **params):
        self.env['hr.salary.rule.category'].search([('code', 'ilike', _str)]).write(params)
        return {
            "message" : "Success to Update Rule Category"
        }
    def _update_rulecategory_schema(self):
        return{
            "name" : {"type" : "string", "required":False},
            "code" : {"type" : "string", "required":False}
        }
    
    #Delete Salary Rule Category
    @restapi.method(
        [(["/rule_category/<string:str>"], "DELETE")],
        auth="public",
    )
    def deleteRuleCategory(self, _str):
        self.env['hr.salary.rule.category'].search([('code', 'ilike', _str)]).unlink()
        return {
            "message" : "Success to Delete Rule Category"
        }
    

    #Get Salary Rule
    @restapi.method(
        [(["/salary_rule/"], "GET")],
        auth="public",
    )
    def getAllSalaryRule(self):
        salary_rule = self.env['hr.salary.rule'].search([])
        result = []
        for data in salary_rule:
            result.append({
                "name" : data.name,
                "code": data.code,
                # "category_id" : data.category_id,
                # "register_id" : data.register_id,
            })
        return {
            "result" : result
        }