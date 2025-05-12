import json
import os

import unstructured_client
from unstructured_client.models import operations, shared


def save_dict_list_json_file(*,file_name,dicts : list):
    with open(file_name, "w") as f:
        json.dump([d for d in dicts], f)


# https://github.com/Unstructured-IO/unstructured
# https://docs.unstructured.io/api-reference/api-services/sdk
# https://api.unstructured.io/general/docs#/default/pipeline_1_general_v0_general_post


def parse_pdf_to_json(*, input_filename, output_filename):
    client = unstructured_client.UnstructuredClient(
        api_key_auth=os.environ.get("UNSTRUCTURED_API_KEY"),
        server_url="https://api.unstructuredapp.io",
    )

    with open(input_filename, "rb") as f:
        data = f.read()

    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=shared.Files(
                content=data,
                file_name=input_filename,
            ),
            # --- Other partition parameters ---
            # Note: Defining 'strategy', 'chunking_strategy', and 'output_format'
            # parameters as strings is accepted, but will not pass strict type checking. It is
            # advised to use the defined enum classes as shown below.
            strategy=shared.Strategy.AUTO,
            languages=['eng'],
        ),
    )

    try:

        res = client.general.partition(request=req)

        output_dir = os.path.dirname(output_filename)
        os.makedirs(output_dir, exist_ok=True)
        save_dict_list_json_file(file_name=output_filename, dicts=res.elements)
    except Exception as e:
        print(e)


def get_element_text(element):
    ret = None
    type_ = element['type']
    if type_ not in ['Image', 'Footer', 'PageNumber']:
        ret = '\n' if type_ in ['Title', 'Header'] else ''
        if type_ in ['NarrativeText', 'UncategorizedText']:
            ret += element['text']
        else:
            ret += f"{type_} : {element.get('text', '')}"
        ret += '\n'
    return ret


def split_json_to_pages(*, output_dir, load_filename):
    pages = {}
    with open(load_filename, "r") as f:
        data = json.load(f)
        for i, element in enumerate(data):
            page_number = element['metadata']['page_number']
            if page_number == 3:
                print(element)
            page_text_so_far = pages.get(page_number, '')
            page_text = get_element_text(element)
            if page_text:
                pages[page_number] = page_text_so_far + page_text
    for page_number, text in pages.items():
        output_filename = f"{output_dir}/page_{page_number}.txt"
        with open(output_filename, "w") as f:
            f.write(text)


if __name__ == "__main__":
    parse_pdf_to_json(input_filename="/Users/hed-bar-nissan/Downloads/diagram.pdf",
                      output_filename="output/diagram.pdf.json")