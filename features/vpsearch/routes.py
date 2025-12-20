
from flask import Blueprint, render_template, jsonify, request, abort, redirect, url_for
from sqlalchemy import func
from .models import Year, Brand, YearBrand, Model, Submodel
from .part_models import Windshield, Backglass, DoorWindow, NagsGlass
from database import db

vpsearch_bp = Blueprint("vpsearch_bp", __name__)

SUBMODEL_CHOICES = [
    "4 Door Sedan",
    "4 Door Utility",
    "2 Door Coupe",
    "Conventional Cab",
    "4 Door Hatchback",
    "4 Door Crew Cab",
    "2 Door Convertible",
    "Cabover",
    "2 Door Standard Cab",
    "4 Door Station Wagon",
    "2 Door Extended Cab",
    "2 Door Hatchback",
    "Mini Van",
    "Van",
    "2 Door Conventional Cab",
    "4 Door Conventional Cab",
    "2 Door Super Cab",
    "Extended Conventional Cab",
    "4 Door Cabover",
    "4 Door Extended Cab",
    "4 Door Coupe",
    "Extended Van",
    "Step Van",
    "2 Door Utility",
    "4 Door Extended Crew Cab",
    "Cargo Van",
    "Cab Over Engine",
    "2 Door Pickup",
    "Bus",
    "4 Door Quad Cab",
    "Cab Forward",
    "Extended Cargo Van",
    "2 Door Club Cab",
    "Cutaway Van",
    "Cabover/Cargo Truck",
    "3 Door Hatchback",
    'Cargo Van 66.7"" WB',
    "Cargo Van Wide",
    "4 Door Super Cab",
    "3 Door Van",
    "4D Gran Coupe",
    "2 Door Hardtop",
    "2 Door Sedan",
    "2 Door Panel Wagon",
    "Extended Cabover",
]


@vpsearch_bp.route("/")
def index():
    years = db.session.query(Year).order_by(Year.year.desc()).all()
    print(f"Years found: {years}")
    return render_template("index.html", years=years)

@vpsearch_bp.route("/vehicles", methods=("GET", "POST"))
def vehicles_page():
    year_rows = (
        db.session.query(Year.id.label("id"), Year.year.label("year"))
        .order_by(Year.year.desc())
        .all()
    )
    brand_rows = (
        db.session.query(
            Brand.id.label("id"),
            Brand.brand_name.label("name"),
            Brand.is_truck.label("is_truck"),
            Brand.is_active.label("is_active"),
        )
        .order_by(Brand.brand_name)
        .all()
    )
    year_brand_records = (
        db.session.query(
            YearBrand.id.label("id"),
            Year.id.label("year_id"),
            Year.year.label("year"),
            Brand.id.label("brand_id"),
            Brand.brand_name.label("brand_name"),
            func.count(Model.id).label("model_count"),
        )
        .join(Year, YearBrand.year_id == Year.id)
        .join(Brand, YearBrand.brand_id == Brand.id)
        .outerjoin(Model, Model.year_brand_id == YearBrand.id)
        .group_by(YearBrand.id, Year.id, Year.year, Brand.id, Brand.brand_name)
        .order_by(Year.year.desc(), Brand.brand_name)
        .all()
    )

    year_options = [{"id": row.id, "year": row.year} for row in year_rows]
    brand_options = [
        {"id": row.id, "name": row.name, "is_truck": row.is_truck, "is_active": row.is_active}
        for row in brand_rows
    ]
    if request.method == "POST":
        year_id = request.form.get("year_id")
        submitted_list = request.form.get("selected_brand_ids")
        if submitted_list:
            brand_ids = [value for value in submitted_list.split(",") if value]
        else:
            brand_ids = [value for value in request.form.getlist("brand_ids") if value]
        if not year_id or not brand_ids:
            abort(400)
        try:
            year_id_value = int(year_id)
        except ValueError:
            abort(400)
        brand_ids_int = []
        for value in brand_ids:
            try:
                brand_ids_int.append(int(value))
            except ValueError:
                abort(400)
        existing_brands = {
            brand_id
            for (brand_id,) in db.session.query(YearBrand.brand_id)
            .filter(
                YearBrand.year_id == year_id_value,
                YearBrand.brand_id.in_(brand_ids_int),
            )
            .all()
        }
        additions = []
        for brand_id in brand_ids_int:
            if brand_id in existing_brands:
                continue
            additions.append(YearBrand(year_id=year_id_value, brand_id=brand_id))
            existing_brands.add(brand_id)
        if additions:
            db.session.add_all(additions)
            db.session.commit()
        return redirect(url_for("vpsearch_bp.vehicles_page"))

    year_brand_mappings = [
        {
            "id": row.id,
            "year_id": row.year_id,
            "year": row.year,
            "brand_id": row.brand_id,
            "brand_name": row.brand_name,
            "model_count": row.model_count,
        }
        for row in year_brand_records
    ]

    return render_template(
        "vehicles.html",
        years=year_options,
        brands=brand_options,
        year_brand_mappings=year_brand_mappings,
    )


