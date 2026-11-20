# Run claude-haiku-4-5

- **Agent:** claude-api (built-in loop), model claude-haiku-4-5
- **Skills given:** yes
- **Series:** pilot, seed 101, built 2026-11-20T23:30:30+00:00
- **Grader:** pyproj 3.8.0 / PROJ 9.8.1, EPSG v12.029 (2025-10-02)
- **Score:** 49 of 53 checks passed (92%)

## dep-codes: Spot deprecated CRS codes (6/10)
*GIGS: 7000 (deprecation)*

| Check | Result | Detail |
|---|---|---|
| EPSG:20087 deprecated or not | pass | said True; registry: deprecated (Pulkovo 1995 / Gauss-Kruger 27N) |
| EPSG:20087 replacement | fail | said ['EPSG:28427']; registry: ['EPSG:2486'] |
| EPSG:10256 deprecated or not | pass | said False; registry: live (GS-IRF) |
| EPSG:6979 deprecated or not | pass | said True; registry: deprecated (IGD05) |
| EPSG:6979 replacement | fail | said ['EPSG:6975']; registry: ['EPSG:7135'] |
| EPSG:32662 deprecated or not | pass | said True; registry: deprecated (WGS 84 / Plate Carree) |
| EPSG:32662 replacement | fail | said ['EPSG:32661']; registry: ['EPSG:32663', 'EPSG:3786']; following the chain to live records: ['EPSG:4087'] |
| EPSG:7351 deprecated or not | pass | said False; registry: live (NAD83(2011) / InGCS Randolph-Wayne (m)) |
| EPSG:21894 deprecated or not | pass | said True; registry: deprecated (Bogota 1975 / Colombia East) |
| EPSG:21894 replacement | fail | said ['EPSG:3115']; registry: ['EPSG:21899'] |

## tfm-bng: British National Grid to WGS 84 (7/7)
*GIGS: 5100 + 5203 (TM conversion then Position Vector)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:27700; expected EPSG:27700 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.43e-09 degree (tolerance 3e-07), computed with EPSG:7710 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: All coordinates within valid BNG range (0-700km E, 0-1200km N) British National Grid is based on OSGB36 with Transverse Mercator projection. The transformation includes automatic BNG inverse.

## tfm-ed50-geog: ED50 North Sea positions to WGS 84 (7/7)
*GIGS: 5203-style (ED50 to WGS 84, North Sea)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4230; expected EPSG:4230 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1311; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.56e-09 degree (tolerance 3e-07), computed with EPSG:1311 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: All well positions assumed within North Sea area ED50 is European Datum 1950, used for North Sea oil and gas positions

## tfm-ed50-utm31: ED50 / UTM zone 31N to WGS 84 (7/7)
*GIGS: 5100 + 5203-style (UTM conversion then ED50 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:23031; expected EPSG:23031 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1311; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.93e-09 degree (tolerance 3e-07), computed with EPSG:1311 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: All platform positions within ED50/UTM zone 31N coverage ED50 / UTM zone 31N is a projected CRS for UK North Sea platforms

## tfm-osgb36-geog: OSGB36 latitude/longitude to WGS 84 (7/7)
*GIGS: 5203 (Position Vector, OSGB36 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.86e-09 degree (tolerance 3e-07), computed with EPSG:7710 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: All survey sites assumed within Great Britain OSGB36 geographic is based on OSGB36 datum. All points well within area of use.

## tfm-outside-area: OSGB36 to WGS 84 with stray points (7/7)
*GIGS: 5203 (points outside the area of use)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged ['P05', 'P06']; expected ['P05', 'P06'] |
| coordinates within GIGS tolerance | pass | largest difference 4.97e-09 degree (tolerance 3e-07), computed with EPSG:7710 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: OSGB36 area of use defined by bounding box: lon -8.6 to 1.9, lat 49.9 to 60.9 Points P05, P06 are outside OSGB36 area of use and were not transformed. These likely represent data entry errors or points from other regions.

## tfm-reverse-roundtrip: WGS 84 to OSGB36, with a round trip (8/8)
*GIGS: 5203 (reverse direction and round trip)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| target CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.88e-09 degree (tolerance 3e-07), computed with EPSG:7710 |
| round trip within GIGS tolerance | pass | largest difference 0.00e+00 (tolerance 6e-08) |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: GPS positions assumed within Great Britain area Round trip from WGS 84 to OSGB36 and back to WGS 84 confirms transformation accuracy. Differences should be within GIGS tolerance (0.006m / 0.00000006 degrees).
