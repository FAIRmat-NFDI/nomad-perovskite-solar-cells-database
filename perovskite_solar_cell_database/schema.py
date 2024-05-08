
from nomad.datamodel.data import EntryData, UseCaseElnCategory

from .schema_sections import Ref, Cell, Module, Substrate, ETL, Perovskite, PerovskiteDeposition, HTL, Backcontact, Add, Encapsulation, JV, Stabilised, EQE, Stability, Outdoor
from nomad.metainfo import Package, Section, SubSection
import json
from .schema_sections.utils import create_archive

m_package = Package(name='perovskite_solar_cell_database')


class PerovskiteSolarCell(EntryData):
    """
    This schema is adapted to map the data in the [Perovskite Solar Cell Database
    Project](https://www.perovskitedatabase.com/). The descriptions in the quantities
    represent the instructions given to the user who manually curated the data.
    """

    m_def = Section(
        label='Perovskite Solar Cell',
        a_eln=dict(lane_width='400px'),
        categories=[UseCaseElnCategory])

    ref = SubSection(section_def=Ref)
    cell = SubSection(section_def=Cell)
    module = SubSection(section_def=Module)
    substrate = SubSection(section_def=Substrate)
    etl = SubSection(section_def=ETL)
    perovskite = SubSection(section_def=Perovskite)
    perovskite_deposition = SubSection(section_def=PerovskiteDeposition)
    htl = SubSection(section_def=HTL)
    backcontact = SubSection(section_def=Backcontact)
    add = SubSection(section_def=Add)
    encapsulation = SubSection(section_def=Encapsulation)
    jv = SubSection(section_def=JV)
    stabilised = SubSection(section_def=Stabilised)
    eqe = SubSection(section_def=EQE)
    stability = SubSection(section_def=Stability)
    outdoor = SubSection(section_def=Outdoor)



import numpy as np
from nomad.metainfo import (
    Quantity, Datetime, Section)
from nomad.datamodel.data import ArchiveSection
from nomad.units import ureg


