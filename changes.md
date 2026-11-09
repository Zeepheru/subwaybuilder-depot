# List of Changes

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
