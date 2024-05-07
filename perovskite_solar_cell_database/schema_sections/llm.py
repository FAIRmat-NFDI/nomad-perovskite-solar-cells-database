import numpy as np
from nomad.metainfo import (
    Quantity, Datetime, Section)
from nomad.datamodel.data import ArchiveSection
class LLM(ArchiveSection):
    """Information about the source of the data. It describes who curated the data,
     the journal in which the data was published,
     the DOI number of the publication, the lead author and the publication date."""

    m_def = Section(
        a_eln=dict(lane_width='800px'))

    doi = Quantity(
        type=str,
        shape=[],
        description="""
                    """,
        a_eln=dict(
            component='FileEditQuantity'))


    def normalize(self, archive, logger):
        schema = """
            Here is the schema in JSON:
            {
                "devices": [
                {
                    "device_stack": [
                    "string"
                    ],
                    "perovskite_absorber_chemical_formula": string,
                    "scan_direction": valid-choices-only-from: {['forward', 'reversed']},
                    "pce": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "jsc": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "voc": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "ff": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "active_area": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "light_intensity": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "bandgap": {
                    "value": float,
                    "unit": "string",
                    "extra_info": "string"
                    },
                    "substrate": "string",
                    "backcontact": "string",
                    "hole_transport_layer": "string",
                    "electron_transport_layer": "string | string",
                    "extra_info": "string"
                }
                ]
            }          
            """
        prompt = ("Can you list out the different solar cell devices mentioned in the text below. Try to fill all the values in the schema. Only provide a JSON output.")
        import requests
        import json

        from chemdataextractor import Document

        f = open('', 'rb')
        doc = Document.from_file(f)

        for item in doc.elements:
            if "References" in str(item):
                index_to_delete = doc.elements.index(item)
                del doc.elements[index_to_delete:]

        paper_text = ' '.join(map(str, doc.elements))

        url = "http://172.28.105.30/backend/api/generate"
        # llama_messages=[
        # {
        #     'role': 'system',
        #     'content': 'You are a solar cell scientist. You only give answers in valid JSON with extracted data given a schema.'
        # },
        # {
        #     'role': 'user',
        #     'content': prompt + "\n" + schema + "\n" + paper_text,
        # },]

        response = requests.post(url, json={
            "model": "llama3:70b",
            "seed": 42,
            "options":{"temperature":0},
            "stream": False,
            "prompt": paper_text + "\n" + prompt + "\n" + schema,
            # "messages": llama_messages
        })
        print(json.loads(response.content)["response"])
        # print(json.loads(response.content.decode('ascii').strip())['message']['content'])
