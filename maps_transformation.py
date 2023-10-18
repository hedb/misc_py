import os
import csv
import urllib.parse as urlparse


url = 'http://foo.appspot.com/abc?def=ghi'

def transform_to_kml_entity(row):

    #Output
    """
    <Placemark>
	<ExtendedData><SchemaData schemaUrl="#Saved_Places">
		<SimpleData name="Google Maps URL">http://maps.google.com/?cid=13109062879604241309</SimpleData>
		<SimpleData name="Location">{ &quot;Address&quot;: &quot;Artekale Kalea, 15, 48005 Bilbo, Bizkaia, Spain&quot;, &quot;Business Name&quot;: &quot;HOSTEL Quartier Bilbao&quot;, &quot;Country Code&quot;: &quot;ES&quot;, &quot;Geo Coordinates&quot;: { &quot;Latitude&quot;: &quot;43.2562036&quot;, &quot;Longitude&quot;: &quot;-2.9234867&quot; } }</SimpleData>
		<SimpleData name="Published">2018/07/26 08:16:52+00</SimpleData>
		<SimpleData name="Title">HOSTEL Quartier Bilbao</SimpleData>
		<SimpleData name="Updated">2018/07/26 08:16:52+00</SimpleData>
	</SchemaData></ExtendedData>
      <Point><coordinates>-2.9234867,43.2562036</coordinates></Point>
  </Placemark>
    """

    # Input
    # ['Azkuna Zentroa', '', 'https://www.google.com/search?q=Azkuna+Zentroa&ludocid=10032865328663185881&ibp=gwp;0,7']


    parsed = urlparse.urlparse(row[2])
    loc_coord = urlparse.parse_qs(parsed.query)['ludocid']

    ret = """
    <Placemark>
        <name>{}</name>
        <coordinates>{},0</coordinates>
	</Placemark>
    """.format(row[0],loc_coord)
    return ret


def main():
    input_dir = 'C:/Users/hedbn/PycharmProjects/misc/maps_data'

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_file_path = os.path.join(input_dir, filename)
            with open(input_file_path, newline='',encoding = 'utf-8') as csvfile:
                reader = csv.reader(csvfile)
                first_row = True
                for row in reader:
                    if (first_row):
                        first_row = False; continue
                    print(transform_to_kml_entity(row))



if __name__ == "__main__":
    main()