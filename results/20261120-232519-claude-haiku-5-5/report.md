# Run claude-haiku-5-5

- **Agent:** claude-api (built-in loop), model claude-haiku-5-5
- **Skills given:** no
- **Series:** pilot, seed 101, built 2026-11-20T23:25:19+00:00
- **Grader:** pyproj 3.8.0 / PROJ 9.8.1, EPSG v12.029 (2025-10-02)
- **Score:** 53 of 53 checks passed (100%)

## dep-codes: Spot deprecated CRS codes (10/10)
*GIGS: 7000 (deprecation)*

| Check | Result | Detail |
|---|---|---|
| EPSG:20087 deprecated or not | pass | said True; registry: deprecated (Pulkovo 1995 / Gauss-Kruger 27N) |
| EPSG:20087 replacement | pass | said ['EPSG:2486']; registry: ['EPSG:2486'] |
| EPSG:10256 deprecated or not | pass | said False; registry: live (GS-IRF) |
| EPSG:6979 deprecated or not | pass | said True; registry: deprecated (IGD05) |
| EPSG:6979 replacement | pass | said ['EPSG:7135']; registry: ['EPSG:7135'] |
| EPSG:32662 deprecated or not | pass | said True; registry: deprecated (WGS 84 / Plate Carree) |
| EPSG:32662 replacement | pass | said ['EPSG:32663', 'EPSG:3786']; registry: ['EPSG:32663', 'EPSG:3786']; following the chain to live records: ['EPSG:4087'] |
| EPSG:7351 deprecated or not | pass | said False; registry: live (NAD83(2011) / InGCS Randolph-Wayne (m)) |
| EPSG:21894 deprecated or not | pass | said True; registry: deprecated (Bogota 1975 / Colombia East) |
| EPSG:21894 replacement | pass | said ['EPSG:21899']; registry: ['EPSG:21899'] |

## tfm-bng: British National Grid to WGS 84 (7/7)
*GIGS: 5100 + 5203 (TM conversion then Position Vector)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:27700; expected EPSG:27700 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.31e-10 degree (tolerance 3e-07), computed with EPSG:7710 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Input eastings/northings are British National Grid (EPSG:27700); inverse Transverse Mercator to OSGB36 (EPSG:4277) then EPSG:7710. Grid fetched from PROJ CDN on demand. Default PROJ 27700->4326 chooses the same operation (9); OSTN02 op 5339 returned inf in this environment so was not used. Helmert 1314 differs by about 1e-5 deg (~1 m).

## tfm-ed50-geog: ED50 North Sea positions to WGS 84 (7/7)
*GIGS: 5203-style (ED50 to WGS 84, North Sea)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4230; expected EPSG:4230 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1311; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.44e-10 degree (tolerance 3e-07), computed with EPSG:1311 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Input is ED50 geographic (EPSG:4230), lat/lon order. A UK-specific ED50 North Sea operation was not in this database; ED50 to WGS 84 (18) used. PROJ default for 4230->4326 would use a different (lower accuracy) operation; not used.

## tfm-ed50-utm31: ED50 / UTM zone 31N to WGS 84 (7/7)
*GIGS: 5100 + 5203-style (UTM conversion then ED50 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:23031; expected EPSG:23031 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1311; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.86e-10 degree (tolerance 3e-07), computed with EPSG:1311 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Inverse UTM zone 31N on ED50 (EPSG:23031 to EPSG:4230), then EPSG:1311. PROJ default for 23031->4326 picks ED50 to WGS 84 (1) (about 1 m different); EPSG:1311 chosen deliberately for North Sea accuracy.

## tfm-osgb36-geog: OSGB36 latitude/longitude to WGS 84 (7/7)
*GIGS: 5203 (Position Vector, OSGB36 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 5.00e-10 degree (tolerance 3e-07), computed with EPSG:7710 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Input is OSGB36 geographic (EPSG:4277), lat/lon order; all points within the GB area. Helmert alternative 1314 (2 m) differs by about 1e-5 deg (~1 m) at these points. Grid fetched from PROJ CDN on demand.

## tfm-outside-area: OSGB36 to WGS 84 with stray points (7/7)
*GIGS: 5203 (points outside the area of use)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged ['P05', 'P06']; expected ['P05', 'P06'] |
| coordinates within GIGS tolerance | pass | largest difference 3.99e-10 degree (tolerance 3e-07), computed with EPSG:7710 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: P05 (47.16N, 2.05E, France) and P06 (56.28N, 120.99E, Siberia/Russia region) lie far outside the OSGB36 area of use; not transformed. Left P05 and P06 as null rather than transforming them with an invalid operation. The other six points were transformed.

## tfm-reverse-roundtrip: WGS 84 to OSGB36, with a round trip (8/8)
*GIGS: 5203 (reverse direction and round trip)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| target CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| operation chosen | pass | used EPSG:7710; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.77e-10 degree (tolerance 3e-07), computed with EPSG:7710 |
| round trip within GIGS tolerance | pass | largest difference 0.00e+00 (tolerance 6e-08) |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Input is WGS 84 lat/lon (EPSG:4326). Results are OSGB36 geographic (EPSG:4277) lat/lon. Round trip applies the forward operation to the results. Round trip returns to inputs within rounding (see round_trip values).
