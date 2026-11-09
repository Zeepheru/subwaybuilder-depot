# How foundation depths are calculated

MapGen produces two separate depth systems: building foundations estimated from
building height and footprint, and water-bed depths derived from bathymetry and
OSM water boundaries. The descriptions below follow the current implementation
in [maps.py](../src/depot/maps.py).

## Building foundations

`_calculate_building_foundation(coords, height, alpha=0.25)` calculates a single
depth for each footprint:

1. Construct a polygon from its exterior ring in longitude/latitude coordinates.
2. Find its minimum rotated bounding rectangle. This rectangle is computed in
   degrees, before measuring its sides in metres.
3. Measure two adjacent sides using the haversine function in
   [utils.py](../src/depot/utils.py), and use the shorter side as width `W`.
4. With building height `H` in metres, calculate:

   ```text
   raw_depth = alpha * H * (H / W) ** 0.25
   depth = int(max(10, min(raw_depth, 80)))
   ```

The default `alpha` is `0.25`. The result is a **positive depth in metres**,
clamped to 10–80 m and truncated to an integer, rather than rounded. Taller
buildings receive deeper foundations; at the same height, narrower buildings
also receive deeper foundations. The width is a bounding-rectangle dimension,
not footprint area or the narrowest local part of an irregular building.

Examples with the default `alpha`:

| Height H | Width W | Raw depth | Stored depth |
| -------- | ------- | --------- | ------------ |
| 4 m | 20 m | 0.67 m | 10 m |
| 40 m | 20 m | 11.89 m | 11 m |
| 100 m | 20 m | 37.38 m | 37 m |
| 200 m | 20 m | 88.91 m | 80 m |

This is a heuristic for game collision depths. It does not inspect actual piles,
basements, soil, ground elevation, geology, or nearby water. Although the helper's
caller describes `alpha` as a soil stiffness parameter, it uses a constant rather
than a soil dataset. `alpha` is an internal method argument, not a `MapGen`
constructor parameter.

### Inputs, defaults, and outputs

Buildings come from a supplied `buildings_geojson` or an Overture download.
`process_buildings()` cleans, filters, and simplifies the footprints before
creating collision indices. `generate_pmtiles()` separately prepares footprints
for the display tiles.

| Output | Depth representation |
| ------ | -------------------- |
| `buildings_index.json` and `.json.gz` | Each building's `f` field stores the positive depth. |
| `buildings_index.bin` and `.bin.gz` | Each building's foundation depth is stored as a float32, using the same integer-valued calculation. |
| `buildings_foundations.geojson` / `.mbtiles` | The `foundationDepth` property uses the same formula; the tile layer is named `foundations`. |
| `<CITY>_foundations.pmtiles` | Separate building foundation display archive, exported when `create_building_foundations=True`. Tiles start at zoom 12. |

The index writers substitute a height of 4 m only when `height` is absent or
`None`. The display path also replaces empty or non-positive heights with 4 m
through `_set_default_building_height()`. Its attempted fallback for nonnumeric
values is incomplete: an earlier `float(val)` check can raise before the
exception handler. Input heights should therefore be valid numeric values.

With `create_building_foundations=False`, both collision indices use a fixed
10 m depth and the separate foundation PMTiles archive is not exported. The
current display pipeline still calls `_create_building_foundation_files()` and
creates its intermediate files even when that flag is false.

### Why collision and display results can differ

- Collision and display footprints use separate simplification settings:
  `building_index_simplification` and `building_tile_simplification`. Changes to
  the resulting rectangle can change the estimated depth. Currently, both paths
  filter using `building_index_filter_size`.
- The JSON index processes every component of a MultiPolygon separately. The
  binary index keeps only the largest component by area in coordinate space.
  The foundation display writer assigns depths only to Polygon features.
- Only exterior coordinates enter the formula; courtyard holes do not affect
  the bounding rectangle.
- The helper returns 10 m if the measured width is non-positive, but a degenerate
  footprint can fail earlier when its bounding rectangle is a line or point.

## Ocean and inland-water depths

`load_bathymetry_data()` supplies the water depth index and the
`ocean_foundations` display layer. Despite the naming, this also covers inland
water included in its OSM mask. Depths here are **negative elevations in metres**;
for example, `-5` represents a water bed 5 m below the zero reference.

1. Load elevations from the configured OPeNDAP endpoint. The current default
   points to the GEBCO 2026 sub-ice dataset. Read the map bounding box plus a
   `0.05` degree buffer.
2. Linearly interpolate onto a grid with latitude spacing `CELL_SIZE=0.0027`
   degrees and longitude spacing corrected by the cosine of the map's midpoint
   latitude. Cubically interpolate onto a denser grid using
   `resolution_multiplier=4` before constructing contours. This smooths the
   available data; it does not add measured detail.
3. Generate negative-elevation contour bands. Boundaries are spaced at 5 m near
   zero, 10 m from 40 m, 50 m from 100 m, 100 m from 500 m, and 1,000 m from
   1,000 m depth. The deepest sampled value is also inserted as a boundary.
   Each band receives its lower, more negative boundary as its stored depth.
4. Repair and combine contour polygons, subtracting shallower regions from
   deeper ones with small geometric buffers around the boundaries.
5. Build a water mask from the raw Planetiler MBTiles `water` and `waterway`
   layers at `maxzoom`. Line waterways are buffered into polygons. Ditches are
   skipped; canals and drains are skipped unless `include_canals_drains=True`.
6. Assign `-5` m to OSM water regions not covered by a bathymetric contour,
   provided the combined gap area exceeds `1e-7` square degrees. Clip all
   contours to the OSM water mask and map bounding box.
7. Split the contours into spatial grid cells for the collision index. Entries
   within each cell are ordered shallowest first. Coordinates are rounded to six
   decimal places for serialization.

The fallback is a fixed assumption for missing coverage, rather than a measured
river or lake depth. The use of discrete contour bands, interpolation, buffers,
and rounded coordinates also means these outputs approximate the source data.
The education and retail overlap toggles do not alter these depth calculations.

### Outputs and caching

| Output | Purpose |
| ------ | ------- |
| `ocean_depth_index.json.gz` | Collision index: grid cells reference polygons with bounds `b`, negative depth `d`, and rings `p`. |
| `ocean_depth_index_contours.json.gz` | Full contour polygons before cell splitting, used for the display layer. |
| `ocean_foundations.geojson` / `.mbtiles` | Display features with `kind="ocean_foundation"` and `depth_min` equal to the contour's negative depth. Tiles start at zoom 8. |

`generate_pmtiles()` merges the ocean foundation tiles into the main map archive.
`create_ocean_foundations=False` skips this ocean-depth generation and merge path.

`reprocess_bathymetry_data` defaults to **False in the constructor**, despite its
docstring saying True. When false and both compressed index and contour files
exist, they are loaded without checking whether the bounding box, OSM water,
source dataset, or parameters changed. Set it to `True` to regenerate those
outputs after changing inputs, including `include_canals_drains`. The raw MBTiles
must be available for regeneration. If no contours survive the water-mask clip,
the loader returns without writing new depth files.

## Code entry points

- Building formula: `MapGen._calculate_building_foundation`.
- Collision indices: `MapGen.process_buildings`, `_convert_to_game_format`, and
  `create_buildings_index_binary`.
- Building display: `MapGen._generate_building_tiles`,
  `_set_default_building_height`, and `_create_building_foundation_files`.
- Water depths: `MapGen.load_bathymetry_data`, `_process_columns_worker`, and
  `_generate_ocean_depth_tiles`.
- Archive assembly and feature flags: `MapGen.generate_pmtiles`.
