# Nearby Places

This will use the Google Places API to find all local places within a radius and export them as JSON files.

You can then use the jsontoexcel to optionally export a json/series of JSON files into an excel spreadsheet. 

## Requirements

1) Configure the [Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview#how-use) to obtain an API key.

2) Store the API key in a .txt called 'google_api_key.txt' (included in .gitignore).

3) Go to Google Maps and right click to obtain lat/long and put them into NearbyPlaces.py. You might want to also use the 'measure' tool to figure out a good radius.

**NOTE**: Depending on locale: The maps measure tool may give distance in feet: the Places API takes distance in meters. You may need to convert.

4) Run NearbyPlaces.py as many times as needed. If you run it more than once, save the output to a different json.

5) If you want an .xls file, check requirements.txt (Pandas) and run jsontoexcel.py which will grab all .jsons in the directory and output an unstyled xlsx. 

## Licensing

I don't care, I used Claude to make this which was trained on unlicensed code from everyone else here, so do whatever. 