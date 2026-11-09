# List of Changes to Code

## Additional high-level methods

### `MapGen.copy_output_artifacts(path='out/')`

Copies the README's registry artifacts from the city directory to a destination
relative to that directory, excluding demand data and `config.json`. Creates the
destination and returns the copied paths. Copies both compressed building indices,
the compressed ocean depth index, roads, runways/taxiways, `<CITY>.pmtiles`, and
`<CITY>_foundations.pmtiles`. Roads and runways/taxiways prefer `.geojson`, with
`.geojson.gz` as a fallback. Filenames were verified against `cities/SIN`.

Missing source files produce a warning without stopping the other copies.
Existing matching destination files are overwritten; unrelated files are
preserved, including any existing demand data and config. Absolute destination
paths and the city directory itself are rejected. This method is called
explicitly and is not part of `run_all()`.

## Extra Configuration

(To be highlighted separately from the native Depot ones)

### `include_canals_drains`

New `MapGen` boolean parameter, defaulting to `False`.

Under `maps.py/load_bathymetry_data`

Don't include canals and drains

`if feature_kind == 'canal' or feature_kind == 'drain'`, `continue` as well

### `resolve_edu_overlaps`

New `MapGen` boolean parameter, defaulting to `True`.

When enabled, subtract school, college, and university zones from parks, and
subtract water and aerodromes from those education zones. Education keeps the
game's `type="college"` schema in the `commercial` layer. Set to `False` to
preserve the previous education overlap behavior.

### `resolve_retail_overlaps`

New `MapGen` boolean parameter, defaulting to `True`.

When enabled, subtract retail zones from parks, and subtract water and aerodromes
from retail zones. Set to `False` to preserve the previous retail overlap
behavior. Both options apply in `maps.py/_process_tile_worker` independently;
ordinary commercial zones continue to resolve overlaps regardless of either
option.
