from odoo import models

class PurchaseOrderXlsx(models.AbstractModel):
    _name = "report.purchase_order_xlsx"
    _description = "Export Purchase Orders to XLSX"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, purchase_orders):
        # Nombre de la hoja de trabajo
        sheet = workbook.add_worksheet("Productos")
        
        # Formatos para la hoja
        bold = workbook.add_format({"bold": True})
        
        # Escribir el encabezado
        sheet.write(0, 0, "Producto", bold)
        sheet.write(0, 1, "Cantidad", bold)
        
        # Escribir los datos
        row = 1
        for order in purchase_orders:
            for line in order.order_line:
                # Columna 0: Producto (referencia)
                sheet.write(row, 0, line.product_id.default_code or '')
                # Columna 1: Cantidad pedida
                sheet.write(row, 1, line.product_qty)
                row += 1
