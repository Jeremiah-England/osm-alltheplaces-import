# osm-alltheplaces-import
A collection of scripts for assisting the import of [alltheplaces] data into openstreetmap

The scripts are currently for preparing a local import into the SC Update area. But they 
could easily be adapted to another area in the United States and maybe other places as well.

## Getting Started

You can run the download script to get the data. 

```shell
python scripts/download.py
```

Be sure to call the script from the repository directory as shown, 
not the `scripts` directory (I use the path relative to where the
file is called from for reading and writing files.)

Alternatively you can download it from the [alltheplaces] site and 
save extract it all to `<repository>/data/alltheplaces` where the 
geojsons are *directly* in the `alltheplaces` directory. The other 
scripts assume this placement.

## Filtering by Zip

To filter by zipcode run

```shell
python scripts/filter_by_zips.py
```

Again, be sure to call from the repository directory as shown for the 
same reason mentioned in for the download script.

It will save a geojson to `data/filtered_by_zip.geojson` all the
filtered places in it.

## ToDo

There are a lot of points that cannot be filtered by zip code because
either the property key for the zip code is different/missing or the 
zipcode could not be casted to an integer. I should

1. Investigate what other zipcode keys there are, if any.
2. See if any zips are not casting to int and if it's reasonable to ignore them all.

Finally, we should also look into getting shapefiles with county boundaries
and filtering geospatially to see what features are in the aread that are 
missing or have mis-formatted zip codes.

<!-- References --> 

[alltheplaces]: https://alltheplaces.xyz
