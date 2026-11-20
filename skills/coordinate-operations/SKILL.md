---
name: coordinate-operations
version: 0.1-draft
description: Compute coordinates correctly. Use with coordinate-reference whenever coordinates must actually be converted or transformed, so the numbers come from a tested engine applying the operation you chose, never from mental arithmetic or a library's silent default.
---

# Coordinate operations

`coordinate-reference` says what to decide: which CRS, which operation, what to record. This skill says how to get
the numbers. The rule is short:

**You choose the operation; a tested engine applies it; you check what it applied.**

An agent should never compute coordinates itself, in its head or in hand-written formulas it hasn't tested. The
arithmetic of a Position Vector transformation or a Transverse Mercator projection is easy to get almost right, and
almost right is metres wrong.

There are two routes to an engine. Take the first unless you have a reason not to.

## Route A: use an open-source library (recommended)
**PROJ** is the reference open-source engine, with a copy of the EPSG registry built in (`proj.db`). Reach it through
pyproj (Python), GDAL/OGR, PostGIS or QGIS. Other options: Apache SIS (Java, follows ISO 19111 closely);
proj4js (JavaScript) applies a single `+towgs84` shift per CRS and knows nothing of areas of use or alternative
operations, so with proj4js you must choose the operation yourself and supply its parameters from the registry.

### The method, with pyproj
```python
from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.transformer import TransformerGroup
from pyproj.database import get_database_metadata

src, tgt = CRS.from_epsg(4277), CRS.from_epsg(4326)          # 1. name both CRSs by code
assert not src.is_deprecated and not tgt.is_deprecated        #    deprecated codes still resolve: check
# 2. list the operations whose area of use contains your points (west, south, east, north)
group = TransformerGroup(src, tgt, always_xy=True,
                         area_of_interest=AreaOfInterest(-4.3, 55.8, -3.2, 56.1))
for t in group.transformers:                                  # can be applied here, PROJ's ranking
    print(t.description, t.accuracy)
for op in group.unavailable_operations:                       # better ones whose grid file is missing
    print("not available:", op.name, op.accuracy)
# 3. choose by the rules in coordinate-reference (area, not deprecated, accuracy), then apply exactly that one
chosen = next(t for t in group.transformers if "OSGB36 to WGS 84 (6)" in t.description)
lon, lat = chosen.transform(-3.6, 55.97)                      # always_xy: longitude first, in and out
# 4. round trip and record
back = next(t for t in TransformerGroup(tgt, src, always_xy=True).transformers
            if "OSGB36 to WGS 84 (6)" in t.description)               # the same operation, reversed
print(back.transform(lon, lat))                               # should return (-3.6, 55.97)
print(get_database_metadata("EPSG.VERSION"))                  # e.g. v12.029: record it
```
The EPSG code of the transformation inside a PROJ pipeline is in `t.to_json_dict()["steps"][i]["id"]`. Skip the steps
that are conversions (a map projection) or axis swaps (EPSG:15498).

### What libraries do that you must check
- **The default picks for you, per point.** `Transformer.from_crs(src, tgt)` chooses an operation each time it
  transforms, and doesn't say which until afterwards (`get_last_used_operation()`). It may not be the one you would
  choose: for ED50 to WGS 84 in the UK North Sea, PROJ 9.8.1's default applies EPSG:1138 (stated 6 m), about 1.3 m
  from EPSG:1311 (stated 1 m). List the options and apply the one you chose.
- **Ballpark fallbacks.** With no known operation between two datums, PROJ returns a "Ballpark geographic offset":
  no datum shift at all, wrong by up to hundreds of metres, with no error. Reject any operation whose name contains
  "Ballpark" unless both CRSs share a datum.
- **Missing grids.** Grid-based operations (OSTN15, NTv2, NADCON) need grid files. Without them PROJ quietly uses the
  next option. Enable the CDN (`pyproj.network.set_network_enabled(True)` or `PROJ_NETWORK=ON`) or install the grids
  (`projsync`), and record whether the grid operation was applied.
- **Axis order.** EPSG:4326 is latitude first; most software and GeoJSON are longitude first. Set `always_xy=True`
  (or the library's equivalent) and be explicit in what you write out.
- **Areas of use are bounding boxes** in `proj.db`. The live registry also has outlines; where boxes overlap, check
  the outline (EPSG API `Extent/{code}/polygon`).
- **The library's EPSG copy has a version.** It may be behind the live registry. Record it; check anything critical
  at epsg.org.

## Route B: build your own engine
Only if you need to (no library fits your platform, or you're writing one). Then:
1. Implement the methods from the registry's own formulas: IOGP Guidance Note 7-2, *Coordinate Conversions and
   Transformations including Formulas*. Take parameters from the registry by code, never from memory.
2. Prove each method against the GIGS test dataset (series 5100 conversions, 5200 transformations: forward, reverse
   and round trip) within its stated tolerances, before you use it. Record the GIGS version you passed.
3. From then on, treat it like a library: choose the operation, apply it, check, record.

## Checks after every computation
- **Round trip** a sample: forward then reverse should return the input within GIGS round-trip tolerance (0.006 m;
  0.00000006°).
- **Plausibility:** the shift between datums should be the size you expect (OSGB36 to WGS 84: 70–125 m; ED50 to
  WGS 84 in the North Sea: 110–125 m). Zero means nothing was applied; kilometres mean a wrong operation or swapped
  axes.
- **Area:** every input point lies inside the area of use of the source CRS and of the operation. Flag those that
  don't (see `coordinate-reference`, section 5).

## The operations an agent needs
Whatever the engine, an agent doing coordinate work needs these, as tools or as code it can run:

| Operation | Does | Returns |
|---|---|---|
| read coordinates | Parses decimal degrees, DMS, grid references, eastings/northings | position, form, axis order, datum (stated or assumed), precision, any other reading |
| look up a CRS | Finds a CRS by code or name in the registry | kind, datum, ellipsoid, axes, area of use, deprecated and replacement, WKT2 |
| list transformations | For source, target and site: the operations whose area contains the site, deprecated ones dropped, ranked | each with code, name, method, accuracy, area, whether it can be applied |
| transform | Applies a **named** operation | coordinates, the operation applied, its accuracy |
| measure | Lengths geodesically; areas in an equal-area projection centred on the area | values, with the method recorded |

## Record
With every result: the engine and its version (`pyproj 3.8.0 / PROJ 9.8.1`), the EPSG dataset version, the operation
applied (code, name, stated accuracy), and whether the round trip passed.