@vpsearch_bp.route("/vehicles/models/<int:year_brand_id>", methods=("GET", "POST"))
def vehicle_models(year_brand_id):
    record = (
        db.session.query(YearBrand, Year, Brand)
        .join(Year, YearBrand.year_id == Year.id)
        .join(Brand, YearBrand.brand_id == Brand.id)
        .filter(YearBrand.id == year_brand_id)
        .first()
    )
    if not record:
        abort(404)

    year_brand_row, year_row, brand_row = record
    if request.method == "POST":
        model_name = request.form.get("model_name", "").strip()
        if not model_name:
            abort(400)
        new_model = Model(year_brand_id=year_brand_id, model_name=model_name)
        db.session.add(new_model)
        db.session.commit()
        return redirect(url_for("vpsearch_bp.vehicle_models", year_brand_id=year_brand_id))

    model_rows = (
        db.session.query(
            Model.id.label("id"),
            Model.model_name.label("model_name"),
            func.count(Submodel.id).label("submodel_count"),
        )
        .outerjoin(Submodel, Submodel.model_id == Model.id)
        .filter(Model.year_brand_id == year_brand_id)
        .group_by(Model.id, Model.model_name)
        .order_by(Model.model_name)
        .all()
    )

    models_data = [
        {
            "id": row.id,
            "name": row.model_name,
            "submodel_count": row.submodel_count,
            "submodel_url": url_for("vpsearch_bp.model_submodels", model_id=row.id),
        }
        for row in model_rows
    ]
    mapping_context = {
        "id": year_brand_row.id,
        "year": year_row.year,
        "brand": brand_row.brand_name,
    }

    return render_template(
        "vehicles_models.html",
        year_brand=mapping_context,
        models=models_data,
    )


