# Copilot Instructions – Cotiz_AC

## Project Overview

Quotation management system for an AC installation company ("Multiservicios RMG"). Generates professional ProForma documents in PDF and Excel. Built with Flask + SQLite + vanilla JS frontend.

**Language**: All code comments, UI labels, database fields, and variable names are in **Spanish**. Keep this convention.

## Architecture

```
app.py                  # Flask app, all routes (pages + REST API)
src/models/models.py    # SQLAlchemy ORM models (Empresa, Cliente, Cotizacion, DetalleCotizacion)
src/controllers/        # Static-method controller classes (business logic, DB operations)
src/services/           # Export services: PDFService (ReportLab), ExcelService (openpyxl)
templates/              # Jinja2 templates (Bootstrap 5)
static/js/              # jQuery-based JS (one file per page)
static/css/style.css    # Custom styles
static/img/logormg.jpg  # Company logo (used in PDF/Excel exports)
instance/cotizaciones.db # SQLite database (auto-created)
exports/pdf/            # Generated PDF files
exports/excel/          # Generated Excel files
```

## Key Patterns

### Models (`src/models/models.py`)
- Use `db.Column()` for fields, `Mapped[...]` type hints for relationships.
- All models have `to_dict()` for JSON serialization.
- `Cotizacion.calcular_totales()` computes: NETO = subtotal − descuento; IVA = NETO × 0.16; total = NETO + IVA + envío.
- `DetalleCotizacion` has `grupo` field (city/section grouping, e.g. "Hermosillo", "Navojoa").
- When adding model attributes, use the attribute-assignment pattern (e.g., `obj.field = value`), not constructor kwargs.

### Controllers (`src/controllers/`)
- All methods are `@staticmethod` inside a class (e.g., `CotizacionController`).
- Return `(dict, http_status_code)` tuples. The dict contains either `{'success': True, 'cotizacion': ...}` or `{'error': 'message'}`.
- Database writes use `db.session.add()` / `db.session.commit()` with `try/except` + `db.session.rollback()`.
- Cotización numbering: `COT-00001` format via `generar_consecutivo()`.
- Detalles are replaced entirely on update (delete all, re-add).

### Services (`src/services/`)
- `ExcelService` and `PDFService` both have `generar_cotizacion(cotizacion_data: dict, empresa_data: dict)` as the main entry point.
- Both services mirror the same ProForma layout: logo, header, client info, 5-column table (IVA | CANT. | DESCRIPCIÓN | P. UNITARIO | TOTAL), group separators, totals block, terms, footer.
- Corporate colors: `#08568D` (blue), `#F3F3F3` (gray). Always use these.
- Excel uses active formulas (e.g., `=B{r}*D{r}` for TOTAL column). Do NOT hardcode computed values in formula cells.
- When modifying the PDF layout, apply the same change to the Excel layout and vice versa — they must stay in sync.

### Routes (`app.py`)
- Page routes render templates: `/`, `/nueva-cotizacion`, `/historial`, `/clientes`, `/configuracion`.
- REST API under `/api/`: cotizaciones, clientes, empresa. Standard CRUD verbs.
- Export endpoints: `/api/cotizaciones/<id>/export/pdf` and `/api/cotizaciones/<id>/export/excel`.
- Service calls use `# type: ignore` because `generar_cotizacion` receives dict data, not ORM objects.

### Frontend (`static/js/`)
- jQuery + Bootstrap 5. One JS file per page (`cotizacion.js`, `historial.js`, `clientes.js`, `configuracion.js`).
- API calls via `$.ajax()` or `$.get()` / `$.post()`.
- `cotizacion.js` handles dynamic rows with a `lineaContador` counter, per-line IVA calculation, grupo/city field, descuento, envío delivery.
- `main.js` has shared utilities (e.g., `cargarClientesSelect()`).

## Database

- SQLite at `instance/cotizaciones.db`. Initialize with `python init_db.py`.
- Single `Empresa` row (singleton pattern via `Empresa.query.first()`).
- `Cotizacion` → `DetalleCotizacion` is 1:N with cascade delete.
- Estatus values: `Borrador`, `Enviada`, `Aceptada`, `Cancelada`.

## Development

- **Python 3.8+**, virtual env at `venv/`.
- Dependencies in `requirements.txt`: Flask, Flask-SQLAlchemy, Flask-CORS, openpyxl, reportlab, Pillow, python-dotenv.
- Run: `flask run` or `python app.py` (port 5000).
- No test suite currently exists. If adding tests, use `pytest` and place them in a `tests/` directory.

## Coding Conventions

- Type hints on function signatures. Use `Dict[str, Any]`, `List[...]`, `Optional[...]` from `typing`.
- Docstrings on all classes and public methods (Spanish is acceptable).
- Use `# type: ignore` sparingly — only for known openpyxl/ReportLab dynamic attribute access.
- Controller methods should always return the `(result_dict, status_code)` tuple pattern.
- Keep `models.py` as a single file (all 4 models together).
- No ORMs other than Flask-SQLAlchemy.

## Common Tasks

| Task | How |
|------|-----|
| Add a model field | Add `db.Column()` in `models.py` → update `to_dict()` → update controller create/update → update relevant JS and template |
| Add an export field | Update both `excel_service.py` AND `pdf_service.py` — keep layouts in sync |
| New API endpoint | Add route in `app.py` → add controller method → follow `(dict, status)` return pattern |
| New page | Add route in `app.py` → create template extending `base.html` → add JS file in `static/js/` |
