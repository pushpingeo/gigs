# Coordinate tasks: instructions

You are being tested on coordinate reference work: reading what system coordinates are in, choosing the right
operation to move them to another system, applying it, and recording what you did. The tests are modelled on the
IOGP GIGS test series (Geospatial Integrity of Geoscience Software).

{skills}

## What to do
1. Work only inside this folder. Don't look for answers elsewhere: there are none to find. The points and codes were
   drawn at random for this run, and the expected answers are worked out only after you finish.
2. Do each task in `tasks/`. Each file has a `task` in plain words and either `points` or `codes`.
3. Use tools for the arithmetic: a coordinate library (such as PROJ / pyproj) or code you have written and tested.
   Never work coordinates out by hand.
4. Write one answer file per task to `answers/<test_id>.json`, in the format below. Valid JSON only.
5. When you have answered every task, stop. Say briefly what you did and anything you were unsure about.

## Answer format: `transformation`
```json
{
  "test_id": "tfm-example",
  "source_crs": "EPSG:4277",
  "target_crs": "EPSG:4326",
  "operation": {"code": "EPSG:1314", "name": "OSGB36 to WGS 84 (6)", "accuracy_m": 2,
                "why": "one line: why this operation"},
  "computed_by": "library",
  "computed_with": "pyproj 3.8.0 / PROJ 9.8.1",
  "epsg_version": "v12.029",
  "results": [{"id": "P01", "lat": 55.1234567, "lon": -3.1234567}],
  "outside_area_of_use": ["P07"],
  "round_trip": [{"id": "P01", "lat": 55.1234567, "lon": -3.1234567}],
  "assumptions": "anything you assumed",
  "notes": "anything else"
}
```
- `source_crs`, `target_crs`: EPSG codes (`EPSG:nnnn`; `OGC:CRS84` is accepted for WGS 84 longitude-latitude).
- `operation.code`: the EPSG code of the datum **transformation** you applied (not a map projection or an axis swap).
- `computed_by`: `library`, `own_code` or `by_hand`.
- `results`: target coordinates. Geographic as `lat`/`lon` in decimal degrees (at least 8 decimal places); projected
  as `easting`/`northing` in metres. For a point you decide not to transform, give `null` for its values.
- `outside_area_of_use`: ids of points outside the area of use of the source CRS or of the operation. `[]` if none.
- `round_trip`: only when the task asks for it: your results transformed back to the source CRS.

## Answer format: `deprecation`
```json
{
  "test_id": "dep-example",
  "epsg_version": "v12.029",
  "codes": [{"code": "EPSG:4291", "deprecated": true, "replacement": ["EPSG:4618"], "reason": "short reason"}]
}
```
- `replacement`: the replacing codes if deprecated, otherwise `[]`.