@vpsearch_bp.route("/vehicles/models/<int:model_id>/submodels", methods=("GET", "POST"))
def model_submodels(model_id):
    model = db.session.query(Model).filter_by(id=model_id).first()
    if not model:
        abort(404)

    year_brand = model.year_brand
    if not year_brand:
        abort(404)

    if request.method == "POST":
        selected = [value.strip() for value in request.form.getlist("submodels") if value.strip()]
        existing_names = {row.submodel_name for row in model.submodels}
        additions = [
            Submodel(model_id=model_id, submodel_name=value, vehicle_id=value)
            for value in selected
            if value not in existing_names
        ]
        if additions:
            db.session.add_all(additions)
            db.session.commit()
        return redirect(url_for("vpsearch_bp.model_submodels", model_id=model_id))

    year = year_brand.year
    brand = year_brand.brand
    submodel_records = (
        db.session.query(
            Submodel.id.label("id"),
            Submodel.submodel_name.label("name"),
            Submodel.vehicle_id.label("vehicle_id"),
        )
        .filter_by(model_id=model_id)
        .order_by(Submodel.submodel_name)
        .all()
    )

    submodel_ids = [row.id for row in submodel_records]
    part_counts = {sid: 0 for sid in submodel_ids}
    if submodel_ids:
        for cls in (Windshield, Backglass, DoorWindow):
            counts = (
                db.session.query(cls.bodystyle_id, func.count(cls.nags_glass_id).label("count"))
                .filter(cls.bodystyle_id.in_(submodel_ids))
                .group_by(cls.bodystyle_id)
                .all()
            )
            for bodystyle_id, count in counts:
                part_counts[bodystyle_id] = part_counts.get(bodystyle_id, 0) + count

    submodel_rows = [
        {
            "id": row.id,
            "name": row.name,
            "vehicle_id": row.vehicle_id,
            "part_count": part_counts.get(row.id, 0),
        }
        for row in submodel_records
    ]

    return render_template(
        "vehicles_submodels.html",
        model={
            "id": model.id,
            "name": model.model_name,
            "year_brand_id": year_brand.id,
            "year": year.year,
            "brand": brand.brand_name,
        },
        submodels=submodel_rows,
        submodel_choices=SUBMODEL_CHOICES,
    )


@vpsearch_bp.route("/vehicles/submodels/<int:submodel_id>/parts", methods=("GET", "POST"))
def submodel_parts(submodel_id):
    submodel = db.session.query(Submodel).filter_by(id=submodel_id).first()
    if not submodel:
        abort(404)

    if request.method == "POST":
        created_any = False

        def _strip_field(*field_names):
            for name in field_names:
                value = request.form.get(name)
                if value:
                    return value.strip()
            return None

        def _validate_bodystyle():
            field_value = request.form.get("bodystyle_id")
            if not field_value:
                return submodel_id
            try:
                resolved = int(field_value)
            except ValueError:
                abort(400)
            if resolved != submodel_id:
                abort(400)
            return submodel_id

        def _should_handle(kind):
            if glass_type:
                return glass_type == kind
            if kind == "windshield":
                return bool(
                    request.form.get("windshield_part")
                    or request.form.get("windshield_desc")
                    or request.form.get("windshield_side")
                )
            if kind == "backglass":
                return bool(
                    request.form.get("backglass_part")
                    or request.form.get("backglass_desc")
                    or request.form.get("backglass_side")
                )
            if kind == "door_window":
                return bool(
                    request.form.get("door_window_part")
                    or request.form.get("door_window_desc")
                    or request.form.get("door_window_side")
                    or request.form.get("door_window_position")
                )
            return False

        glass_type = request.form.get("glass_type")
        _validate_bodystyle()

        if _should_handle("windshield"):
            windshield_part = _strip_field("nags_part_id", "windshield_part")
            if windshield_part:
                part_side = _strip_field("part_side", "windshield_side")
                exists = (
                    db.session.query(Windshield)
                    .filter_by(
                        bodystyle_id=submodel_id,
                        nags_glass_id=windshield_part,
                        part_side=part_side,
                    )
                    .first()
                )
                if not exists:
                    db.session.add(Windshield(
                        bodystyle_id=submodel_id,
                        nags_glass_id=windshield_part,
                        part_side=part_side,
                    ))
                    created_any = True

        if _should_handle("backglass"):
            backglass_part = _strip_field("nags_part_id", "backglass_part")
            if backglass_part:
                part_side = _strip_field("part_side", "backglass_side")
                exists = (
                    db.session.query(Backglass)
                    .filter_by(
                        bodystyle_id=submodel_id,
                        nags_glass_id=backglass_part,
                        part_side=part_side,
                    )
                    .first()
                )
                if not exists:
                    db.session.add(Backglass(
                        bodystyle_id=submodel_id,
                        nags_glass_id=backglass_part,
                        part_side=part_side,
                    ))
                    created_any = True

        if _should_handle("door_window"):
            door_part = _strip_field("nags_part_id", "door_window_part")
            if door_part:
                part_side = _strip_field("part_side", "door_window_side")
                part_posi = _strip_field("position_id", "door_window_position")
                exists = (
                    db.session.query(DoorWindow)
                    .filter_by(
                        bodystyle_id=submodel_id,
                        nags_glass_id=door_part,
                        part_side=part_side,
                        part_posi=part_posi,
                    )
                    .first()
                )
                if not exists:
                    db.session.add(DoorWindow(
                        bodystyle_id=submodel_id,
                        nags_glass_id=door_part,
                        part_side=part_side,
                        part_posi=part_posi,
                    ))
                    created_any = True

        if created_any:
            db.session.commit()
        return redirect(url_for("vpsearch_bp.submodel_parts", submodel_id=submodel_id))

    windshield_records = (
        db.session.query(Windshield, NagsGlass)
        .join(NagsGlass, Windshield.nags_glass_id == NagsGlass.id)
        .filter(Windshield.bodystyle_id == submodel_id)
        .all()
    )
    backglass_records = (
        db.session.query(Backglass, NagsGlass)
        .join(NagsGlass, Backglass.nags_glass_id == NagsGlass.id)
        .filter(Backglass.bodystyle_id == submodel_id)
        .all()
    )
    door_window_records = (
        db.session.query(DoorWindow, NagsGlass)
        .join(NagsGlass, DoorWindow.nags_glass_id == NagsGlass.id)
        .filter(DoorWindow.bodystyle_id == submodel_id)
        .all()
    )

    windshield_rows = [
        {
            "nags_id": glass.id,
            "description": glass.description,
            "adas": glass.adas,
        }
        for wind, glass in windshield_records
    ]
    backglass_rows = [
        {
            "nags_id": glass.id,
            "description": glass.description,
        }
        for part, glass in backglass_records
    ]
    door_window_rows = [
        {
            "nags_id": glass.id,
            "description": glass.description,
            "side": part.part_side,
            "position": part.part_posi,
        }
        for part, glass in door_window_records
    ]

    return render_template(
        "vehicles_submodel_parts.html",
        submodel={
            "id": submodel.id,
            "name": submodel.submodel_name,
            "vehicle_id": submodel.vehicle_id,
        },
        model_id=submodel.model_id,
        windshields=windshield_rows,
        backglass=backglass_rows,
        door_windows=door_window_rows,
    )

