from odoo import fields, models, api
from datetime import date

class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    # Campo calculado para almacenar el costo del componente basado en el precio del proveedor
    cost = fields.Float(string="Cost (Supplier Price)", store=True)

    def manual_compute_bom_cost(self):
        """
        Método manual para calcular el costo de los componentes en la BoM usando el valor del campo product_cost
        del proveedor. Aplica la conversión si la Unidad de Medida es "ml", dividiendo el costo por 946.
        """
        for line in self:
            product = line.product_id
            if product:
                # Obtener la línea de proveedor vigente en función de las fechas
                supplierinfo = product.seller_ids.filtered(lambda s: (not s.date_start or s.date_start <= date.today()) and
                                                           (not s.date_end or s.date_end >= date.today()))[:1]

                if supplierinfo:
                    # Obtener el valor del campo product_cost del proveedor
                    product_cost = supplierinfo.product_cost

                    # Obtener la unidad de medida "ml" creada por el usuario, usando el id de category_id
                    ml_uom = self.env['uom.uom'].search([('name', '=', 'ml'), ('category_id', '=', product.uom_id.category_id.id)], limit=1)

                    # Aplicar la conversión si la unidad de medida es "ml"
                    if product.uom_id == ml_uom:
                        product_cost = product_cost / 946

                    # Asignar el costo sin realizar conversiones adicionales
                    line.cost = product_cost * line.product_qty
                else:
                    # Usar el costo estándar del producto si no hay proveedor vigente
                    line.cost = product.standard_price * line.product_qty
            else:
                line.cost = 0.0


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # Campo para almacenar el costo total de la BoM
    total_cost = fields.Float(string="Total Cost", store=True)

    def manual_compute_total_bom_cost(self):
        """
        Método manual para calcular el costo total de la BoM sumando los costos de cada componente.
        Luego actualiza el `standard_price` del producto con este costo total.
        """
        for bom in self:
            # Asegurar que todas las líneas de la BoM tienen el costo calculado
            for line in bom.bom_line_ids:
                line.manual_compute_bom_cost()

            # Calcular el costo total de la BoM
            total_cost = sum(line.cost for line in bom.bom_line_ids)
            bom.total_cost = total_cost

            # Si la BoM tiene un producto asociado, actualizamos el standard_price
            if bom.product_tmpl_id:
                bom.product_tmpl_id.standard_price = total_cost


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def button_bom_cost(self):
        """
        Método manual para calcular el costo de la Lista de Materiales (BoM)
        basado en el campo product_cost del proveedor y la unidad de medida.
        """
        for product in self:
            if product.bom_count > 0:
                # Obtener las BoMs asociadas con el producto
                boms = self.env['mrp.bom'].search([('product_tmpl_id', '=', product.id)])
                for bom in boms:
                    # Calcular manualmente el costo de cada línea de la BoM
                    for line in bom.bom_line_ids:
                        line.manual_compute_bom_cost()

                    # Calcular el costo total de la BoM
                    bom.manual_compute_total_bom_cost()
