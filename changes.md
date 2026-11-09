# List of Changes

## Extra Configuration

(To be highlighted separately from the native Depot ones)

### `include_canals_drains`

Under `maps.py/load_bathymetry_data`

Don't include canals and drains

`if feature_kind == 'canal' or feature_kind == 'drain'`, `continue`