@vpsearch_bp.route("/api/brands/<int:year_id>")
def get_brands(year_id):
    brands = (
        db.session.query(Brand.id, Brand.brand_name)
        .join(YearBrand, YearBrand.brand_id == Brand.id)
        .filter(YearBrand.year_id == year_id)
        .all()
    )
    return jsonify([{"id": b.id, "name": b.brand_name} for b in brands])

@vpsearch_bp.route("/api/models/<int:year_id>/<int:brand_id>")
def get_models(year_id, brand_id):
    yb = (
        db.session.query(YearBrand)
        .filter_by(year_id=year_id, brand_id=brand_id)
        .first()
    )
    if not yb:
        return jsonify([])

    models = (
        db.session.query(Model.id, Model.model_name)
        .filter_by(year_brand_id=yb.id)
        .all()
    )
    return jsonify([{"id": m.id, "name": m.model_name} for m in models])

@vpsearch_bp.route("/api/submodels/<int:model_id>")
def get_submodels(model_id):
    submodels = (
        db.session.query(Submodel.id, Submodel.submodel_name)
        .filter_by(model_id=model_id)
        .all()
    )
    return jsonify([{"id": s.id, "name": s.submodel_name} for s in submodels])

@vpsearch_bp.route("/api/glass/<int:submodel_id>")
def get_glass_parts(submodel_id):
    from .part_models import NagsGlass

    def serialize_part(part):
        glass = part.nags_glass
        return {
            "nags_id": glass.id,
            "description": glass.description,
            "glass_type": glass.glass_type,
            "adas": glass.adas,
            "price": str(glass.price),
            "side": getattr(part, "part_side", None),
            "position": getattr(part, "part_posi", None)
        }

    windshields = db.session.query(Windshield).filter_by(bodystyle_id=submodel_id).all()
    backglass = db.session.query(Backglass).filter_by(bodystyle_id=submodel_id).all()
    door_windows = db.session.query(DoorWindow).filter_by(bodystyle_id=submodel_id).all()

    return jsonify({
        "windshields": [serialize_part(p) for p in windshields],
        "backglass": [serialize_part(p) for p in backglass],
        "door_windows": [serialize_part(p) for p in door_windows],
    })
