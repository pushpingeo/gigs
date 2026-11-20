# Run Claude (Opus 5.5) via Claude Code, with skills

- **Agent:** Claude Code subagent (general-purpose), working in a copy of the packet, model claude-opus-5-5
- **Skills given:** yes
- **Series:** pilot, seed 210756892, built 2026-11-20T23:08:54+00:00
- **Grader:** pyproj 3.8.0 / PROJ 9.8.1, EPSG v12.029 (2025-10-02)
- **Score:** 53 of 53 checks passed (100%)

## dep-codes: Spot deprecated CRS codes (10/10)
*GIGS: 7000 (deprecation)*

| Check | Result | Detail |
|---|---|---|
| EPSG:20075 deprecated or not | pass | said True; registry: deprecated (Pulkovo 1995 / Gauss-Kruger 15N) |
| EPSG:20075 replacement | pass | said ['EPSG:2474']; registry: ['EPSG:2474'] |
| EPSG:20931 deprecated or not | pass | said False; registry: live (GSK-2011 / Gauss-Kruger zone 31) |
| EPSG:21481 deprecated or not | pass | said True; registry: deprecated (Beijing 1954 / Gauss-Kruger 21N) |
| EPSG:21481 replacement | pass | said ['EPSG:21461']; registry: ['EPSG:21461'] |
| EPSG:3752 deprecated or not | pass | said True; registry: deprecated (WGS 84 / Mercator 41) |
| EPSG:3752 replacement | pass | said ['EPSG:3994']; registry: ['EPSG:3994'] |
| EPSG:7843 deprecated or not | pass | said False; registry: live (GDA2020) |
| EPSG:4088 deprecated or not | pass | said True; registry: deprecated (World Equidistant Cylindrical (Sphere)) |
| EPSG:4088 replacement | pass | said ['EPSG:4087']; registry: ['EPSG:4087'] |

## tfm-bng: British National Grid to WGS 84 (7/7)
*GIGS: 5100 + 5203 (TM conversion then Position Vector)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:27700; expected EPSG:27700 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.94e-10 degree (tolerance 3e-07), computed with EPSG:1314 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Eastings/northings read as EPSG:27700 OSGB36 / British National Grid, metres, easting first. Inverse BNG projection (conversion) then EPSG:1314. Round trip back to BNG checked internally: within about 0.001 m (GIGS tolerance 0.006 m). Datum shifts 70-125 m range plausible.

## tfm-ed50-geog: ED50 North Sea positions to WGS 84 (7/7)
*GIGS: 5203-style (ED50 to WGS 84, North Sea)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4230; expected EPSG:4230 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1311; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.98e-10 degree (tolerance 3e-07), computed with EPSG:1311 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Read as ED50 (EPSG:4230) decimal degrees, latitude first, west negative; all points in the UK sector offshore. Datum shifts in the expected 110-125 m range; round trip checked internally.

## tfm-ed50-utm31: ED50 / UTM zone 31N to WGS 84 (7/7)
*GIGS: 5100 + 5203-style (UTM conversion then ED50 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:23031; expected EPSG:23031 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1311; acceptable: EPSG:1311 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.93e-10 degree (tolerance 3e-07), computed with EPSG:1311 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Read as EPSG:23031 ED50 / UTM zone 31N, metres, easting first, full (untruncated) eastings. Points fall at about 1.1-1.3E, west of the UK/Norway median line, so the UK-applicable 1311 is used rather than Norway's 1613. Round trip to UTM checked internally within about 0.001 m (GIGS tolerance 0.006 m).

## tfm-osgb36-geog: OSGB36 latitude/longitude to WGS 84 (7/7)
*GIGS: 5203 (Position Vector, OSGB36 to WGS 84)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.63e-10 degree (tolerance 3e-07), computed with EPSG:1314 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Read as OSGB36 (EPSG:4277) decimal degrees, latitude first, west negative. Round trip checked internally within 2e-8 deg (GIGS tolerance 6e-8).

## tfm-outside-area: OSGB36 to WGS 84 with stray points (7/7)
*GIGS: 5203 (points outside the area of use)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| target CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged ['P02', 'P07']; expected ['P02', 'P07'] |
| coordinates within GIGS tolerance | pass | largest difference 4.32e-10 degree (tolerance 3e-07), computed with EPSG:1314 |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: Read as OSGB36 (EPSG:4277) decimal degrees, latitude first, west negative. P02 (47.36N, 2.96E, central France) and P07 (64.45N, 124.27E, eastern Siberia) lie outside the area of use of OSGB36 and of EPSG:1314; swapping lat/lon does not bring either into Great Britain, so they look like rows that don't belong. Not transformed (null values); would only transform them on the owner's say-so, marked as outside.

## tfm-reverse-roundtrip: WGS 84 to OSGB36, with a round trip (8/8)
*GIGS: 5203 (reverse direction and round trip)*

| Check | Result | Detail |
|---|---|---|
| source CRS identified | pass | said EPSG:4326; expected EPSG:4326 or CRS84 |
| target CRS identified | pass | said EPSG:4277; expected EPSG:4277 |
| operation chosen | pass | used EPSG:1314; acceptable: EPSG:1314, EPSG:7710 (best stated accuracy whose area of use contains the points) |
| points outside the area of use flagged | pass | flagged none; expected none |
| coordinates within GIGS tolerance | pass | largest difference 4.96e-10 degree (tolerance 3e-07), computed with EPSG:1314 |
| round trip within GIGS tolerance | pass | largest difference 1.30e-08 (tolerance 6e-08) |
| computed with a tool, not by hand | pass | computed_by: library |
| provenance recorded | pass | operation, accuracy, EPSG version, engine |

Agent's notes: GPS positions read as WGS 84 (EPSG:4326) decimal degrees, latitude first, west negative. Round trip WGS 84 -> OSGB36 -> WGS 84 with the same operation (EPSG:1314) returns inputs within 2e-8 deg (GIGS tolerance 6e-8).
