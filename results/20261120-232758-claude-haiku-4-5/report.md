# Run claude-haiku-4-5

- **Agent:** claude-api (built-in loop), model claude-haiku-4-5
- **Skills given:** no
- **Series:** pilot, seed 101, built 2026-11-20T23:27:58+00:00
- **Grader:** pyproj 3.8.0 / PROJ 9.8.1, EPSG v12.029 (2025-10-02)
- **Score:** 35 of 53 checks passed (66%)

## dep-codes: Spot deprecated CRS codes (2/10)
*GIGS: 7000 (deprecation)*

| Check | Result | Detail |
|---|---|---|
| EPSG:20087 deprecated or not | fail | said False; registry: deprecated (Pulkovo 1995 / Gauss-Kruger 27N) |
| EPSG:20087 replacement | fail | said []; registry: ['EPSG:2486'] |
| EPSG:10256 deprecated or not | pass | said False; registry: live (GS-IRF) |
| EPSG:6979 deprecated or not | fail | said False; registry: deprecated (IGD05) |
| EPSG:6979 replacement | fail | said []; registry: ['EPSG:7135'] |
| EPSG:32662 deprecated or not | fail | said False; registry: deprecated (WGS 84 / Plate Carree) |
| EPSG:32662 replacement | fail | said []; registry: ['EPSG:32663', 'EPSG:3786']; following the chain to live records: ['EPSG:4087'] |
| EPSG:7351 deprecated or not | pass | said False; registry: live (NAD83(2011) / InGCS Randolph-Wayne (m)) |
| EPSG:21894 deprecated or not | fail | said False; registry: deprecated (Bogota 1975 / Colombia East) |
| EPSG:21894 replacement | fail | said []; registry: ['EPSG:21899'] |

## tfm-bng: British National Grid to WGS 84 (6/7)
*GIGS: 5100 + 5203 (TM conversion then Position Vector)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:27700; expected EPSG:27700 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | fail | largest difference 1.91e-05 degree (tolerance 3e-07), computed with EPSG:1314 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Using best available transformation between OSGB36 and WGS 84

## tfm-ed50-geog: ED50 North Sea positions to WGS 84 (4/7)
*GIGS: 5203-style (ED50 to WGS 84, North Sea)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4230; expected EPSG:4230 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | fail | used EPSG:1198; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | fail | flagged none; expected ['P01', 'P05', 'P06'] |
| coordinates within GIGS tolerance | fail | no operation named, or not one PROJ knows for these CRSs |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Using best available transformation between ED50 and WGS 84

## tfm-ed50-utm31: ED50 / UTM zone 31N to WGS 84 (4/7)
*GIGS: 5100 + 5203-style (UTM conversion then ED50 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:23031; expected EPSG:23031 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | fail | used EPSG:1198; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | fail | flagged none; expected ['P01', 'P02', 'P03', 'P04', 'P05', 'P06'] |
| coordinates within GIGS tolerance | fail | no operation named, or not one PROJ knows for these CRSs |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: CRS transformation automatically handles both datum change and map projection change

## tfm-osgb36-geog: OSGB36 latitude/longitude to WGS 84 (6/7)
*GIGS: 5203 (Position Vector, OSGB36 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | fail | largest difference 2.08e-05 degree (tolerance 3e-07), computed with EPSG:1314 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Using best available transformation between OSGB36 and WGS 84

## tfm-outside-area: OSGB36 to WGS 84 with stray points (6/7)
*GIGS: 5203 (points outside the area of use)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged ['P05', 'P06']; expected ['P05', 'P06'] |
| coordinates within GIGS tolerance | fail | largest difference 1.86e-05 degree (tolerance 3e-07), computed with EPSG:1314 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Points outside OSGB36 area of use (Great Britain and surrounding) are marked with null values and listed Identified 2 points outside OSGB36 validity area

## tfm-reverse-roundtrip: WGS 84 to OSGB36, with a round trip (7/8)
*GIGS: 5203 (reverse direction and round trip)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| target CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | fail | largest difference 1.83e-05 degree (tolerance 3e-07), computed with EPSG:1314 |
| round trip within GIGS tolerance | pass | largest difference 0.00e+00 (tolerance 6e-08) |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Using best available transformation between WGS 84 and OSGB36 Round trip verifies the reversibility of the transformation with minimal numerical error
