import json
import re





if __name__ == "__main__":
    input_file_name = "C:/Users/hedbn/Desktop/Flow/sample_log.txt"
    output_file_name = "C:/Users/hedbn/Desktop/Flow/sample_output.tsv"

    output_file = open(output_file_name,'w')


    with open(input_file_name, "r") as infile:

        regex = re.compile(r";.*")

        for line in infile:
            try:
                line = line.replace('"nginx_response_time": -','"nginx_response_time": "-"')
                data = json.loads(line)

                nginx_upstream_content_type = data["nginx_upstream_content_type"]
                nginx_upstream_content_type = regex.sub("",nginx_upstream_content_type)

                # if (nginx_upstream_content_type != "text/html"):
                #     continue

                output_file.write(data["nginx_http_host"] + "\t"  + nginx_upstream_content_type + "\t"  + "http://" + data["nginx_http_host"] + " : " + data["nginx_request"])
                output_file.write("\n")

            except (RuntimeError, TypeError, NameError, json.decoder.JSONDecodeError):
                print(line)
                pass
