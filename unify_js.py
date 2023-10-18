import urllib.request


input_file = "C:/Users/hedbn/Desktop/js_file_list.txt"
output_file = "C:/localhost/unified.js"


with open(input_file, "r") as infile:
    with open(output_file, "w",encoding='utf-8') as outfile:
        for line in infile:
            print("Downloading " + line)
            response = urllib.request.urlopen(line)
            data = response.read()  # a `bytes` object
            text = data.decode('utf-8',errors='ignore')  # a `str`; this step can't be used if data is binary
            outfile.write("// __START__" + line + "\n")
            outfile.write(text + "\n\n\n")