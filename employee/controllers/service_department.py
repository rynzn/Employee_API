from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
import json

class DepartmentService(Component):
    _inherit = 'base.rest.service'
    _name = 'department.service'
    _usage = 'department'
    _collection = 'base.rest.public.services'

    #Get Department
    @restapi.method(
        [(["/"], "GET")],
        auth="public",
    )
    def getListDepartment(self):
        departments = self.env['hr.department'].search([])
        result = []
        for data in departments :
            result.append({
                "id" : data.id,
                "name" : data.name
            })
        return{
            "result" : result
        }
    
    @restapi.method(
        [(["/<int:id>"], "GET")],
        auth="public",
    )
    def getDepartmentById(self, _id):
        department = self.env['hr.department'].browse(_id)
        return {
            "result" :{
                "id" : department.id,
                "name" : department.name
            }
        }
    
    @restapi.method(
        [(["/employee/<int:id>"], "GET")],
        auth="public",
    )
    def getAllEmployeeFromDepartment(self, _id):
        department = self.env['hr.department'].browse(_id)
        employee = self.env['hr.employee'].search([('department_id', '=', department.id)])

        result = []
        for data in employee :
            result.append({
                "employee_id": data.id,
                "name" : data.name
            })
        return{
            "result" : {
                "id" : department.id,
                "name" : department.name,
                "employee" : result
            }
        }
    
    #Delete Department
    @restapi.method(
        [(["/<int:id>"], "DELETE")],
        auth="public",
    )
    def deleteDepartment(self, _id):
        department = self.env['hr.department'].browse(_id)
        employee = self.env['hr.employee'].search([('department_id.id', '=', department.id)]).unlink()
        self.env['hr.department'].browse(_id).unlink()
        
        return {
            "message": "Succes delete departement",
        }
    
    @restapi.method(
        [(["/employee/<int:id>"], "DELETE")],
        auth="public",
    )
    def deleteEmployeeInDepartment(self, _id):
        department = self.env['hr.department'].browse(_id)
        employee = self.env['hr.employee'].search([('department_id.id', '=', department.id)]).unlink()
        
        return {
            "message": "Succes delete employee in departement",
        }
    
    #Create Department
    @restapi.method(
        [(["/"], "POST")], 
        auth="public",
        input_param=restapi.CerberusValidator("_create_department_schema")
    )
    def createDepartment(self, **params):
        department = self.env['hr.department'].sudo().create(params)
        return {
            "message" : "Success to Create Department",
            "result" : {
                "id" : department.id,
                "name" : department.name
            }
        }
    def _create_department_schema(self):
        return{
            "name" : {"type" : "string", "required":True}
        }
    
    #Update Employee
    @restapi.method(
        [(["/<int:id>"], "PUT")], 
        auth="public",
        input_param=restapi.CerberusValidator("_update_department_schema")
    )
    def updateDepartment(self, _id, **params):
        self.env['hr.department'].browse(_id).write(params)
        return {
            "message" : "Success to Update Department"
        }
    def _update_department_schema(self):
        return{
            "name" : {"type" : "string", "required":False}
        }