class LLM(EntryData):
    """Information about the source of the data. It describes who curated the data,
     the journal in which the data was published,
     the DOI number of the publication, the lead author and the publication date."""

    m_def = Section(
        label='LLM',
        a_eln=dict(lane_width='800px'),
        categories=[UseCaseElnCategory])


    doi = Quantity(
        type=str,
        shape=[],
        description="""
                    """,
        a_eln=dict(
            component='FileEditQuantity'))

    def normalize(self, archive, logger):
        # schema = """
        #     Here is the schema in JSON:
        #     {
        #         "devices": [
        #         {
        #             "device_stack": [
        #             "string"
        #             ],
        #             "perovskite_absorber_chemical_formula": string,
        #             "scan_direction": valid-choices-only-from: {['forward', 'reversed']},
        #             "pce": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "jsc": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "voc": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "ff": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "active_area": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "light_intensity": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "bandgap": {
        #             "value": float,
        #             "unit": "string",
        #             "extra_info": "string"
        #             },
        #             "substrate": "string",
        #             "backcontact": "string",
        #             "hole_transport_layer": "string",
        #             "electron_transport_layer": "string | string",
        #             "extra_info": "string"
        #         }
        #         ]
        #     }
        #     """
        # prompt = (
        #     "Can you list out the different solar cell devices mentioned in the text below. Try to fill all the values in the schema. Only provide a JSON output.")
        # import requests
        # import json
        #
        # from chemdataextractor import Document
        #
        # f = open('tests/data/10.3390--nano9010121.pdf', 'rb')
        # doc = Document.from_file(f)
        #
        # for item in doc.elements:
        #     if "References" in str(item):
        #         index_to_delete = doc.elements.index(item)
        #         del doc.elements[index_to_delete:]
        #
        # paper_text = ' '.join(map(str, doc.elements))
        #
        # url = "http://172.28.105.30/backend/api/generate"
        # # llama_messages=[
        # # {
        # #     'role': 'system',
        # #     'content': 'You are a solar cell scientist. You only give answers in valid JSON with extracted data given a schema.'
        # # },
        # # {
        # #     'role': 'user',
        # #     'content': prompt + "\n" + schema + "\n" + paper_text,
        # # },]
        #
        # response = requests.post(url, json={
        #     "model": "llama3:70b",
        #     "seed": 42,
        #     "options": {"temperature": 0},
        #     "stream": False,
        #     "prompt": paper_text + "\n" + prompt + "\n" + schema,
        #     # "messages": llama_messages
        # })
        #
        # resp = json.loads(response.content)["response"]
        

        data = """
        {
  "devices": [
    {
      "device_stack": ["MAPbI3"],
      "perovskite_absorber_chemical_formula": "MAPbI3",
      "scan_direction": "forward",
      "pce": {"value": 4.27, "unit": "%", "extra_info": ""},
      "jsc": {"value": 11, "unit": "mA/cm2", "extra_info": ""},
      "voc": {"value": 0.9, "unit": "V", "extra_info": ""},
      "ff": {"value": 53, "unit": "%", "extra_info": ""},
      "active_area": {"value": null, "unit": null, "extra_info": ""},
      "light_intensity": {"value": 100, "unit": "mW/cm2", "extra_info": "AM1.5"},
      "bandgap": {"value": null, "unit": null, "extra_info": ""},
      "substrate": "",
      "backcontact": "",
      "hole_transport_layer": "",
      "electron_transport_layer": "",
      "extra_info": ""
    },
    {
      "device_stack": ["MAPbI3", "QD-FAPbBrI"],
      "perovskite_absorber_chemical_formula": "MAPbI3",
      "scan_direction": "forward",
      "pce": {"value": 6.54, "unit": "%", "extra_info": ""},
      "jsc": {"value": null, "unit": null, "extra_info": ""},
      "voc": {"value": null, "unit": null, "extra_info": ""},
      "ff": {"value": 43.3, "unit": "%", "extra_info": ""},
      "active_area": {"value": null, "unit": null, "extra_info": ""},
      "light_intensity": {"value": 100, "unit": "mW/cm2", "extra_info": "AM1.5"},
      "bandgap": {"value": null, "unit": null, "extra_info": ""},
      "substrate": "",
      "backcontact": "",
      "hole_transport_layer": "",
      "electron_transport_layer": "",
      "extra_info": ""
    },
    {
      "device_stack": ["MAPbI3", "QD-FAPbBrI2"],
      "perovskite_absorber_chemical_formula": "MAPbI3",
      "scan_direction": "forward",
      "pce": {"value": 7.59, "unit": "%", "extra_info": ""},
      "jsc": {"value": 17.4, "unit": "mA/cm2", "extra_info": ""},
      "voc": {"value": 0.9, "unit": "V", "extra_info": ""},
      "ff": {"value": 48.6, "unit": "%", "extra_info": ""},
      "active_area": {"value": null, "unit": null, "extra_info": ""},
      "light_intensity": {"value": 100, "unit": "mW/cm2", "extra_info": "AM1.5"},
      "bandgap": {"value": null, "unit": null, "extra_info": ""},
      "substrate": "",
      "backcontact": "",
      "hole_transport_layer": "",
      "electron_transport_layer": "",
      "extra_info": ""
    }
  ]
}
        """
        resp = json.loads(data)



        for i, device in enumerate(resp['devices']):
            solarcell.jv = JV()
            solarcell.jv.default_Voc = device.get("voc").get("value")
            solarcell.jv.default_Jsc = device.get("jsc").get("value")
            solarcell.jv.default_FF = device.get("ff").get("value")
            solarcell.jv.defalt_PCE = device.get("pce").get("value")
            
            solarcell.backcontact = Backcontact()
            solarcell.backcontact.stack_sequence = device.get("backcontact")

            solarcell.htl = HTL()
            solarcell.htl.stack_sequence = device.get("hole_transport_layer")

            solarcell.substrate = Substrate()
            solarcell.substrate.stack_sequence = device.get("substrate")

            solarcell.perovskite = Perovskite()
            solarcell.perovskite.composition_long_form = device.get("perovskite_absorber_chemical_formula")

            solarcell.cell = Cell()
            solarcell.cell.stack_sequence = " | ".join(device.get("device_stack"))
            solarcell.area_measured = device.get("active_area").get("value")

            solarcell.normalize(archive, logger)

            create_archive(solarcell, archive, f'llm-solar-cell-entry-{i}.archive.json')
            # print(json.loads(response.content.decode('ascii').strip())['message']['content'])
        super().normalize(archive, logger)


m_package.__init_metainfo__()
