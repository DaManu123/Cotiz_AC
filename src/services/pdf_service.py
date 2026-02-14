import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class PDFService:
    """
    Servicio para generación de PDFs de cotizaciones.
    Replica exactamente el formato Pro-Forma de Multiservicios RMG.
    """

    # ── Colores corporativos ──
    AZUL = colors.HexColor('#08568D')
    GRIS = colors.HexColor('#F3F3F3')
    BLANCO = colors.white
    NEGRO = colors.black
    GRIS_TEXTO = colors.HexColor('#555555')
    GRIS_CLARO = colors.HexColor('#888888')

    # ── Ruta del logo ──
    LOGO_PATH = os.path.join('static', 'img', 'logormg.jpg')

    def __init__(self, output_dir: str = 'exports/pdf'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    # ══════════════════════════════════════════════════════════
    #  ESTILOS
    # ══════════════════════════════════════════════════════════

    def _crear_estilos(self) -> dict:
        base = getSampleStyleSheet()
        return {
            'base': base,
            # Header
            'proforma_title': ParagraphStyle(
                'ProformaTitle', parent=base['Heading1'],
                fontSize=22, textColor=self.AZUL, alignment=TA_RIGHT,
                fontName='Helvetica-Bold', spaceAfter=0, spaceBefore=0,
            ),
            'empresa_dato': ParagraphStyle(
                'EmpresaDato', parent=base['Normal'],
                fontSize=9, textColor=self.GRIS_TEXTO, alignment=TA_LEFT,
                fontName='Helvetica',
            ),
            'info_label': ParagraphStyle(
                'InfoLabel', parent=base['Normal'],
                fontSize=10, textColor=self.AZUL, fontName='Helvetica-Bold',
                alignment=TA_CENTER,
            ),
            'info_value': ParagraphStyle(
                'InfoValue', parent=base['Normal'],
                fontSize=10, textColor=self.NEGRO, fontName='Helvetica',
                alignment=TA_CENTER,
            ),
            # Table
            'table_header': ParagraphStyle(
                'TableHeader', parent=base['Normal'],
                fontSize=10, textColor=self.BLANCO, alignment=TA_CENTER,
                fontName='Helvetica-Bold',
            ),
            'cell_center': ParagraphStyle(
                'CellCenter', parent=base['Normal'],
                fontSize=9, textColor=self.NEGRO, alignment=TA_CENTER,
                fontName='Helvetica',
            ),
            'cell_right': ParagraphStyle(
                'CellRight', parent=base['Normal'],
                fontSize=9, textColor=self.NEGRO, alignment=TA_RIGHT,
                fontName='Helvetica',
            ),
            'grupo': ParagraphStyle(
                'Grupo', parent=base['Normal'],
                fontSize=9, textColor=self.AZUL, alignment=TA_CENTER,
                fontName='Helvetica-Bold',
            ),
            # Totals
            'totales_label': ParagraphStyle(
                'TotalesLabel', parent=base['Normal'],
                fontSize=10, textColor=self.NEGRO, alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'totales_valor': ParagraphStyle(
                'TotalesValor', parent=base['Normal'],
                fontSize=10, textColor=self.NEGRO, alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'pagado_label': ParagraphStyle(
                'PagadoLabel', parent=base['Normal'],
                fontSize=11, textColor=self.BLANCO, alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            'pagado_valor': ParagraphStyle(
                'PagadoValor', parent=base['Normal'],
                fontSize=11, textColor=self.BLANCO, alignment=TA_RIGHT,
                fontName='Helvetica-Bold',
            ),
            # Terms & Footer
            'terms_title': ParagraphStyle(
                'TermsTitle', parent=base['Normal'],
                fontSize=9, textColor=self.AZUL, fontName='Helvetica-Bold',
                spaceAfter=4,
            ),
            'terms_text': ParagraphStyle(
                'TermsText', parent=base['Normal'],
                fontSize=8, textColor=self.GRIS_TEXTO, fontName='Helvetica',
                leftIndent=6,
            ),
            'footer': ParagraphStyle(
                'Footer', parent=base['Normal'],
                fontSize=9, textColor=self.AZUL, alignment=TA_CENTER,
                fontName='Helvetica-Bold',
            ),
            'footer_sub': ParagraphStyle(
                'FooterSub', parent=base['Normal'],
                fontSize=8, textColor=self.GRIS_CLARO, alignment=TA_CENTER,
                fontName='Helvetica-Oblique',
            ),
        }

    # ══════════════════════════════════════════════════════════
    #  ENCABEZADO: LOGO + PRO-FORMA + INFO + FECHA/N°
    # ══════════════════════════════════════════════════════════

    def _bloque_encabezado(self, empresa_data: dict, cotizacion_data: dict, estilos: dict) -> list:
        elements: list = []
        s = estilos
        page_width = letter[0] - 0.7 * inch  # ancho útil con márgenes 0.35+0.35
        # ── Row 1: Logo left + PRO-FORMA right ──
        logo_cell: object
        if os.path.exists(self.LOGO_PATH):
            logo_cell = Image(self.LOGO_PATH, width=2.3 * inch, height=1.05 * inch)
        else:
            logo_cell = Paragraph(empresa_data.get('nombre', ''), s['proforma_title'])

        header_data = [[
            logo_cell,
            Paragraph('PRO-FORMA', s['proforma_title']),
        ]]
        header_table = Table(
            header_data,
            colWidths=[page_width * 0.45, page_width * 0.55],
            rowHeights=[1.2 * inch],  # altura fija para centrar ambos verticalmente
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),      # logo a la izquierda
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),      # PRO-FORMA a la derecha
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (0, 0), 4),      # margen izquierdo del logo
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.15 * inch))

        # ── Row 2: Company info left + Fecha/N° right ──
        # Iconos PNG para cada dato de empresa
        ICONS_DIR = os.path.join('static', 'img', 'icons')
        icon_map = {
            'direccion': os.path.join(ICONS_DIR, 'icons8-location-pin-48.png'),
            'telefono': os.path.join(ICONS_DIR, 'icons8-phone-48.png'),
            'email': os.path.join(ICONS_DIR, 'icons8-email-48.png'),
            'redes_sociales': os.path.join(ICONS_DIR, 'icons8-web-48.png'),
            'rfc': os.path.join(ICONS_DIR, 'icons8-id-card-48.png'),
        }
        icon_size = 11  # puntos (tamaño del icono en el PDF)

        info_rows: list = []
        campos = [
            ('direccion', empresa_data.get('direccion', '')),
            ('telefono', empresa_data.get('telefono', '')),
            ('email', empresa_data.get('email', '')),
            ('redes_sociales', empresa_data.get('redes_sociales', '')),
            ('rfc', empresa_data.get('rfc', '')),
        ]
        for campo, valor in campos:
            if valor:
                icon_path = icon_map.get(campo, '')
                if os.path.exists(icon_path):
                    icon_img = Image(icon_path, width=icon_size, height=icon_size)
                else:
                    icon_img = Paragraph('', s['empresa_dato'])
                info_rows.append([icon_img, Paragraph(valor, s['empresa_dato'])])

        if info_rows:
            info_mini_table = Table(info_rows, colWidths=[16, page_width * 0.55 - 20])
            info_mini_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('LEFTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 2),
                ('LEFTPADDING', (1, 0), (1, -1), 2),
            ]))
        else:
            info_mini_table = Paragraph('', s['empresa_dato'])

        # Fecha / N° as small table
        fecha_str = cotizacion_data.get('fecha', '')
        try:
            fecha_obj = datetime.strptime(str(fecha_str), '%Y-%m-%d')
            fecha_fmt = fecha_obj.strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            fecha_fmt = str(fecha_str) if fecha_str else datetime.now().strftime('%d/%m/%Y')

        fecha_n_data = [
            [Paragraph('Fecha', s['info_label']),
             Paragraph(fecha_fmt, s['info_value'])],
            [Paragraph('N° de Pro-forma', s['info_label']),
             Paragraph(cotizacion_data.get('numero_cotizacion', ''), s['info_value'])],
        ]
        fecha_table = Table(fecha_n_data, colWidths=[1.4 * inch, 1.2 * inch])
        fecha_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, self.AZUL),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, self.AZUL),
            ('BACKGROUND', (0, 0), (0, -1), self.GRIS),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        info_row_data = [[info_mini_table, fecha_table]]
        info_table = Table(info_row_data, colWidths=[page_width * 0.55, page_width * 0.45])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.15 * inch))

        return elements

    # ══════════════════════════════════════════════════════════
    #  TABLA DE CONCEPTOS
    # ══════════════════════════════════════════════════════════

    def _tabla_conceptos(self, cotizacion_data: dict, estilos: dict) -> list:
        elements: list = []
        s = estilos
        page_width = letter[0] - 0.7 * inch  # ancho útil con márgenes 0.35+0.35

        # Column widths: IVA | CANT | DESC | P.U. | TOTAL
        col_widths = [
            page_width * 0.13,
            page_width * 0.08,
            page_width * 0.39,
            page_width * 0.18,
            page_width * 0.22,
        ]

        # Headers
        headers = [
            Paragraph('IVA', s['table_header']),
            Paragraph('CANT.', s['table_header']),
            Paragraph('DESCRIPCIÓN', s['table_header']),
            Paragraph('P. UNITARIO', s['table_header']),
            Paragraph('TOTAL', s['table_header']),
        ]
        table_data: list = [headers]

        # Data rows (with group separators)
        detalles = cotizacion_data.get('detalles', [])
        current_grupo = None

        for det in detalles:
            grupo = det.get('grupo', '') or ''

            # Group separator
            if grupo and grupo != current_grupo:
                current_grupo = grupo
                table_data.append([
                    Paragraph(grupo, s['grupo']), '', '', '', ''
                ])

            cantidad = det.get('cantidad', 0)
            precio_unitario = det.get('precio_unitario', 0)
            importe = cantidad * precio_unitario
            iva_total = importe * 1.16

            table_data.append([
                Paragraph(f'{iva_total:,.2f}', s['cell_right']),
                Paragraph(f'{int(cantidad)}' if cantidad == int(cantidad) else f'{cantidad}', s['cell_center']),
                Paragraph(det.get('descripcion', ''), s['cell_center']),
                Paragraph(f'{precio_unitario:,.2f}', s['cell_right']),
                Paragraph(f'{importe:,.2f}', s['cell_right']),
            ])

        # Empty rows to fill min 15 rows
        data_row_count = len(table_data) - 1  # minus header
        filas_extra = max(0, 10 - data_row_count)
        for _ in range(filas_extra):
            table_data.append([
                Paragraph('0.00', s['cell_right']),
                Paragraph('', s['cell_center']),
                Paragraph('', s['cell_center']),
                Paragraph('0.00', s['cell_right']),
                Paragraph('0.00', s['cell_right']),
            ])

        conceptos = Table(table_data, colWidths=col_widths, repeatRows=1)

        num_rows = len(table_data)
        style_cmds = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.AZUL),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.BLANCO),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            # Content
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]

        # White borders between header cells
        for i in range(5):
            style_cmds.append(('BOX', (i, 0), (i, 0), 1, self.BLANCO))

        # Group separator rows: span all columns, gray background
        for row_idx in range(1, num_rows):
            row_data = table_data[row_idx]
            if isinstance(row_data[1], str) and row_data[1] == '' and isinstance(row_data[0], Paragraph):
                # Check if it's a grupo row (only first cell has content)
                txt = row_data[0].text if hasattr(row_data[0], 'text') else ''  # type: ignore
                if txt and not any(c in txt for c in ['0.00', ',']):
                    style_cmds.append(('SPAN', (0, row_idx), (4, row_idx)))
                    style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), self.GRIS))
                    style_cmds.append(('ALIGN', (0, row_idx), (-1, row_idx), 'CENTER'))

        conceptos.setStyle(TableStyle(style_cmds))
        elements.append(conceptos)

        return elements

    # ══════════════════════════════════════════════════════════
    #  BLOQUE DE TOTALES
    # ══════════════════════════════════════════════════════════

    def _bloque_totales(self, cotizacion_data: dict, estilos: dict) -> list:
        elements: list = []
        s = estilos
        page_width = letter[0] - 0.7 * inch  # ancho útil con márgenes 0.35+0.35

        subtotal = cotizacion_data.get('subtotal', 0) or 0
        descuento = cotizacion_data.get('descuento', 0) or 0
        envio = cotizacion_data.get('envio_delivery', 0) or 0
        neto = subtotal - descuento
        impuestos = neto * 0.16
        pagado = neto + impuestos + envio

        elements.append(Spacer(1, 0.1 * inch))

        totales_data = [
            ['', Paragraph('Total parcial', s['totales_label']),
             Paragraph(f'${subtotal:,.2f}', s['totales_valor'])],
            ['', Paragraph('Descuento ($)', s['totales_label']),
             Paragraph(f'${descuento:,.2f}', s['totales_valor'])],
            ['', Paragraph('NETO', s['totales_label']),
             Paragraph(f'${neto:,.2f}', s['totales_valor'])],
            ['', Paragraph('Impuesto (IVA)', s['totales_label']),
             Paragraph(f'${impuestos:,.2f}', s['totales_valor'])],
            ['', Paragraph('Envío Delivery', s['totales_label']),
             Paragraph(f'${envio:,.2f}', s['totales_valor'])],
            ['', Paragraph('Pagado', s['pagado_label']),
             Paragraph(f'${pagado:,.2f}', s['pagado_valor'])],
        ]

        totales = Table(totales_data, colWidths=[
            page_width * 0.45, page_width * 0.28, page_width * 0.27
        ])
        totales.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LINEBELOW', (1, 0), (2, 4), 0.5, colors.HexColor('#CCCCCC')),
            # Pagado row (last) - blue background
            ('BACKGROUND', (1, 5), (2, 5), self.AZUL),
            ('BOX', (1, 5), (2, 5), 2, self.AZUL),
        ]))
        elements.append(totales)

        return elements

    # ══════════════════════════════════════════════════════════
    #  TÉRMINOS Y PIE
    # ══════════════════════════════════════════════════════════

    def _bloque_terminos(self, cotizacion_data: dict, estilos: dict) -> list:
        elements: list = []
        s = estilos
        notas = cotizacion_data.get('notas', '')
        if not notas:
            return elements

        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph('Términos y Condiciones:', s['terms_title']))
        for linea in notas.split('\n'):
            if linea.strip():
                elements.append(Paragraph(linea.strip(), s['terms_text']))

        return elements

    def _bloque_pie(self, empresa_data: dict, estilos: dict) -> list:
        elements: list = []
        s = estilos

        elements.append(Spacer(1, 0.3 * inch))
        elements.append(HRFlowable(
            width="100%", thickness=2, color=self.AZUL,
            spaceBefore=0, spaceAfter=6
        ))

        nombre = empresa_data.get('nombre', '')
        elements.append(Paragraph(nombre, s['footer']))
        elements.append(Paragraph("Quedo a sus ordenes", s['footer_sub']))
        elements.append(Paragraph("Saludos!", s['footer_sub']))

        return elements

    # ══════════════════════════════════════════════════════════
    #  MÉTODO PRINCIPAL
    # ══════════════════════════════════════════════════════════

    def generar_cotizacion(self, cotizacion_data: dict, empresa_data: dict) -> str:
        numero = cotizacion_data.get('numero_cotizacion', 'SIN-NUMERO')
        filename = f"{str(numero).replace('/', '-')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.35 * inch,
            leftMargin=0.35 * inch,
            topMargin=0.3 * inch,
            bottomMargin=0.3 * inch,
        )

        estilos = self._crear_estilos()
        elements: list = []

        # 1. Encabezado
        elements.extend(self._bloque_encabezado(empresa_data, cotizacion_data, estilos))

        # 2. Tabla de conceptos
        elements.extend(self._tabla_conceptos(cotizacion_data, estilos))

        # 3. Totales
        elements.extend(self._bloque_totales(cotizacion_data, estilos))

        # 4. Términos y condiciones
        elements.extend(self._bloque_terminos(cotizacion_data, estilos))

        # 5. Pie
        elements.extend(self._bloque_pie(empresa_data, estilos))

        doc.build(elements)
        return filepath
