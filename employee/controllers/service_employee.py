from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi
import json

class EmployeeService(Component):
    _inherit = 'base.rest.service'
    _name = 'employee.service'
    _usage = 'employee'
    _collection = 'base.rest.public.services'

    #Get Employee
    @restapi.method(
        [(["/"], "GET")],
        auth="public",
    )
    def getAllEmployee(self):
        employees = self.env['hr.employee'].search([])
        result = []
        for data in employees:
            result.append({
                "employee_id": data.id,
                "name" : data.name,
                "department" : {
                    "id": data.department_id.id,
                    "name": data.department_id.name}
            })
        return {
            "result" : result
        }
    
    @restapi.method(
        [(["/<int:id>"], "GET")],
        auth="public",
    )
    def getEmployeeById(self, _id):
        employee = self.env['hr.employee'].browse(_id)
        return {
            "result" : {
                "employee_id": employee.id,
                "name" : employee.name,
                "department" : {
                    "id": employee.department_id.id,
                    "name": employee.department_id.name}
                }
            }

    @restapi.method(
        [(["/attachment/<int:id>"], "GET")],
        auth="public",
    )
    def getAttachmentEmployee(self, _id):
        attachment = self.env['ir.attachment'].search([('res_model', '=', 'hr.employee'),('res_id', '=', _id)])

        result = []
        for data in attachment:
            result.append({
                "name" : data.name
            })
        return {
            "result" : result
        }
    
    #Delete Employee
    @restapi.method(
        [(["/<int:id>"], "DELETE")],
        auth="public",
    )
    def deleteEmployeeById(self, _id):
        self.env['hr.employee'].browse(_id).unlink()
        return {
            "message": "Succes delete employee"
        }

    #Create Employee
    @restapi.method(
        [(["/"], "POST")], 
        auth="public",
        input_param=restapi.CerberusValidator("_create_employee_schema")
    )
    def createEmployee(self, **params):
        employee = self.env['hr.employee'].sudo().create(params)
        return {
            "message" : "Success to Create Employee",
            "result" : {
                "id" : employee.id,
                "name" : employee.name
            }
        }
    def _create_employee_schema(self):
        return{
            "name" : {"type" : "string", "required":True}
        }
    
    @restapi.method(
        [(["/attachment/<int:id>"], "POST")], 
        auth="public",
        input_param=restapi.CerberusValidator("_create_attachment_schema")
    )
    def createAttachment(self, _id, **params):
        employee = self.env['hr.employee'].browse(_id)
        self.env['ir.attachment'].sudo().create({
            "name" : params["name"],
            "res_model" : "hr.employee",
            "res_id" : employee.id,
            "datas" : params["datas"],
        })
        return {
            "message" : "Success to Create Attachment",
            "name" : params["name"],
        }
    def _create_attachment_schema(self):
        return{
            "name" : {"type" : "string", "required":True},
            "datas" : {"type" : "string", "required":True}
        }    

    #Update Employee
    @restapi.method([(["/<int:id>"], "PUT")], 
        auth="public",
        input_param=restapi.CerberusValidator("_update_employee_schema")
    )
    def updateEmployee(self, _id, **params):
        self.env['hr.employee'].browse(_id).write(params)
        return {
            "message" : "Success to Update Employee"
        }
    def _update_employee_schema(self):
        return{
            "name" : {"type" : "string", "required":False}
        }