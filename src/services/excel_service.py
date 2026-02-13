import os
from datetime import datetime
from typing import Dict, Any
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet


class ExcelService:
    """Servicio para generación de archivos Excel de cotizaciones"""
    
    def __init__(self, output_dir='exports/excel'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generar_cotizacion(self, cotizacion_data: Dict[str, Any], empresa_data: Dict[str, Any]) -> str:
        """
        Genera un archivo Excel de cotización profesional
        
        Args:
            cotizacion_data: dict con datos de cotización
            empresa_data: dict con datos de empresa
        
        Returns:
            str: ruta del archivo generado
        """
        # Nombre del archivo
        filename = f"{cotizacion_data['numero_cotizacion'].replace('/', '-')}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear libro
        wb = Workbook()
        ws: Worksheet = wb.active  # type: ignore
        ws.title = "Cotización"
        
        # Estilos
        font_title = Font(name='Arial', size=18, bold=True, color='2C3E50')
        font_subtitle = Font(name='Arial', size=10, color='7F8C8D')
        font_heading = Font(name='Arial', size=12, bold=True, color='2C3E50')
        font_bold = Font(name='Arial', size=10, bold=True)
        font_normal = Font(name='Arial', size=10)
        
        fill_header = PatternFill(start_color='3498DB', end_color='3498DB', fill_type='solid')
        fill_light = PatternFill(start_color='ECF0F1', end_color='ECF0F1', fill_type='solid')
        
        border_thin = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        align_center = Alignment(horizontal='center', vertical='center')
        align_left = Alignment(horizontal='left', vertical='center')
        align_right = Alignment(horizontal='right', vertical='center')
        
        # Configurar ancho de columnas
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 15
        
        row = 1
        
        # === ENCABEZADO EMPRESA ===
        ws.merge_cells(f'A{row}:D{row}')
        cell = ws[f'A{row}']
        cell.value = empresa_data.get('nombre', 'EMPRESA')
        cell.font = font_title
        cell.alignment = align_center
        row += 1
        
        # Info empresa
        info_empresa = []
        if empresa_data.get('direccion'):
            info_empresa.append(empresa_data['direccion'])
        if empresa_data.get('telefono'):
            info_empresa.append(f"Tel: {empresa_data['telefono']}")
        if empresa_data.get('email'):
            info_empresa.append(f"Email: {empresa_data['email']}")
        
        if info_empresa:
            ws.merge_cells(f'A{row}:D{row}')
            cell = ws[f'A{row}']
            cell.value = ' | '.join(info_empresa)
            cell.font = font_subtitle
            cell.alignment = align_center
            row += 1
        
        row += 1  # Espacio
        
        # === TÍTULO COTIZACIÓN ===
        ws.merge_cells(f'A{row}:D{row}')
        cell = ws[f'A{row}']
        cell.value = 'COTIZACIÓN'
        cell.font = font_heading
        cell.alignment = align_center
        cell.fill = fill_light
        row += 2
        
        # === INFORMACIÓN DE COTIZACIÓN ===
        # Número y Fecha
        ws[f'A{row}'] = 'Cotización No:'
        ws[f'A{row}'].font = font_bold
        ws[f'B{row}'] = cotizacion_data['numero_cotizacion']
        ws[f'C{row}'] = 'Fecha:'
        ws[f'C{row}'].font = font_bold
        ws[f'D{row}'] = cotizacion_data['fecha']
        row += 1
        
        # Cliente
        ws[f'A{row}'] = 'Cliente:'
        ws[f'A{row}'].font = font_bold
        ws[f'B{row}'] = cotizacion_data['cliente']['nombre']
        ws[f'C{row}'] = 'Teléfono:'
        ws[f'C{row}'].font = font_bold
        ws[f'D{row}'] = cotizacion_data['cliente'].get('telefono', '')
        row += 1
        
        # Email y Estatus
        ws[f'A{row}'] = 'Email:'
        ws[f'A{row}'].font = font_bold
        ws[f'B{row}'] = cotizacion_data['cliente'].get('email', '')
        ws[f'C{row}'] = 'Estatus:'
        ws[f'C{row}'].font = font_bold
        ws[f'D{row}'] = cotizacion_data['estatus']
        row += 2
        
        # === TABLA DE CONCEPTOS ===
        # Encabezados
        headers = ['Cantidad', 'Descripción', 'Precio Unitario', 'Total']
        for col_num, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col_num)
            cell.value = header  # type: ignore
            cell.font = Font(name='Arial', size=10, bold=True, color='FFFFFF')
            cell.fill = fill_header
            cell.alignment = align_center
            cell.border = border_thin
        
        row += 1
        start_detail_row = row
        
        # Detalles
        for detalle in cotizacion_data['detalles']:
            ws[f'A{row}'] = detalle['cantidad']
            ws[f'A{row}'].alignment = align_center
            ws[f'A{row}'].border = border_thin
            
            ws[f'B{row}'] = detalle['descripcion']
            ws[f'B{row}'].alignment = align_left
            ws[f'B{row}'].border = border_thin
            
            ws[f'C{row}'] = detalle['precio_unitario']
            ws[f'C{row}'].number_format = '$#,##0.00'
            ws[f'C{row}'].alignment = align_right
            ws[f'C{row}'].border = border_thin
            
            ws[f'D{row}'] = detalle['total_linea']
            ws[f'D{row}'].number_format = '$#,##0.00'
            ws[f'D{row}'].alignment = align_right
            ws[f'D{row}'].border = border_thin
            
            # Alternar color de fondo
            if (row - start_detail_row) % 2 == 1:
                for col in range(1, 5):
                    ws.cell(row=row, column=col).fill = fill_light
            
            row += 1
        
        row += 1
        
        # === TOTALES ===
        # Subtotal
        ws[f'C{row}'] = 'Subtotal:'
        ws[f'C{row}'].font = font_bold
        ws[f'C{row}'].alignment = align_right
        ws[f'D{row}'] = cotizacion_data['subtotal']
        ws[f'D{row}'].number_format = '$#,##0.00'
        ws[f'D{row}'].alignment = align_right
        ws[f'D{row}'].font = font_normal
        row += 1
        
        # IVA
        ws[f'C{row}'] = 'IVA (16%):'
        ws[f'C{row}'].font = font_bold
        ws[f'C{row}'].alignment = align_right
        ws[f'D{row}'] = cotizacion_data['impuestos']
        ws[f'D{row}'].number_format = '$#,##0.00'
        ws[f'D{row}'].alignment = align_right
        ws[f'D{row}'].font = font_normal
        row += 1
        
        # Total
        ws[f'C{row}'] = 'TOTAL:'
        ws[f'C{row}'].font = Font(name='Arial', size=12, bold=True, color='27AE60')
        ws[f'C{row}'].alignment = align_right
        ws[f'D{row}'] = cotizacion_data['total']
        ws[f'D{row}'].number_format = '$#,##0.00'
        ws[f'D{row}'].alignment = align_right
        ws[f'D{row}'].font = Font(name='Arial', size=12, bold=True, color='27AE60')
        ws[f'D{row}'].border = Border(top=Side(style='medium', color='27AE60'))
        row += 2
        
        # === NOTAS ===
        if cotizacion_data.get('notas'):
            ws.merge_cells(f'A{row}:D{row}')
            cell = ws[f'A{row}']
            cell.value = 'Notas:'
            cell.font = font_bold
            cell.alignment = align_left
            row += 1
            
            ws.merge_cells(f'A{row}:D{row}')
            cell = ws[f'A{row}']
            cell.value = cotizacion_data['notas']
            cell.font = font_normal
            cell.alignment = align_left
            row += 1
        
        # === PIE DE PÁGINA ===
        row += 1
        ws.merge_cells(f'A{row}:D{row}')
        cell = ws[f'A{row}']
        cell.value = f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        cell.font = Font(name='Arial', size=8, color='95A5A6')
        cell.alignment = align_center
        
        # Guardar archivo
        wb.save(filepath)
        
        return filepath