@vpsearch_bp.route("/brands")
def brands_partial():
    year_id = request.args.get("year", type=int)
    brands = []
    if year_id:
        brands = (
            db.session.query(Brand.id, Brand.brand_name)
            .join(YearBrand, YearBrand.brand_id == Brand.id)
            .filter(YearBrand.year_id == year_id)
            .all()
        )
    return render_template("vpsearch/_brand_select.html", brands=brands)

@vpsearch_bp.route("/models")
def models_partial():
    year_id = request.args.get("year", type=int)
    brand_id = request.args.get("brand", type=int)
    models = []
    if year_id and brand_id:
        yb = (
            db.session.query(YearBrand)
            .filter_by(year_id=year_id, brand_id=brand_id)
            .first()
        )
        if yb:
            models = (
                db.session.query(Model.id, Model.model_name)
                .filter_by(year_brand_id=yb.id)
                .all()
            )
    return render_template("vpsearch/_model_select.html", models=models)

@vpsearch_bp.route("/submodels")
def submodels_partial():
    model_id = request.args.get("model", type=int)
    submodels = []
    if model_id:
        submodels = (
            db.session.query(Submodel.id, Submodel.submodel_name)
            .filter_by(model_id=model_id)
            .all()
        )
    return render_template("vpsearch/_submodel_select.html", submodels=submodels)

@vpsearch_bp.route("/glass_tables")
def glass_tables_partial():
    submodel_id = request.args.get("submodel", type=int)
    selected_part = request.args.get("selected_part", type=str)
    print(f"Submodel ID: {submodel_id}, Selected Part: {selected_part}")

    from .part_models import Windshield, Backglass, DoorWindow

    def serialize_part(part):
        glass = part.nags_glass
        return {
            "nags_id": glass.id,
            "description": glass.description,
            "glass_type": glass.glass_type,
            "adas": glass.adas,
            "price": str(glass.price),
            "side": getattr(part, "part_side", None),
            "position": getattr(part, "part_posi", None)
        }

    windshields = []
    backglass = []
    door_windows = []

    if submodel_id and selected_part:
        if selected_part == "ws":
            windshields = db.session.query(Windshield).filter_by(bodystyle_id=submodel_id).all()
        elif selected_part == "bg":
            backglass = db.session.query(Backglass).filter_by(bodystyle_id=submodel_id).all()
        elif selected_part in {"wrr", "wrl", "wfr", "wfl"}:
            pos_map = {"wrr": ("R", "R"), "wrl": ("R", "L"), "wfr": ("F", "R"), "wfl": ("F", "L")}
            part_posi, part_side = pos_map[selected_part]
            door_windows = db.session.query(DoorWindow).filter_by(
                bodystyle_id=submodel_id,
                part_posi=part_posi,
                part_side=part_side
            ).all()
        else:
            # Unhandled part types like 'rf' (roof) or invalid input
            return render_template("vpsearch/_glass_tables.html",
                                   windshields=[], backglass=[], door_windows=[])
    else:
        # If no part selected, default to showing all glass types
        # windshields = db.session.query(Windshield).filter_by(bodystyle_id=submodel_id).all()
        # backglass = db.session.query(Backglass).filter_by(bodystyle_id=submodel_id).all()
        # door_windows = db.session.query(DoorWindow).filter_by(bodystyle_id=submodel_id).all()
        pass

    return render_template("vpsearch/_glass_tables.html",
                           windshields=[serialize_part(p) for p in windshields],
                           backglass=[serialize_part(p) for p in backglass],
                           door_windows=[serialize_part(p) for p in door_windows])

