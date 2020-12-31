"""A script for converting alltheplaces geojson post box features into MapRoulette style geojsons

Currently stashing the output here:
https://gist.githubusercontent.com/Jeremiah-England/c06ef4461d9caca4c51734bd46a15e6f/raw/spartanburg-post-boxes.json

And the associated MapRoulette Challenge is here:
https://maproulette.org/admin/project/42267/challenge/15591
Or... probably here if you're not the admin:
https://maproulette.org/browse/challenges/15591
"""
import json
import math
from jsonseq.encode import JSONSeqEncoder


def tag_blue_pillar_boxes(features):
    """
    See https://wiki.openstreetmap.org/wiki/Key:post_box:type
    and https://wiki.openstreetmap.org/wiki/Key:colour
    """
    for f in features:
        if 'blue box' in f['properties']['name'].lower():
            f['properties']['post_box:type'] = 'pillar'
            f['properties']['colour'] = 'blue'


if __name__ == '__main__':
    features_file = 'data/spartanburg.geojson'
    with open(features_file, 'r') as f:
        feature_collection = json.load(f)

    collection_boxes = [f for f in feature_collection['features'] if f['properties']['@spider'] ==
                        'usps_collection_boxes']

    # see https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dpost_box
    for box in collection_boxes:
        box['properties']['amenity'] = 'post_box'

    tag_blue_pillar_boxes(collection_boxes)

    # keep_tags = {'note', 'collection_times', 'addr:full', 'addr:city', 'addr:state', 'addr:postcode', 'addr:country',
    #              'name', 'brand', 'amenity', 'post_box', 'post_box:type', 'colour'}
    drop_tags = ['ref', '@spider']
    for f in collection_boxes:
        for tag in drop_tags:
            del f['properties'][tag]

    # actually I want to keep these in. See here:
    # https://www.reddit.com/r/openstreetmap/comments/knz0x5/help_im_creating_a_test_map_roulette_project_with/
    # for f in collection_boxes:
    #     del f['id']

    # filter out overlapping po boxes taking the latter ones for now
    filtered_boxes = []
    for i in range(len(collection_boxes)):
        for j in range(i + 1, len(collection_boxes)):
            if math.dist(collection_boxes[i]['geometry']['coordinates'],
                         collection_boxes[j]['geometry']['coordinates']) < 0.000001:
                break
        else:
            filtered_boxes.append(collection_boxes[i])
    collection_boxes = filtered_boxes

    # convert to feature collection
    # collection_boxes = [{'type': 'FeatureCollection', 'features': [f]} for f in collection_boxes]

    print(len(collection_boxes))
    with open('data/spartanburg-post-boxes-2.geojson', 'w') as f:
        # See https://learn.maproulette.org/documentation/line-by-line-geojson/ for explanation of encoding
        # f.write(''.join(JSONSeqEncoder().encode(collection_boxes)))
        json.dump({'type': 'FeatureCollection', 'features': collection_boxes}, f)
