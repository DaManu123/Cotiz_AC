import os
from datetime import datetime
from typing import Dict, Any, List
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.worksheet.worksheet import Worksheet


class ExcelService:
    """
    Servicio para generación de archivos Excel de cotizaciones.
    Replica exactamente el formato ProForma de Multiservicios RMG.
    
    Estructura de columnas (8 columnas, tamaño carta vertical):
        A=4.3, B=13, C=11.5, D=31.6, E=7.4, F=16.4, G=17.5, H=21.8
    
    Colores corporativos:
        Azul: #08568D (encabezados tabla)
        Gris: #F3F3F3 (bloque datos empresa)
    """
    
    # ── Colores corporativos exactos ──
    AZUL_CORP = '08568D'
    GRIS_CORP = 'F3F3F3'
    BLANCO = 'FFFFFF'
    NEGRO = '000000'
    
    # ── Anchos de columna exactos ──
    COL_WIDTHS = {
        'A': 4.3,
        'B': 13,
        'C': 11.5,
        'D': 31.6,
        'E': 7.4,
        'F': 16.4,
        'G': 17.5,
        'H': 21.8,
    }

    def __init__(self, output_dir: str = 'exports/excel'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    # ══════════════════════════════════════════════════════════
    #  ESTILOS REUTILIZABLES
    # ══════════════════════════════════════════════════════════
    
    def _crear_estilos(self) -> Dict[str, Any]:
        """Crea y retorna todos los estilos necesarios para la ProForma."""
        
        # ── Fuentes ──
        font_empresa_nombre = Font(name='Arial', size=16, bold=True, color=self.AZUL_CORP)
        font_empresa_datos = Font(name='Arial', size=10, color=self.NEGRO)
        font_empresa_datos_bold = Font(name='Arial', size=10, bold=True, color=self.NEGRO)
        font_header_tabla = Font(name='Arial', size=12, bold=True, color=self.BLANCO)
        font_contenido = Font(name='Arial', size=10.5, color=self.NEGRO)
        font_totales = Font(name='Arial', size=11, bold=True, color=self.NEGRO)
        font_total_final = Font(name='Arial', size=12, bold=True, color=self.AZUL_CORP)
        font_notas = Font(name='Arial', size=9, color='444444')
        font_pie = Font(name='Arial', size=8, color='888888', italic=True)
        font_proforma_title = Font(name='Arial', size=14, bold=True, color=self.BLANCO)
        font_info_label = Font(name='Arial', size=10, bold=True, color=self.AZUL_CORP)
        font_info_value = Font(name='Arial', size=10, color=self.NEGRO)
        
        # ── Rellenos ──
        fill_azul = PatternFill(start_color=self.AZUL_CORP, end_color=self.AZUL_CORP, fill_type='solid')
        fill_gris = PatternFill(start_color=self.GRIS_CORP, end_color=self.GRIS_CORP, fill_type='solid')
        fill_blanco = PatternFill(start_color=self.BLANCO, end_color=self.BLANCO, fill_type='solid')
        
        # ── Bordes ──
        border_thin = Border(
            left=Side(style='thin', color='CCCCCC'),
            right=Side(style='thin', color='CCCCCC'),
            top=Side(style='thin', color='CCCCCC'),
            bottom=Side(style='thin', color='CCCCCC')
        )
        border_bottom_azul = Border(
            bottom=Side(style='medium', color=self.AZUL_CORP)
        )
        border_bottom_thin = Border(
            bottom=Side(style='thin', color='CCCCCC')
        )
        
        # ── Alineaciones ──
        align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
        align_left = Alignment(horizontal='left', vertical='center', wrap_text=True)
        align_right = Alignment(horizontal='right', vertical='center')
        
        return {
            'font_empresa_nombre': font_empresa_nombre,
            'font_empresa_datos': font_empresa_datos,
            'font_empresa_datos_bold': font_empresa_datos_bold,
            'font_header_tabla': font_header_tabla,
            'font_contenido': font_contenido,
            'font_totales': font_totales,
            'font_total_final': font_total_final,
            'font_notas': font_notas,
            'font_pie': font_pie,
            'font_proforma_title': font_proforma_title,
            'font_info_label': font_info_label,
            'font_info_value': font_info_value,
            'fill_azul': fill_azul,
            'fill_gris': fill_gris,
            'fill_blanco': fill_blanco,
            'border_thin': border_thin,
            'border_bottom_azul': border_bottom_azul,
            'border_bottom_thin': border_bottom_thin,
            'align_center': align_center,
            'align_left': align_left,
            'align_right': align_right,
        }
    
    # ══════════════════════════════════════════════════════════
    #  CONFIGURACIÓN DE HOJA
    # ══════════════════════════════════════════════════════════
    
    def _configurar_hoja(self, ws: Worksheet) -> None:
        """Configura la hoja: anchos de columna, formato carta vertical, sin grid."""
        ws.title = "ProForma"
        
        for col_letter, width in self.COL_WIDTHS.items():
            ws.column_dimensions[col_letter].width = width
        
        ws.page_setup.paperSize = ws.PAPERSIZE_LETTER  # type: ignore
        ws.page_setup.orientation = 'portrait'
        ws.sheet_properties.pageSetUpPr.fitToPage = True  # type: ignore
        ws.page_margins.left = 0.5
        ws.page_margins.right = 0.5
        ws.page_margins.top = 0.5
        ws.page_margins.bottom = 0.5
        ws.sheet_view.showGridLines = False  # type: ignore
    
    # ══════════════════════════════════════════════════════════
    #  BLOQUE SUPERIOR – DATOS DE EMPRESA (filas 1-11)
    # ══════════════════════════════════════════════════════════
    
    def _escribir_encabezado_empresa(
        self, ws: Worksheet, empresa_data: Dict[str, Any], estilos: Dict[str, Any]
    ) -> int:
        """
        Escribe el bloque superior con datos de la empresa.
        
        - Filas 1-3: Nombre empresa grande (merge A1:H3)
        - Fila 4: Línea separadora azul
        - Fila 5: Espacio
        - Filas 6-10: Datos empresa sobre fondo gris en D6:H10
        - Fila 11: Espacio
        
        Returns:
            int: siguiente fila disponible (12)
        """
        s = estilos
        
        # ── Filas 1-3: Nombre de la empresa ──
        ws.merge_cells('A1:H3')
        cell = ws['A1']
        cell.value = empresa_data.get('nombre', 'EMPRESA')  # type: ignore
        cell.font = s['font_empresa_nombre']
        cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # ── Fila 4: Línea separadora azul ──
        for col in range(1, 9):
            ws.cell(row=4, column=col).fill = s['fill_azul']
        ws.row_dimensions[4].height = 4
        
        # ── Fila 5: Espacio ──
        ws.row_dimensions[5].height = 8
        
        # ── Filas 6-10: Datos de empresa con fondo gris ──
        datos_lineas: List[tuple] = []
        
        if empresa_data.get('direccion'):
            datos_lineas.append(('Dirección:', empresa_data['direccion']))
        if empresa_data.get('telefono'):
            datos_lineas.append(('Teléfono:', empresa_data['telefono']))
        if empresa_data.get('email'):
            datos_lineas.append(('Correo:', empresa_data['email']))
        if empresa_data.get('redes_sociales'):
            datos_lineas.append(('Redes:', empresa_data['redes_sociales']))
        if empresa_data.get('rfc'):
            datos_lineas.append(('RFC:', empresa_data['rfc']))
        
        # Asegurar 5 filas (6-10)
        while len(datos_lineas) < 5:
            datos_lineas.append(('', ''))
        
        for i, (label, value) in enumerate(datos_lineas[:5]):
            row_num = 6 + i
            
            # Fondo gris en D:H
            for col in range(4, 9):
                ws.cell(row=row_num, column=col).fill = s['fill_gris']
            
            if label:
                cell_label = ws.cell(row=row_num, column=4)
                cell_label.value = f"  {label}"  # type: ignore
                cell_label.font = s['font_empresa_datos_bold']
                cell_label.alignment = s['align_left']
                cell_label.fill = s['fill_gris']
                
                ws.merge_cells(f'E{row_num}:H{row_num}')
                cell_val = ws.cell(row=row_num, column=5)
                cell_val.value = value  # type: ignore
                cell_val.font = s['font_empresa_datos']
                cell_val.alignment = s['align_left']
                cell_val.fill = s['fill_gris']
        
        ws.row_dimensions[11].height = 12
        return 12
    
    # ══════════════════════════════════════════════════════════
    #  ENCABEZADO PRINCIPAL DE TABLA (fila 12+)
    # ══════════════════════════════════════════════════════════
    
    def _escribir_encabezado_tabla(
        self, ws: Worksheet, row: int, cotizacion_data: Dict[str, Any], estilos: Dict[str, Any]
    ) -> int:
        """
        Escribe:
            - Fila 12: Barra azul "PROFORMA" + No. + Fecha
            - Fila 13: Datos del cliente
            - Fila 14: Línea separadora
            - Fila 15: Encabezados azules de columnas
        
        Returns:
            int: siguiente fila (inicio de datos)
        """
        s = estilos
        
        # ═══ Fila 12: Barra azul PROFORMA ═══
        for col in range(1, 9):
            ws.cell(row=row, column=col).fill = s['fill_azul']
        ws.row_dimensions[row].height = 28
        
        # "PROFORMA" en A12:B12
        ws.merge_cells(f'A{row}:B{row}')
        cell_t = ws.cell(row=row, column=1)
        cell_t.value = "PROFORMA"  # type: ignore
        cell_t.font = s['font_proforma_title']
        cell_t.alignment = Alignment(horizontal='left', vertical='center')
        
        # No. en F12:G12
        ws.merge_cells(f'F{row}:G{row}')
        cell_n = ws.cell(row=row, column=6)
        cell_n.value = f"No. {cotizacion_data.get('numero_cotizacion', '')}"  # type: ignore
        cell_n.font = Font(name='Arial', size=11, bold=True, color=self.BLANCO)
        cell_n.alignment = Alignment(horizontal='right', vertical='center')
        
        # Fecha en H12
        fecha_str = cotizacion_data.get('fecha', '')
        try:
            fecha_obj = datetime.strptime(str(fecha_str), '%Y-%m-%d')
            fecha_fmt = fecha_obj.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            fecha_fmt = str(fecha_str) if fecha_str else datetime.now().strftime('%d/%m/%Y')
        
        cell_f = ws.cell(row=row, column=8)
        cell_f.value = fecha_fmt  # type: ignore
        cell_f.font = Font(name='Arial', size=11, color=self.BLANCO)
        cell_f.alignment = Alignment(horizontal='center', vertical='center')
        
        row += 1
        
        # ═══ Fila 13: Datos del cliente ═══
        ws.row_dimensions[row].height = 22
        
        cell_cli_lbl = ws.cell(row=row, column=1)
        cell_cli_lbl.value = "Cliente:"  # type: ignore
        cell_cli_lbl.font = s['font_info_label']
        cell_cli_lbl.alignment = s['align_left']
        
        ws.merge_cells(f'B{row}:D{row}')
        cliente = cotizacion_data.get('cliente', {})
        cell_cli_nom = ws.cell(row=row, column=2)
        cell_cli_nom.value = cliente.get('nombre', '') if isinstance(cliente, dict) else ''  # type: ignore
        cell_cli_nom.font = s['font_info_value']
        cell_cli_nom.alignment = s['align_left']
        
        ws.merge_cells(f'F{row}:G{row}')
        cell_tel = ws.cell(row=row, column=6)
        tel = cliente.get('telefono', '') if isinstance(cliente, dict) else ''
        cell_tel.value = f"Tel: {tel}" if tel else ''  # type: ignore
        cell_tel.font = s['font_info_value']
        cell_tel.alignment = s['align_right']
        
        cell_est = ws.cell(row=row, column=8)
        cell_est.value = cotizacion_data.get('estatus', 'Borrador')  # type: ignore
        cell_est.font = Font(name='Arial', size=10, bold=True, color=self.AZUL_CORP)
        cell_est.alignment = Alignment(horizontal='center', vertical='center')
        
        row += 1
        
        # ═══ Fila 14: Línea separadora ═══
        for col in range(1, 9):
            ws.cell(row=row, column=col).border = s['border_bottom_azul']
        ws.row_dimensions[row].height = 6
        row += 1
        
        # ═══ Fila 15: ENCABEZADOS TABLA (azul, texto blanco, negrita 12pt) ═══
        ws.row_dimensions[row].height = 25
        
        # Fondo azul completo A-H
        for col in range(1, 9):
            c = ws.cell(row=row, column=col)
            c.fill = s['fill_azul']
            c.border = Border(
                left=Side(style='thin', color=self.BLANCO),
                right=Side(style='thin', color=self.BLANCO),
                top=Side(style='thin', color=self.BLANCO),
                bottom=Side(style='thin', color=self.BLANCO),
            )
        
        # IVA en A:B (merge)
        ws.merge_cells(f'A{row}:B{row}')
        c_iva = ws.cell(row=row, column=1)
        c_iva.value = "IVA"  # type: ignore
        c_iva.font = s['font_header_tabla']
        c_iva.fill = s['fill_azul']
        c_iva.alignment = Alignment(horizontal='center', vertical='center')
        
        # CANT. en C
        c_cant = ws.cell(row=row, column=3)
        c_cant.value = "CANT."  # type: ignore
        c_cant.font = s['font_header_tabla']
        c_cant.alignment = Alignment(horizontal='center', vertical='center')
        
        # DESCRIPCIÓN en D:E (merge)
        ws.merge_cells(f'D{row}:E{row}')
        c_desc = ws.cell(row=row, column=4)
        c_desc.value = "DESCRIPCIÓN"  # type: ignore
        c_desc.font = s['font_header_tabla']
        c_desc.fill = s['fill_azul']
        c_desc.alignment = Alignment(horizontal='center', vertical='center')
        
        # PRECIO UNIT. en F
        c_pu = ws.cell(row=row, column=6)
        c_pu.value = "PRECIO UNIT."  # type: ignore
        c_pu.font = s['font_header_tabla']
        c_pu.alignment = Alignment(horizontal='center', vertical='center')
        
        # IMPORTE en G
        c_imp = ws.cell(row=row, column=7)
        c_imp.value = "IMPORTE"  # type: ignore
        c_imp.font = s['font_header_tabla']
        c_imp.alignment = Alignment(horizontal='center', vertical='center')
        
        # TOTAL C/IVA en H
        c_tiva = ws.cell(row=row, column=8)
        c_tiva.value = "TOTAL C/IVA"  # type: ignore
        c_tiva.font = s['font_header_tabla']
        c_tiva.alignment = Alignment(horizontal='center', vertical='center')
        
        row += 1
        return row
    
    # ══════════════════════════════════════════════════════════
    #  FILAS DE CONCEPTOS (con fórmulas activas)
    # ══════════════════════════════════════════════════════════
    
    def _escribir_conceptos(
        self, ws: Worksheet, start_row: int, detalles: List[Dict[str, Any]], estilos: Dict[str, Any]
    ) -> int:
        """
        Escribe filas de conceptos con fórmulas de IVA automáticas.
        
        Columnas:
            A-B (merge): IVA = G*16%
            C:           Cantidad
            D-E (merge): Descripción
            F:           Precio unitario
            G:           Importe = C*F (fórmula)
            H:           Total con IVA = ((G*16%)+G) (fórmula)
        """
        s = estilos
        row = start_row
        
        if not detalles:
            for _ in range(5):
                self._fila_vacia(ws, row, s)
                row += 1
            return row
        
        for detalle in detalles:
            ws.row_dimensions[row].height = 22
            
            cantidad = detalle.get('cantidad', 0)
            descripcion = detalle.get('descripcion', '')
            precio_unitario = detalle.get('precio_unitario', 0)
            
            # A-B (merge): IVA = Importe * 16%
            ws.merge_cells(f'A{row}:B{row}')
            c_iva = ws.cell(row=row, column=1)
            c_iva.value = f'=G{row}*16%'  # type: ignore
            c_iva.font = s['font_contenido']
            c_iva.alignment = Alignment(horizontal='center', vertical='center')
            c_iva.border = s['border_thin']
            c_iva.number_format = '$#,##0.00'
            
            # C: Cantidad
            c_cant = ws.cell(row=row, column=3)
            c_cant.value = cantidad  # type: ignore
            c_cant.font = s['font_contenido']
            c_cant.alignment = Alignment(horizontal='center', vertical='center')
            c_cant.border = s['border_thin']
            c_cant.number_format = '0'
            
            # D-E (merge): Descripción
            ws.merge_cells(f'D{row}:E{row}')
            c_desc = ws.cell(row=row, column=4)
            c_desc.value = descripcion  # type: ignore
            c_desc.font = s['font_contenido']
            c_desc.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            c_desc.border = s['border_thin']
            
            # F: Precio unitario
            c_pu = ws.cell(row=row, column=6)
            c_pu.value = precio_unitario  # type: ignore
            c_pu.font = s['font_contenido']
            c_pu.alignment = Alignment(horizontal='right', vertical='center')
            c_pu.border = s['border_thin']
            c_pu.number_format = '$#,##0.00'
            
            # G: Importe = Cant × P.U. (fórmula)
            c_imp = ws.cell(row=row, column=7)
            c_imp.value = f'=C{row}*F{row}'  # type: ignore
            c_imp.font = s['font_contenido']
            c_imp.alignment = Alignment(horizontal='right', vertical='center')
            c_imp.border = s['border_thin']
            c_imp.number_format = '$#,##0.00'
            
            # H: Total con IVA = ((G*16%)+G) (fórmula exacta del original)
            c_tiva = ws.cell(row=row, column=8)
            c_tiva.value = f'=((G{row}*16%)+G{row})'  # type: ignore
            c_tiva.font = s['font_contenido']
            c_tiva.alignment = Alignment(horizontal='right', vertical='center')
            c_tiva.border = s['border_thin']
            c_tiva.number_format = '$#,##0.00'
            
            # Bordes en celdas que quedan fuera de merge (B, E)
            ws.cell(row=row, column=2).border = s['border_thin']
            ws.cell(row=row, column=5).border = s['border_thin']
            
            row += 1
        
        # Filas vacías para completar mínimo 10 filas de tabla
        filas_extra = max(0, 10 - len(detalles))
        for _ in range(filas_extra):
            self._fila_vacia(ws, row, s)
            row += 1
        
        return row
    
    def _fila_vacia(self, ws: Worksheet, row: int, estilos: Dict[str, Any]) -> None:
        """Escribe una fila vacía con bordes y merges correctos."""
        s = estilos
        ws.row_dimensions[row].height = 20
        ws.merge_cells(f'A{row}:B{row}')
        ws.merge_cells(f'D{row}:E{row}')
        for col in range(1, 9):
            ws.cell(row=row, column=col).border = s['border_thin']
    
    # ══════════════════════════════════════════════════════════
    #  BLOQUE DE TOTALES (con fórmulas SUM)
    # ══════════════════════════════════════════════════════════
    
    def _escribir_totales(
        self, ws: Worksheet, row: int, start_data_row: int, end_data_row: int,
        estilos: Dict[str, Any]
    ) -> int:
        """Escribe Subtotal, IVA y Total con fórmulas SUM activas."""
        s = estilos
        last = end_data_row - 1
        
        row += 1  # Espacio
        
        # ── SUBTOTAL ──
        ws.row_dimensions[row].height = 22
        ws.merge_cells(f'D{row}:F{row}')
        c_lbl = ws.cell(row=row, column=4)
        c_lbl.value = "Subtotal:"  # type: ignore
        c_lbl.font = s['font_totales']
        c_lbl.alignment = Alignment(horizontal='right', vertical='center')
        
        c_val = ws.cell(row=row, column=7)
        c_val.value = f'=SUM(G{start_data_row}:G{last})'  # type: ignore
        c_val.font = s['font_totales']
        c_val.alignment = Alignment(horizontal='right', vertical='center')
        c_val.number_format = '$#,##0.00'
        c_val.border = s['border_bottom_thin']
        row += 1
        
        # ── IVA (16%) ──
        ws.row_dimensions[row].height = 22
        ws.merge_cells(f'D{row}:F{row}')
        c_lbl = ws.cell(row=row, column=4)
        c_lbl.value = "IVA (16%):"  # type: ignore
        c_lbl.font = s['font_totales']
        c_lbl.alignment = Alignment(horizontal='right', vertical='center')
        
        c_val = ws.cell(row=row, column=7)
        c_val.value = f'=SUM(A{start_data_row}:A{last})'  # type: ignore
        c_val.font = s['font_totales']
        c_val.alignment = Alignment(horizontal='right', vertical='center')
        c_val.number_format = '$#,##0.00'
        c_val.border = s['border_bottom_thin']
        row += 1
        
        # ── TOTAL ──
        ws.row_dimensions[row].height = 26
        ws.merge_cells(f'D{row}:F{row}')
        c_lbl = ws.cell(row=row, column=4)
        c_lbl.value = "TOTAL:"  # type: ignore
        c_lbl.font = s['font_total_final']
        c_lbl.alignment = Alignment(horizontal='right', vertical='center')
        
        borde_total = Border(
            top=Side(style='medium', color=self.AZUL_CORP),
            bottom=Side(style='double', color=self.AZUL_CORP)
        )
        
        c_val = ws.cell(row=row, column=7)
        c_val.value = f'=SUM(H{start_data_row}:H{last})'  # type: ignore
        c_val.font = s['font_total_final']
        c_val.alignment = Alignment(horizontal='right', vertical='center')
        c_val.number_format = '$#,##0.00'
        c_val.border = borde_total
        
        c_h = ws.cell(row=row, column=8)
        c_h.value = f'=SUM(H{start_data_row}:H{last})'  # type: ignore
        c_h.font = s['font_total_final']
        c_h.alignment = Alignment(horizontal='right', vertical='center')
        c_h.number_format = '$#,##0.00'
        c_h.border = borde_total
        
        row += 2
        return row
    
    # ══════════════════════════════════════════════════════════
    #  NOTAS / CONDICIONES
    # ══════════════════════════════════════════════════════════
    
    def _escribir_notas(
        self, ws: Worksheet, row: int, cotizacion_data: Dict[str, Any], estilos: Dict[str, Any]
    ) -> int:
        """Escribe notas/condiciones de la cotización."""
        s = estilos
        notas = cotizacion_data.get('notas', '')
        if not notas:
            return row
        
        ws.merge_cells(f'A{row}:H{row}')
        c_t = ws.cell(row=row, column=1)
        c_t.value = "Notas / Condiciones:"  # type: ignore
        c_t.font = Font(name='Arial', size=10, bold=True, color=self.AZUL_CORP)
        c_t.alignment = s['align_left']
        c_t.border = Border(bottom=Side(style='thin', color=self.AZUL_CORP))
        row += 1
        
        for linea in notas.split('\n'):
            ws.merge_cells(f'A{row}:H{row}')
            c = ws.cell(row=row, column=1)
            c.value = f"  {linea.strip()}"  # type: ignore
            c.font = s['font_notas']
            c.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            row += 1
        
        row += 1
        return row
    
    # ══════════════════════════════════════════════════════════
    #  PIE DE PÁGINA
    # ══════════════════════════════════════════════════════════
    
    def _escribir_pie(
        self, ws: Worksheet, row: int, empresa_data: Dict[str, Any], estilos: Dict[str, Any]
    ) -> int:
        """Escribe pie de página con línea azul y texto."""
        s = estilos
        
        # Línea azul
        for col in range(1, 9):
            ws.cell(row=row, column=col).fill = s['fill_azul']
        ws.row_dimensions[row].height = 4
        row += 1
        
        # Agradecimiento
        ws.merge_cells(f'A{row}:H{row}')
        c = ws.cell(row=row, column=1)
        c.value = f"{empresa_data.get('nombre', '')} — Gracias por su preferencia"  # type: ignore
        c.font = Font(name='Arial', size=9, color=self.AZUL_CORP, italic=True)
        c.alignment = Alignment(horizontal='center', vertical='center')
        row += 1
        
        # Fecha generación
        ws.merge_cells(f'A{row}:H{row}')
        c = ws.cell(row=row, column=1)
        c.value = f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}"  # type: ignore
        c.font = s['font_pie']
        c.alignment = Alignment(horizontal='center', vertical='center')
        
        return row
    
    # ══════════════════════════════════════════════════════════
    #  MÉTODO PRINCIPAL – GENERAR COTIZACIÓN
    # ══════════════════════════════════════════════════════════
    
    def generar_cotizacion(self, cotizacion_data: Dict[str, Any], empresa_data: Dict[str, Any]) -> str:
        """
        Genera un archivo Excel de cotización replicando exactamente
        el formato ProForma profesional.
        
        Args:
            cotizacion_data: dict con datos completos de la cotización
            empresa_data: dict con datos de la empresa
        
        Returns:
            str: ruta del archivo generado
        """
        numero = cotizacion_data.get('numero_cotizacion', 'SIN-NUMERO')
        filename = f"{str(numero).replace('/', '-')}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        wb = Workbook()
        ws: Worksheet = wb.active  # type: ignore
        estilos = self._crear_estilos()
        
        # 1. Configurar hoja
        self._configurar_hoja(ws)
        
        # 2. Encabezado empresa (filas 1-11)
        row = self._escribir_encabezado_empresa(ws, empresa_data, estilos)
        
        # 3. Encabezado tabla + datos cotización (fila 12+)
        row = self._escribir_encabezado_tabla(ws, row, cotizacion_data, estilos)
        
        # 4. Conceptos (filas de datos con fórmulas)
        start_data_row = row
        detalles = cotizacion_data.get('detalles', [])
        row = self._escribir_conceptos(ws, row, detalles, estilos)
        end_data_row = row
        
        # 5. Totales (fórmulas SUM)
        row = self._escribir_totales(ws, row, start_data_row, end_data_row, estilos)
        
        # 6. Notas
        row = self._escribir_notas(ws, row, cotizacion_data, estilos)
        
        # 7. Pie de página
        self._escribir_pie(ws, row, empresa_data, estilos)
        
        wb.save(filepath)
        return filepath
