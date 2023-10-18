import json
import re





if __name__ == "__main__":
    input_file_name = "C:/Users/hedbn/Desktop/performance/app_definitions.csv"
    output_file_name = "C:/Users/hedbn/Desktop/performance/app_definitions_output.tsv"

    output_file = open(output_file_name,'w')

    with open(input_file_name, "r") as infile:

        for line in infile:
            try:
                data = json.loads(line)

                output_file.write(data["nginx_http_host"] + "\t"  + nginx_upstream_content_type + "\t"  + "http://" + data["nginx_http_host"] + " : " + data["nginx_request"])
                output_file.write("\n")

            except (RuntimeError, TypeError, NameError, json.decoder.JSONDecodeError):
                print(line)
                pass
