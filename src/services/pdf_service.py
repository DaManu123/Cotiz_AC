import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


class PDFService:
    """Servicio para generación de PDFs de cotizaciones"""
    
    def __init__(self, output_dir='exports/pdf'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generar_cotizacion(self, cotizacion_data, empresa_data):
        """
        Genera un PDF de cotización profesional
        
        Args:
            cotizacion_data: dict con datos de cotización
            empresa_data: dict con datos de empresa
        
        Returns:
            str: ruta del archivo generado
        """
        # Nombre del archivo
        filename = f"{cotizacion_data['numero_cotizacion'].replace('/', '-')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear documento
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Contenedor de elementos
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        style_title = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=6,
            alignment=TA_CENTER
        )
        
        style_subtitle = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        style_heading = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=10
        )
        
        # === ENCABEZADO EMPRESA ===
        elements.append(Paragraph(empresa_data.get('nombre', 'EMPRESA'), style_title))
        
        info_empresa = []
        if empresa_data.get('direccion'):
            info_empresa.append(empresa_data['direccion'])
        if empresa_data.get('telefono'):
            info_empresa.append(f"Tel: {empresa_data['telefono']}")
        if empresa_data.get('email'):
            info_empresa.append(f"Email: {empresa_data['email']}")
        
        if info_empresa:
            elements.append(Paragraph(' | '.join(info_empresa), style_subtitle))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # === TÍTULO COTIZACIÓN ===
        elements.append(Paragraph('COTIZACIÓN', style_heading))
        elements.append(Spacer(1, 0.1*inch))
        
        # === INFO COTIZACIÓN Y CLIENTE ===
        info_data = [
            ['Cotización No:', cotizacion_data['numero_cotizacion'], 'Fecha:', cotizacion_data['fecha']],
            ['Cliente:', cotizacion_data['cliente']['nombre'], 'Teléfono:', cotizacion_data['cliente'].get('telefono', '')],
            ['Email:', cotizacion_data['cliente'].get('email', ''), 'Estatus:', cotizacion_data['estatus']]
        ]
        
        info_table = Table(info_data, colWidths=[1.2*inch, 2.8*inch, 1*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#34495E')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # === TABLA DE CONCEPTOS ===
        elements.append(Paragraph('Conceptos', style_heading))
        elements.append(Spacer(1, 0.1*inch))
        
        # Encabezados de la tabla
        table_data = [
            ['Cant.', 'Descripción', 'Precio Unit.', 'Total']
        ]
        
        # Agregar detalles
        for detalle in cotizacion_data['detalles']:
            table_data.append([
                f"{detalle['cantidad']:.2f}",
                detalle['descripcion'],
                f"${detalle['precio_unitario']:,.2f}",
                f"${detalle['total_linea']:,.2f}"
            ])
        
        # Crear tabla
        conceptos_table = Table(table_data, colWidths=[0.8*inch, 4*inch, 1.3*inch, 1.3*inch])
        conceptos_table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Cantidad centrada
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Precios alineados a derecha
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ECF0F1')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(conceptos_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # === TOTALES ===
        totales_data = [
            ['Subtotal:', f"${cotizacion_data['subtotal']:,.2f}"],
            ['IVA (16%):', f"${cotizacion_data['impuestos']:,.2f}"],
            ['TOTAL:', f"${cotizacion_data['total']:,.2f}"]
        ]
        
        totales_table = Table(totales_data, colWidths=[5.9*inch, 1.5*inch])
        totales_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 1), 10),
            ('FONTSIZE', (0, 2), (-1, 2), 12),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#27AE60')),
            ('LINEABOVE', (0, 2), (-1, 2), 1, colors.HexColor('#27AE60')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(totales_table)
        
        # === NOTAS ===
        if cotizacion_data.get('notas'):
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph('Notas:', style_heading))
            elements.append(Spacer(1, 0.05*inch))
            elements.append(Paragraph(cotizacion_data['notas'], styles['Normal']))
        
        # === PIE DE PÁGINA ===
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#95A5A6'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            f"Documento generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            footer_style
        ))
        
        # Construir PDF
        doc.build(elements)
        
        return filepath
