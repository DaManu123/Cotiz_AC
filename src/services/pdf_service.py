import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class PDFService:
    """
    Servicio para generación de PDFs de cotizaciones.
    Replica exactamente el formato ProForma de Multiservicios RMG.
    
    Colores corporativos:
        Azul: #08568D (encabezados)
        Gris: #F3F3F3 (bloque datos empresa)
    """
    
    # ── Colores corporativos ──
    AZUL = colors.HexColor('#08568D')
    GRIS = colors.HexColor('#F3F3F3')
    BLANCO = colors.white
    NEGRO = colors.black
    GRIS_TEXTO = colors.HexColor('#444444')
    GRIS_CLARO = colors.HexColor('#888888')
    
    def __init__(self, output_dir: str = 'exports/pdf'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    # ══════════════════════════════════════════════════════════
    #  ESTILOS PERSONALIZADOS
    # ══════════════════════════════════════════════════════════
    
    def _crear_estilos(self) -> dict:
        """Crea estilos de párrafo corporativos."""
        base = getSampleStyleSheet()
        
        return {
            'base': base,
            'empresa_nombre': ParagraphStyle(
                'EmpresaNombre',
                parent=base['Heading1'],
                fontSize=16,
                textColor=self.AZUL,
                alignment=TA_CENTER,
                spaceAfter=2,
                spaceBefore=0,
                fontName='Helvetica-Bold',
            ),
            'empresa_dato': ParagraphStyle(
                'EmpresaDato',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.NEGRO,
                alignment=TA_LEFT,
                fontName='Helvetica',
                leftIndent=6,
            ),
            'empresa_dato_bold': ParagraphStyle(
                'EmpresaDatoBold',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.NEGRO,
                alignment=TA_LEFT,
                fontName='Helvetica-Bold',
                leftIndent=6,
            ),
            'proforma_title': ParagraphStyle(
                'ProformaTitle',
                parent=base['Heading1'],
                fontSize=14,
                textColor=self.BLANCO,
                alignment=TA_LEFT,
                fontName='Helvetica-Bold',
                spaceAfter=0,
                spaceBefore=0,
            ),
            'header_white': ParagraphStyle(
                'HeaderWhite', 
                parent=base['Normal'],
                fontSize=11,
                textColor=self.BLANCO,
                alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'header_white_center': ParagraphStyle(
                'HeaderWhiteCenter',
                parent=base['Normal'],
                fontSize=11,
                textColor=self.BLANCO,
                alignment=TA_CENTER,
                fontName='Helvetica',
            ),
            'info_label': ParagraphStyle(
                'InfoLabel',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.AZUL,
                fontName='Helvetica-Bold',
            ),
            'info_value': ParagraphStyle(
                'InfoValue',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.NEGRO,
                fontName='Helvetica',
            ),
            'table_header': ParagraphStyle(
                'TableHeader',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.BLANCO,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
            ),
            'cell_center': ParagraphStyle(
                'CellCenter',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.NEGRO,
                alignment=TA_CENTER,
                fontName='Helvetica',
            ),
            'cell_right': ParagraphStyle(
                'CellRight',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.NEGRO,
                alignment=TA_RIGHT,
                fontName='Helvetica',
            ),
            'totales_label': ParagraphStyle(
                'TotalesLabel',
                parent=base['Normal'],
                fontSize=11,
                textColor=self.NEGRO,
                alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'totales_valor': ParagraphStyle(
                'TotalesValor',
                parent=base['Normal'],
                fontSize=11,
                textColor=self.NEGRO,
                alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'total_final_label': ParagraphStyle(
                'TotalFinalLabel',
                parent=base['Normal'],
                fontSize=12,
                textColor=self.AZUL,
                alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'total_final_valor': ParagraphStyle(
                'TotalFinalValor',
                parent=base['Normal'],
                fontSize=12,
                textColor=self.AZUL,
                alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'notas_title': ParagraphStyle(
                'NotasTitle',
                parent=base['Normal'],
                fontSize=10,
                textColor=self.AZUL,
                fontName='Helvetica-Bold',
                spaceAfter=4,
            ),
            'notas_texto': ParagraphStyle(
                'NotasTexto',
                parent=base['Normal'],
                fontSize=9,
                textColor=self.GRIS_TEXTO,
                fontName='Helvetica',
                leftIndent=10,
            ),
            'pie': ParagraphStyle(
                'Pie',
                parent=base['Normal'],
                fontSize=8,
                textColor=self.GRIS_CLARO,
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique',
            ),
            'agradecimiento': ParagraphStyle(
                'Agradecimiento',
                parent=base['Normal'],
                fontSize=9,
                textColor=self.AZUL,
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique',
            ),
        }
    
    # ══════════════════════════════════════════════════════════
    #  BLOQUE EMPRESA
    # ══════════════════════════════════════════════════════════
    
    def _bloque_empresa(self, empresa_data: dict, estilos: dict) -> list:
        """Genera los elementos del bloque superior de empresa."""
        elements = []
        s = estilos
        
        # Nombre empresa
        elements.append(Paragraph(
            empresa_data.get('nombre', 'EMPRESA'), s['empresa_nombre']
        ))
        
        # Línea azul separadora
        elements.append(HRFlowable(
            width="100%", thickness=3, color=self.AZUL,
            spaceBefore=4, spaceAfter=8
        ))
        
        # Datos empresa en tabla con fondo gris
        datos_filas = []
        if empresa_data.get('direccion'):
            datos_filas.append([
                Paragraph('Dirección:', s['empresa_dato_bold']),
                Paragraph(empresa_data['direccion'], s['empresa_dato'])
            ])
        if empresa_data.get('telefono'):
            datos_filas.append([
                Paragraph('Teléfono:', s['empresa_dato_bold']),
                Paragraph(empresa_data['telefono'], s['empresa_dato'])
            ])
        if empresa_data.get('email'):
            datos_filas.append([
                Paragraph('Correo:', s['empresa_dato_bold']),
                Paragraph(empresa_data['email'], s['empresa_dato'])
            ])
        if empresa_data.get('redes_sociales'):
            datos_filas.append([
                Paragraph('Redes:', s['empresa_dato_bold']),
                Paragraph(empresa_data['redes_sociales'], s['empresa_dato'])
            ])
        if empresa_data.get('rfc'):
            datos_filas.append([
                Paragraph('RFC:', s['empresa_dato_bold']),
                Paragraph(empresa_data['rfc'], s['empresa_dato'])
            ])
        
        if datos_filas:
            # Tabla de datos empresa alineada a la derecha (columnas D-H del Excel)
            page_width = letter[0] - 1 * inch  # ancho disponible
            t = Table(datos_filas, colWidths=[1.2 * inch, page_width - 1.2 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.GRIS),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(t)
        
        elements.append(Spacer(1, 0.2 * inch))
        return elements
    
    # ══════════════════════════════════════════════════════════
    #  BARRA PROFORMA + DATOS CLIENTE
    # ══════════════════════════════════════════════════════════
    
    def _barra_proforma(self, cotizacion_data: dict, estilos: dict) -> list:
        """Genera la barra azul PROFORMA con número y fecha, más datos cliente."""
        elements = []
        s = estilos
        page_width = letter[0] - 1 * inch
        
        # Formatear fecha
        fecha_str = cotizacion_data.get('fecha', '')
        try:
            fecha_obj = datetime.strptime(str(fecha_str), '%Y-%m-%d')
            fecha_fmt = fecha_obj.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            fecha_fmt = str(fecha_str) if fecha_str else datetime.now().strftime('%d/%m/%Y')
        
        # Barra azul: PROFORMA | No. | Fecha
        barra_data = [[
            Paragraph('PROFORMA', s['proforma_title']),
            Paragraph(f"No. {cotizacion_data.get('numero_cotizacion', '')}", s['header_white']),
            Paragraph(fecha_fmt, s['header_white_center']),
        ]]
        
        barra = Table(barra_data, colWidths=[
            page_width * 0.35, page_width * 0.40, page_width * 0.25
        ])
        barra.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.AZUL),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (0, 0), 10),
        ]))
        elements.append(barra)
        
        # Datos del cliente
        cliente = cotizacion_data.get('cliente', {})
        if isinstance(cliente, dict) and cliente:
            nombre = cliente.get('nombre', '')
            telefono = cliente.get('telefono', '')
            estatus = cotizacion_data.get('estatus', 'Borrador')
            
            cli_data = [[
                Paragraph('Cliente:', s['info_label']),
                Paragraph(nombre, s['info_value']),
                Paragraph(f'Tel: {telefono}' if telefono else '', s['info_value']),
                Paragraph(estatus, s['info_label']),
            ]]
            
            cli_table = Table(cli_data, colWidths=[
                0.8 * inch, page_width * 0.40, page_width * 0.30, page_width * 0.15
            ])
            cli_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(cli_table)
        
        # Línea separadora azul
        elements.append(HRFlowable(
            width="100%", thickness=2, color=self.AZUL,
            spaceBefore=2, spaceAfter=6
        ))
        
        return elements
    
    # ══════════════════════════════════════════════════════════
    #  TABLA DE CONCEPTOS
    # ══════════════════════════════════════════════════════════
    
    def _tabla_conceptos(self, cotizacion_data: dict, estilos: dict) -> list:
        """Genera la tabla de conceptos con encabezados azules."""
        elements = []
        s = estilos
        page_width = letter[0] - 1 * inch
        
        # Encabezados: IVA | CANT. | DESCRIPCIÓN | PRECIO UNIT. | IMPORTE | TOTAL C/IVA
        headers = [
            Paragraph('IVA', s['table_header']),
            Paragraph('CANT.', s['table_header']),
            Paragraph('DESCRIPCIÓN', s['table_header']),
            Paragraph('PRECIO UNIT.', s['table_header']),
            Paragraph('IMPORTE', s['table_header']),
            Paragraph('TOTAL C/IVA', s['table_header']),
        ]
        
        table_data = [headers]
        
        # Filas de datos
        detalles = cotizacion_data.get('detalles', [])
        for det in detalles:
            cantidad = det.get('cantidad', 0)
            descripcion = det.get('descripcion', '')
            precio_unitario = det.get('precio_unitario', 0)
            importe = cantidad * precio_unitario
            iva = importe * 0.16
            total_iva = importe + iva
            
            table_data.append([
                Paragraph(f'${iva:,.2f}', s['cell_center']),
                Paragraph(f'{int(cantidad)}', s['cell_center']),
                Paragraph(descripcion, s['cell_center']),
                Paragraph(f'${precio_unitario:,.2f}', s['cell_right']),
                Paragraph(f'${importe:,.2f}', s['cell_right']),
                Paragraph(f'${total_iva:,.2f}', s['cell_right']),
            ])
        
        # Filas vacías para mínimo 5 filas de datos
        filas_extra = max(0, 5 - len(detalles))
        for _ in range(filas_extra):
            table_data.append([  # type: ignore
                Paragraph('', s['cell_center']),
                Paragraph('', s['cell_center']),
                Paragraph('', s['cell_center']),
                Paragraph('', s['cell_right']),
                Paragraph('', s['cell_right']),
                Paragraph('', s['cell_right']),
            ])
        
        # Anchos proporcionales a las columnas del Excel
        col_widths = [
            page_width * 0.10,  # IVA (A+B)
            page_width * 0.08,  # CANT (C)
            page_width * 0.32,  # DESC (D+E)
            page_width * 0.16,  # P.U. (F)
            page_width * 0.17,  # IMPORTE (G)
            page_width * 0.17,  # TOTAL C/IVA (H)
        ]
        
        conceptos = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        num_rows = len(table_data)
        style_cmds = [
            # Encabezado azul
            ('BACKGROUND', (0, 0), (-1, 0), self.AZUL),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.BLANCO),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9.5),
            ('ALIGN', (0, 1), (1, -1), 'CENTER'),   # IVA y CANT centrados
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),    # DESC centrada
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),    # Precios a la derecha
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordes finos
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            
            # Padding
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]
        
        # Bordes blancos entre encabezados
        for i in range(6):
            style_cmds.append(('BOX', (i, 0), (i, 0), 1, self.BLANCO))
        
        conceptos.setStyle(TableStyle(style_cmds))
        elements.append(conceptos)
        
        return elements
    
    # ══════════════════════════════════════════════════════════
    #  BLOQUE DE TOTALES
    # ══════════════════════════════════════════════════════════
    
    def _bloque_totales(self, cotizacion_data: dict, estilos: dict) -> list:
        """Genera el bloque de Subtotal, IVA y Total."""
        elements = []
        s = estilos
        page_width = letter[0] - 1 * inch
        
        subtotal = cotizacion_data.get('subtotal', 0) or 0
        impuestos = cotizacion_data.get('impuestos', 0) or 0
        total = cotizacion_data.get('total', 0) or 0
        
        elements.append(Spacer(1, 0.15 * inch))
        
        totales_data = [
            [
                '',
                Paragraph('Subtotal:', s['totales_label']),
                Paragraph(f'${subtotal:,.2f}', s['totales_valor']),
            ],
            [
                '',
                Paragraph('IVA (16%):', s['totales_label']),
                Paragraph(f'${impuestos:,.2f}', s['totales_valor']),
            ],
            [
                '',
                Paragraph('TOTAL:', s['total_final_label']),
                Paragraph(f'${total:,.2f}', s['total_final_valor']),
            ],
        ]
        
        totales = Table(totales_data, colWidths=[
            page_width * 0.50, page_width * 0.25, page_width * 0.25
        ])
        totales.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            # Línea sobre TOTAL
            ('LINEABOVE', (1, 2), (2, 2), 2, self.AZUL),
            # Doble línea debajo del TOTAL
            ('LINEBELOW', (1, 2), (2, 2), 0.5, self.AZUL),
        ]))
        
        elements.append(totales)
        return elements
    
    # ══════════════════════════════════════════════════════════
    #  NOTAS Y PIE
    # ══════════════════════════════════════════════════════════
    
    def _bloque_notas(self, cotizacion_data: dict, estilos: dict) -> list:
        """Genera el bloque de notas/condiciones."""
        elements = []
        s = estilos
        notas = cotizacion_data.get('notas', '')
        if not notas:
            return elements
        
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(HRFlowable(
            width="100%", thickness=1, color=self.AZUL,
            spaceBefore=0, spaceAfter=4
        ))
        elements.append(Paragraph('Notas / Condiciones:', s['notas_title']))
        
        for linea in notas.split('\n'):
            if linea.strip():
                elements.append(Paragraph(f"• {linea.strip()}", s['notas_texto']))
        
        return elements
    
    def _bloque_pie(self, empresa_data: dict, estilos: dict) -> list:
        """Genera el pie de página."""
        elements = []
        s = estilos
        
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(HRFlowable(
            width="100%", thickness=3, color=self.AZUL,
            spaceBefore=0, spaceAfter=6
        ))
        
        nombre = empresa_data.get('nombre', '')
        elements.append(Paragraph(
            f"{nombre} — Gracias por su preferencia",
            s['agradecimiento']
        ))
        
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(
            f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            s['pie']
        ))
        
        return elements
    
    # ══════════════════════════════════════════════════════════
    #  MÉTODO PRINCIPAL – GENERAR COTIZACIÓN
    # ══════════════════════════════════════════════════════════
    
    def generar_cotizacion(self, cotizacion_data: dict, empresa_data: dict) -> str:
        """
        Genera un PDF de cotización replicando el formato ProForma.
        
        Args:
            cotizacion_data: dict con datos completos de la cotización
            empresa_data: dict con datos de la empresa
        
        Returns:
            str: ruta del archivo generado
        """
        numero = cotizacion_data.get('numero_cotizacion', 'SIN-NUMERO')
        filename = f"{str(numero).replace('/', '-')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch
        )
        
        estilos = self._crear_estilos()
        elements = []
        
        # 1. Bloque empresa
        elements.extend(self._bloque_empresa(empresa_data, estilos))
        
        # 2. Barra PROFORMA + datos cliente
        elements.extend(self._barra_proforma(cotizacion_data, estilos))
        
        # 3. Tabla de conceptos
        elements.extend(self._tabla_conceptos(cotizacion_data, estilos))
        
        # 4. Totales
        elements.extend(self._bloque_totales(cotizacion_data, estilos))
        
        # 5. Notas
        elements.extend(self._bloque_notas(cotizacion_data, estilos))
        
        # 6. Pie de página
        elements.extend(self._bloque_pie(empresa_data, estilos))
        
        doc.build(elements)
        return filepath