# --- ZIP Autocomplete Endpoint ---
@vpsearch_bp.route('/vpsearch/zip_autocomplete')
def zip_autocomplete():
    from sqlalchemy import text
    query = request.args.get('zip', '').strip()
    if not query or len(query) < 2:
        return ''
    sql = text('SELECT DISTINCT zip_code FROM supplier_zip_distances WHERE zip_code LIKE :q LIMIT 10')
    # Use the main db engine if it is already connected to agprodb
    try:
        rows = db.session.execute(sql, {'q': f'{query}%'}).fetchall()
    except Exception:
        # If db.session is not agprodb, you must configure a separate engine:
        # from sqlalchemy import create_engine
        # engine = create_engine('mysql+pymysql://user:password@localhost/agprodb')
        # with engine.connect() as conn:
        #     rows = conn.execute(sql, {'q': f'{query}%'}).fetchall()
        rows = []
    items = ''
    for row in rows:
        zip_val = row[0]
        btn_html = (
            f'<button type="button" class="list-group-item list-group-item-action" '
            f'onclick="document.getElementById(\'zip\').value=\'{zip_val}\';'
            f'document.getElementById(\'zip-suggestions\').innerHTML=\'\';">'
            f'{zip_val}</button>'
        )
        items += btn_html
    if not items:
        items = '<div class="list-group-item">No matches</div>'
    return items
# @vpsearch_bp.route("/glass_tables")
# def glass_tables_partial():
#     submodel_id = request.args.get("submodel", type=int)
#     selected_part = request.args.get("selected_part", type=str)
#     from .part_models import Windshield, Backglass, DoorWindow, NagsGlass
#     def serialize_part(part):
#         glass = part.nags_glass
#         return {
#             "nags_id": glass.id,
#             "description": glass.description,
#             "glass_type": glass.glass_type,
#             "adas": glass.adas,
#             "price": str(glass.price),
#             "side": getattr(part, "part_side", None),
#             "position": getattr(part, "part_posi", None)
#         }
#     windshields = []
#     backglass = []
#     door_windows = []
#     # Logic for part selection
#     if submodel_id and selected_part:
#         if selected_part == "ws":
#             windshields = db.session.query(Windshield).filter_by(bodystyle_id=submodel_id).all()
#         elif selected_part == "bg":
#             backglass = db.session.query(Backglass).filter_by(bodystyle_id=submodel_id).all()
#         elif selected_part in ["wrr", "wrl", "wfr", "wfl"]:
#             pos_map = {"wrr": ("R", "R"), "wrl": ("R", "L"), "wfr": ("F", "R"), "wfl": ("F", "L")}
#             part_posi, part_side = pos_map[selected_part]
#             door_windows = db.session.query(DoorWindow).filter_by(bodystyle_id=submodel_id, part_posi=part_posi, part_side=part_side).all()
#         # rf (roof) and others: return empty or handle as needed
#     elif submodel_id:
#         windshields = db.session.query(Windshield).filter_by(bodystyle_id=submodel_id).all()
#         backglass = db.session.query(Backglass).filter_by(bodystyle_id=submodel_id).all()
#         door_windows = db.session.query(DoorWindow).filter_by(bodystyle_id=submodel_id).all()
#     return render_template(
#         "vpsearch/_glass_tables.html",
#         windshields=[serialize_part(p) for p in windshields],
#         backglass=[serialize_part(p) for p in backglass],
#         door_windows=[serialize_part(p) for p in door_windows],
#     )




