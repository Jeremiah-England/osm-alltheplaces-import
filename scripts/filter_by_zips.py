"""A short script for filtering the places by zipcode

If you call this from the scripts/ directory instead of
the repository directory, make sure to change the 'data'
paths in main to '../data'
"""
import glob
import os
import json


def filter_by_zips(zipcodes, directory):
    """Filter all the features that have given zipcodes

    Parameters
    ----------
    zipcodes : List[str]
        A list of zipcodes to filter for
    directory : str
        The directory where all the alltheplaces geojsons live

    Returns
    -------
    geojson: Dict[str, Any]
        a geojson in terms of python objects
    """
    filtered_features = []
    num_empty = 0
    num_decode_errors = 0
    num_key_errors = 0
    num_value_errors = 0
    num_non_errors = 0
    for file in glob.glob(f'{directory}/*.geojson'):
        if os.stat(file).st_size == 0:  # skip the empty files
            num_empty += 1
            continue

        try:
            with open(file, 'r') as f:
                geojson = json.load(f)
        except json.JSONDecodeError:
            num_decode_errors += 1
            continue

        for f in geojson['features']:
            try:
                if int(f['properties']['addr:postcode']) in zipcodes:
                    filtered_features.append(f)
                num_non_errors += 1
            except KeyError:
                num_key_errors += 1
                continue
            except ValueError:
                num_value_errors += 1
                continue

    print(f'Number of empty files:                                      {num_empty}')
    print(f'Number of file decode errors:                               {num_decode_errors}')
    print(f'Number of key errors (no zip property or different format): {num_key_errors}')
    print(f'Number of value errors (cannot cast zip to integer):        {num_value_errors}')
    print(f'Number of features without errors:                          {num_non_errors}')
    print(f'Number of places found within zip codes:                    {len(filtered_features)}')

    return {'type': 'FeatureCollection', 'features': filtered_features}


if __name__ == '__main__':
    data_directory = 'data/alltheplaces'
    out_file = 'data/filtered_by_zip.geojson'

    greenville_county_zips = {29680, 29607, 29681, 29609, 29611, 29683, 29614, 29613, 29616, 29615, 29687, 29690, 29617,
                              29627, 29635, 29356, 29636, 29644, 29650, 29651, 29654, 29661, 29662, 29669, 29673, 29601,
                              29605}
    spartanburg_county_zips = {29320, 29323, 29322, 29324, 29330, 29329, 29331, 29334, 29333, 29336, 29335, 29338,
                               29346, 29349, 29365, 29369, 29368, 29372, 29374, 29373, 29376, 29375, 29378, 29377,
                               29385, 29388, 29302, 29301, 29304, 29303, 29306, 29316, 29307, 29319}

    zip_codes_master_list = greenville_county_zips | spartanburg_county_zips

    filtered_geojson = filter_by_zips(zip_codes_master_list, data_directory)
    with open(out_file, 'w') as f:
        json.dump(filtered_geojson, f)
