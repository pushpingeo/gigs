"""Read the EPSG registry as PROJ carries it (proj.db), and apply named operations.

Used by the packet builder and the grader. The agent under test never sees this code's
output: expected answers are worked out only at grading time.
"""
import os
import sqlite3
import warnings
from functools import lru_cache

import pyproj
from pyproj.transformer import AreaOfInterest, TransformerGroup

warnings.filterwarnings("ignore", category=UserWarning, module="pyproj")

TRANSFORMATION_TABLES = (
    "helmert_transformation_table",
    "grid_transformation",
    "other_transformation",
    "concatenated_operation",
)


@lru_cache(maxsize=1)
def db():
    return sqlite3.connect(os.path.join(pyproj.datadir.get_data_dir(), "proj.db"))


def epsg_version():
    row = db().execute("select value from metadata where key='EPSG.VERSION'").fetchone()
    date = db().execute("select value from metadata where key='EPSG.DATE'").fetchone()
    return f"{row[0]} ({date[0]})"


def engine_version():
    return f"pyproj {pyproj.__version__} / PROJ {pyproj.proj_version_str}"


def code_of(text):
    """'EPSG:1314', 'epsg 1314', 1314 -> '1314'."""
    if text is None:
        return None
    s = str(text).strip().upper().replace("EPSG", "").replace("::", ":").lstrip(":").strip()
    return s or None


def bbox(code, table=None):
    """Area-of-use bounding box (west, south, east, north) of an EPSG object."""
    q = (
        "select e.west_lon, e.south_lat, e.east_lon, e.north_lat, u.object_table_name "
        "from usage u join extent e on e.auth_name = u.extent_auth_name and e.code = u.extent_code "
        "where u.object_auth_name = 'EPSG' and u.object_code = ?"
    )
    rows = db().execute(q, (str(code),)).fetchall()
    if table:
        rows = [r for r in rows if r[4] == table]
    else:
        rows = [r for r in rows if r[4] != "geodetic_datum"]
    return tuple(rows[0][:4]) if rows else None


def inside(b, lon, lat):
    w, s, e, n = b
    if w <= e:
        return s <= lat <= n and w <= lon <= e
    return s <= lat <= n and (lon >= w or lon <= e)  # crosses the antimeridian


def is_transformation_code(code):
    for t in TRANSFORMATION_TABLES:
        if db().execute(f"select 1 from {t} where auth_name='EPSG' and code=?", (str(code),)).fetchone():
            return True
    return False


def transformation_codes(op):
    """EPSG codes of the datum transformations inside a PROJ operation (conversions and axis swaps dropped)."""
    d = op.to_json_dict()
    steps = d.get("steps") or [d]
    out = []
    for st in steps:
        i = st.get("id") or {}
        if i.get("code") is not None and is_transformation_code(i["code"]):
            out.append(str(i["code"]))
    return out


def candidates(src, tgt, area):
    """Operations from src to tgt whose area of use contains `area` (w, s, e, n), as PROJ ranks them.

    Returns dicts: code(s), name, accuracy, available (grid present), transformer (or None).
    """
    g = TransformerGroup(src, tgt, always_xy=True, area_of_interest=AreaOfInterest(*area))
    out = []
    for t in g.transformers:
        out.append({"codes": transformation_codes(t), "name": t.description, "accuracy": t.accuracy if t.accuracy >= 0 else None,
                    "available": True, "transformer": t})
    for o in g.unavailable_operations:
        out.append({"codes": transformation_codes(o), "name": o.name, "accuracy": o.accuracy if o.accuracy >= 0 else None,
                    "available": False, "transformer": None})
    # Drop ballpark (no datum shift) and operations without an EPSG transformation, unless src and tgt share a datum.
    return [c for c in out if c["codes"] or "ballpark" not in (c["name"] or "").lower()]


def needs_grid(codes):
    return any(db().execute("select 1 from grid_transformation where auth_name='EPSG' and code=?", (c,)).fetchone()
               for c in codes)


def best(cands):
    """The acceptable choices. Returns (best_available, acceptable).

    Acceptable: the best stated accuracy among the operations that apply here, or, since grid files may not be
    available wherever the agent runs, the best among those that need no grid. best_available is the best one this
    machine can apply.
    """
    with_acc = [c for c in cands if c["accuracy"] is not None and c["codes"]]
    if not with_acc:
        return None, []
    top = min(c["accuracy"] for c in with_acc)
    top_nogrid = min((c["accuracy"] for c in with_acc if not needs_grid(c["codes"])), default=None)
    acceptable = [c for c in with_acc
                  if c["accuracy"] == top or (not needs_grid(c["codes"]) and c["accuracy"] == top_nogrid)]
    best_avail = min((c for c in with_acc if c["available"]), key=lambda c: c["accuracy"], default=None)
    return best_avail, acceptable


def deprecated_crs_with_replacement():
    q = ("select d.table_name, d.deprecated_code, group_concat(d.replacement_code) from deprecation d "
         "where d.deprecated_auth_name='EPSG' and d.replacement_auth_name='EPSG' "
         "and d.table_name in ('geodetic_crs','projected_crs') group by d.table_name, d.deprecated_code")
    return [(t, str(c), sorted(set(r.split(",")))) for t, c, r in db().execute(q).fetchall()]


def object_record(code):
    """(table, name, deprecated) for a CRS code, or None."""
    for t in ("geodetic_crs", "projected_crs", "vertical_crs", "compound_crs"):
        r = db().execute(f"select name, deprecated from {t} where auth_name='EPSG' and code=?", (str(code),)).fetchone()
        if r:
            return t, r[0], bool(r[1])
    return None


def replacements(code):
    rows = db().execute("select replacement_code from deprecation where deprecated_auth_name='EPSG' and deprecated_code=?",
                        (str(code),)).fetchall()
    return sorted({str(r[0]) for r in rows})


def live_crs(table, area=None):
    q = f"select code, name from {table} where auth_name='EPSG' and deprecated=0"
    rows = db().execute(q).fetchall()
    return [(str(c), n) for c, n in rows]
