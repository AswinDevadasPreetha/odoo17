from odoo import models, fields,_
from odoo.exceptions import ValidationError



class MrpProduction(models.Model):
    _inherit='mrp.production'
    
    
    def action_confirm(self):
        res = super(MrpProduction,self).action_confirm()
        available_stocks = []
        for rec in self.move_raw_ids:
            stocks = self.env['stock.quant'].search([('product_id','=',rec.product_id.id),('inventory_quantity_auto_apply','>',0)])
            if stocks:
                for stk in stocks:
                    # if stk.reserved_quantity <= stk.inventory_quantity_auto_apply :
                    available_stocks.append(stk)  
            else:
                available_stocks.append(rec)   
        # self.move_raw_ids = (5,0,0)
        new_moverows_ids = []
        for line in available_stocks:
           
            lines = {'product_id':line.product_id.id,
                    'product_uom_qty':self.product_qty * sum(self.bom_id.bom_line_ids.filtered(lambda x:x.product_id.id == line.product_id.id).mapped('product_qty')),
                    'lot_ids':[(4, line.lot_id.id, 0)] if line._name == 'stock.quant' else False,
                    'stock_location_c':line.location_id.id if line._name == 'stock.quant' else False,
                    'raw_material_production_id':self.id}
            
            new_moverows_ids.append(lines)
            if line._name == 'stock.quant':
                # print(line._name,"STTTTTTTTTTTOOOOOOOOOOOOOO",lines,"OOOOOOCCCCCCCCCCCCCKKKKKKKKKKKKKKSSSSSSSSSSSS",available_stocks)
        self.move_raw_ids = False
        # self.move_raw_ids = new_moverows_ids
        self.env['stock.move'].create(new_moverows_ids)
            
        return res



class StockM(models.Model):
    _inherit='stock.move'
    
    stock_location_c = fields.Many2one('stock.quant',string="Locations")

    


















