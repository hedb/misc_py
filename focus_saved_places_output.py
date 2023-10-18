import math
import json
from pprint import pprint


focus_x = -73.6046458
focus_y = 45.5336596


if __name__ == "__main__":

    input_file = "C:/Users/hedbn/Dropbox/Canada/2017/Takeout/Maps (your places)/Saved Places.json"
    output_file = "C:/Users/hedbn/Dropbox/Canada/2017/Takeout/Maps (your places)/Montreal.json"


    with open(input_file, encoding="utf8") as data_file:
        data = json.loads(data_file.read())
        for item in data["features"]:
            x = item['geometry']['coordinates'][0];
            y = item['geometry']['coordinates'][1];
            if (( (x-focus_x)**2 +  (y-focus_y)**2 ) < 10) :
                pprint(item)
