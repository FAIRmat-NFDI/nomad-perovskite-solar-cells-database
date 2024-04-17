from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import Quantity

from perovskite_solar_cell_database.schema_sections.utils import add_solar_cell

from .vars import etl_enum_edit_quantity_suggestions


class ETL(ArchiveSection):
    """
    A section to describe information related to the Electron Transport Layer (**ETL**).
    """

    stack_sequence = Quantity(
        type=str,
        shape=[],
        description="""
    The stack sequence describing the electron transport layer. Use the following formatting guidelines
- With the ETL, we refer to any layer between the substrate and the perovskite in a nip-device, and any layer between the perovskite and the back contact in a pin-device.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If two materials, e.g. A and B, are mixed in one layer, list the materials in alphabetic order and separate them with semicolons, as in (A; B)
- If no electron transport layer, state that as ‘non’
- Use common abbreviations when appropriate but spell it out if risk for confusion.
- If a material is doped, or have an additive, state the pure material here and specify the doping in the columns specifically targeting the doping of those layers.
- There is no sharp well-defined boundary between when a material is best considered as doped or as a mixture of two materials. When in doubt if your material is best described as doped or as a mixture, use the notation that best capture the metaphysical essence of the situation.
- There are a lot of stack sequences described in the literature. Try to find your one in the list. If it is not there (i.e. you may have done something new) define a new stack sequence according to the instructions.
ExampleBelow are some of the most common electron transport layers
TiO2-c | TiO2-mp
TiO2-c
PCBM-60
PCBM-60 | BCP
SnO2-np
C60 | BCP
SnO2-c
TiO2-c | TiO2-mp | ZrO2-mp
ZnO-c
PCBM-60 | C60 | BCP
PCBM-60 | LiF
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=etl_enum_edit_quantity_suggestions)))

    thickness = Quantity(
        type=str,
        shape=[],
        description="""
    A list of thicknesses of the individual layers in the stack. Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- The layers must line up with the previous filed.
- State thicknesses in nm
- Every layer in the stack have a thickness. If it is unknown, state this as ‘nan’
- If there are uncertainties, state the best estimate, e.g write 100 and not 90-110
Example
200
nan |250
100 | 5 | 8
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '40.0 | 50.0', '50.0 | 7.0', '40.0 | nan', '5.0 | 65.0 | nan', '50.0 | 200.0', 'nan | 400.0 | 1700.0', '20.0 | 400.0', '40.0 | 3.0 | 2.0 | 2.0', '40.0 | 150.0', '14000.0', '50.3', '27.0 | 600.0', '40.0 | 210.0', 'nan | 1100.0', '25.0 | 150.0', 'nan | 600.0', 'nan | 2000.0 | nan', '0.0', '30.0 | 351.0', '12.7 | 40.0 | 6.0', '27.0 | 175.0', 'nan | 950.0', 'nan | 100.0 | 2000.0', '40.0 | 353.0', '1800.0', '60.0 | 12.0', 'nan | 480.0 | 900.0', 'nan | 400.0 | nan', 'nan | 600.0 | 1200.0', '160.0 | 40.0', '141.0 | 200.0', '2.4', '50.0 | 1000.0 | 1000.0', 'nan | 325.0', 'nan | 1000.0 | 4500.0', '614.0', '87.0', '8.0 | nan | 1.0', '70.0', 'nan | 5400.0', 'nan | 1000.0 | 1008.0', '500.0', '85.0 | nan', '80.0 | 365.0', '4.0 | nan', '76.0', '90.0 | 400.0', '45.0 | 4.0', '6.0 | 20.0 | 8.0', '35.0 | 150.0', '100.0 | nan | 2.0', '100.0 | 300.0', '2.0 | 4.0 | nan', '50.0 | 50.0 | 300.0', '30.0 | 440.0', '14.0 | nan', '2.0 | 1.0', '31.1', '240.0', '50.0 | 100.0 | 400.0 | 50.0', '101.0 | 500.0', 'nan | nan | 7.0', 'nan | 320.0', '75.0 | 500.0', '95.0 | 365.0', '50.0 | 480.0', '30.0 | 600.0', 'nan | 25.0', 'nan | 1000.0 | 1010.0', '60.0 | 2500.0', '30.0 | 200.0 | nan', '40.0 | 300.0', '1.0 | 25.0 | 6.0', '120.0 | 0.5', '26.0', '55.0 | 5.0', 'nan | 30.0 | 10.0', '700.0 | 80.0', '50.0 | 6.3', 'nan | 500.0 | 500.0 | 10000.0', '20.0 | nan | 20.0', '60.0 | 460.0', '80.0 | 120.0', 'nan | 2000.0 | 2000.0', '9.0', '72.0 | 200.0', '20.0 | 20.0 | 20.0', 'nan | 600.0 | nan', '30.0 | 12000.0', '50.0 | 200.0 | 115.0', 'nan | 270.0', '5000.0', '50.0 | 250.0', 'nan | 500.0 | 3000.0', '700.0 | 2400.0', '30.0 | 130.0', '70.0 | nan', '17.0 | 350.0', '90.0 | 300.0', '80.0 | 1050.0 | 1.0', '70.0 | 80.0 | nan', '6.0 | 54.0', '36.0', '50.0 | 30.0', '23.0 | nan | 1.0', 'nan | 100.0', 'nan | 440.0', '50.0 | 1.0', 'nan | 220.0', '15.0 | 50.0', '50.0 | 180.0', 'nan | 55.0', '106.0 | nan', '25.0 | 15.0', '100.0 | 130.0 | nan', '80.0 | 1400.0', '23.0 | 7.0', '50.0 | 620.0', 'nan | 500.0 | 1300.0', '80.0 | 300.0 | 1400.0', '40.0 | 10.0', '368.0 | nan', '30.0 | 240.0', 'nan | 20.0 | 5.0', 'nan | 2000.0 | 1000.0', '58.0 | 200.0', '0.2 | nan', '135.0', '2.0 | nan', 'nan | 120.0', '15.0 | 6.0', '30.0 | 20.0 | 8.0', '90.0 | 200.0', '5.5', '200.0 | 700.0 | 1000.0', '40.0 | 40.0 | 150.0 | 150.0', 'nan | 750.0', '8.0 | nan | nan', '80.0 | 900.0 | 1.0', '1.2 | 10.0 | 8.0 | 2.0', '277.0', '60.0 | 24.0', '50.0 | 400.0 | 400.0', '27.0 | 275.0', 'nan | 500.0 | 500.0', 'nan | 6.0 | nan | nan', '20.0 | 30.0', '50.0 | 5.0 | 5.0', 'nan | 1300.0', '60.0 | 15.0', '10.0 | nan | 1.0', 'nan | 290.0', '50.0 | 1000.0 | 800.0', '91.0', '60.0 | 30.0', '15.0 | 180.0', '7.5', '405.0', '100.0 | 30.0 | 10.0', '80.0 | 20.0', '13.0 | 20.0 | 8.0', '30.0 | 20.0', 'nan | 100.0 | nan', '65.0 | nan', '50.0 | 50.0 | 6.3', 'nan | 453.0', '30.0 | 350.0', '5.0 | 20.0 | 8.0', '40.0 | 5.0 | 40.0', '40.0 | 3.0', '75.0', '20.0 | 5.0', 'nan | 0.6', '40.0 | 3.0 | 2.0 | 0.5', 'nan | 180.0', 'nan | 600.0 | 500.0', 'nan | 1050.0 | 350.0', 'nan | 5502.0', '22.0', '10.0 | 40.0', '50.0 | nan | 30.0 | 10.0 | 0.05 | 0.8', '35.0 | 40.0', '63.0', '60.0 | 3.0', '34.0', '50.0 | 300.0 | 500.0', '10000.0 | nan | nan', '100.0 | 60.0', '43.0 | nan | 1.0', 'nan | nan | 305.0', '100.0 | 600.0', '70.0 | 80.0 | nan | nan', '280.0', '60.0', '40.0 | 360.0', '45.0 | nan', '7.0', '440.0', '400.0', 'nan | 0.7', '25000.0', '1.5', 'nan | 450.0', '128.0', '20.0 | nan', 'nan | 660.0', '600.0 | 340.0', '208.0 | 200.0', '40.0 | 250.0', '50.0 | 150.0', 'nan | 1000.0 | 1004.0', '50.0 | nan | 1.0', 'nan | 200.0', '12.0', '60.0 | 120.0', '800.0 | 200.0', '100.0', '40.0 | 10.8', 'nan | 1073.0', '70.0 | 130.0', '55.0 | 75.0', '20.0 | 260.0', '15.0 | 1.0', 'nan | nan | 1.5', '15.0 | 400.0', '55.0 | nan', '38.69', '120.0 | 700.0', '16.39', '60.0 | 530.0', '3.0 | 25.0 | 6.0', '70.0 | 10.0', '75.0 | 365.0', '50.0 | 600.0', 'nan | 3600.0', '30.0 | 550.0', '290.0', '100.0 | 1.3', 'nan | 20.0 | 0.6', '55.0 | nan | nan', '50.0 | 540.0', '43.0 | 10.0', '50.0 | 100.0', '40.0 | 5.0', '20.0 | 25.0 | nan', '60.0 | 1500.0', '50.0 | 800.0 | 700.0', '35.0 | 15.0', '30.0 | 150.0', '40.0 | 7.5', 'nan | 15.0 | 6.0', '140.0 | 380.0', '10.0 | 150.0', 'nan | 670.0', '20.0 | 6.0', 'nan | 350.0 | nan', '17.0 | 170.0', '80.0 | 60.0', '20.0 | 10.0 | 10.0', '500.0 | 3000.0', '90.0 | 60.0', 'nan | 20000.0', '15.0 | 20.0', 'nan | 170.0', '60.0 | 50.0 | 45.0', '22.0 | 150.0', '60.0 | nan | 10.0', '7.0 | nan', '44.0', '45.0 | 100.0', '550.0', '5.0 | 30.0', '65.0 | 30.0', '140.0 | nan', '119.0 | 35.0', '50.0 | 1000.0 | 500.0', '3.0 | 50.0', '80.0 | 300.0', '120.0', '50.0 | 500.0', 'nan | 1000.0 | 1011.0', '110.0', '20.0 | 15.0', '100.0 | 340.0', 'nan | 15.0 | 150.0', '68.0 | nan', 'nan | 7.0 | nan | nan', '150.0 | 2.0', '65.0 | 10.0', '40.0 | 20.0 | 40.0', '590.0', '770.0', '90.0 | nan', '70.0 | 20.0', '17.5 | 100.0', '50.0 | 3.0', '75.0 | 200.0', '60.0 | 7.5', '85.0 | 150.0', '33.0 | 200.0', '15.0 | 220.0', 'nan | 452.0', 'nan | 700.0', '5.0 | 7.5 | 20.0', '100.0 | 4.3', '100.0 | 2.0', '800.0 | 340.0', 'nan | 1000.0 | 1002.0', '60.0 | 0.5', '47.03', '210.0', '5.0 | 80.0', '29.0 | 20.0 | 8.0', '40.0 | 260.0', '251.0', '0.5 | 90.0 | 7.0', '42.0 | nan | 1.0', 'nan | 3.0 | 1.0', '17.0 | 140.0', '129.0', '30.0 | 15.0', '14.0 | nan | nan', '50.0 | 220.0', 'nan | 10.0', 'nan | 0.0', 'nan | 9400.0', '6.0 | 340.0', '40.0 | 345.0', '50.0 | 75.0', '17.0 | 150.0', 'nan | 604.0', '30.0 | nan | 200.0', '100.0 | 2.1', '50.0 | 420.0', '40.0 | 3.0 | 2.0 | 1.0', '10.0 | 75.0', 'nan | 550.0 | 2500.0', '10.0 | 50.0', 'nan | 1000.0 | 1005.0', 'nan | 6.0', '100.0 | nan', 'nan | 1000.0 | 2000.0', 'nan | 510.0', '40.0 | 8.0', '1900.0', '90.0', 'nan | 857.0 | 2000.0', '32.0 | nan', '10.0 | 340.0', '89.0 | nan', 'nan | 130.0', '10.0 | 180.0', '40.0 | 4.0', '300.0 | 500.0', '668.0', '142.0 | 20.0 | 8.0', '40.8 | 8.0', '29.0 | nan | 1.0', 'nan | 200.0 | 200.0', 'nan | 800.0', '15.0 | 150.0', '21.0 | 150.0', '47.6', 'nan | 40.0 | 6.0', '25.0 | 187.0', '40.0 | 30.0', '20.0 | nan | nan', 'nan | 70.0 | 350.0', '31.0 | nan | 1.0', 'nan | 20.0 | 10.0', '25.0 | 4.0', 'nan | 1470.0', 'nan | 25.0 | 10.0', '40.0 | 140.0', '1.0 | 30.0 | nan | nan | nan', '28.0 | nan', '11.0', 'nan | 480.0 | 480.0', '56.0 | 250.0', 'nan | 801.0', '50.0 | 2.3', '30.0 | 200.0', 'nan | 53.0', 'nan | 15.0 | 25.0', '5.0 | 150.0', '10.0 | 350.0', '10.0 | 5.0', '60.0 | 80.0', 'nan | 1800.0', '80.0 | 280.0 | 1.0', 'nan | 60.0 | 1000.0', '70.0 | 170.0', '80.0 | 450.0 | 1.0', '30.0 | 1050.0', '30.0 | 8.0', '300.0 | 340.0', 'nan | 380.0', '50.0 | 400.0', '100.0 | 8.3', '11.0 | nan', 'nan | 1.0 | 1.0', '10.0 | 270.0', '23.0 | 20.0', 'nan | 700.0 | 5.0', 'nan | 460.0', '27.0 | 80.0 | 27.0 | 80.0 | 27.0 | 80.0 | 27.0', 'nan | 23.0 | 7.0', 'nan | 125.0 | nan', '11.0 | 120.0', '25.0 | 200.0', '166.9', '3.0 | 40.0 | 6.0', '30.0 | 40.0', 'nan | 13.0', 'nan | 1.0', '30.0 | 2.0', '50.0 | 350.0 | 2.5', '300.0 | 4.0', '8.0', 'nan | 8.0', 'nan | 3.0', 'nan | 360.0', '70.0 | 400.0', '30.0 | 9.0', '20.0 | 10.0', '40.0 | 365.0', '4.0 | 350.0', '60.0 | 140.0', '22.5 | 10.0', '200.0 | nan', '30.0 | 8.0 | 1.0', 'nan | nan | nan | 15.0', '90.0 | 45.0', '70.0 | 500.0 | 2000.0', '100.0 | 6.0', '30.0 | 250.0', 'nan | 548.0', '10.0 | 20.0', '50.0 | 156.0', '30.0 | 450.0 | 500.0', '1.3 | 50.0 | nan', '65.0', 'nan | 45.0', '40.0 | 600.0', '11.2 | 3.0', 'nan | 60.0', '43.9', '55.0 | 8.0', '40.0 | 380.0', '5.0 | nan | 1.0', '5.0 | 20.0', 'nan | 25000.0', '40.0 | 400.0 | 6.0', '31.0 | 150.0', '244.0', '120.0 | 7.0', '47.0', 'nan | 7.0', '50.0 | 1000.0 | 1200.0', '24.0 | 500.0 | nan', 'nan | 125.0', 'nan | 12.0', '28.0 | nan | nan', '1.0 | nan', '5.0 | 45.0', 'nan | 500.0 | nan | 2000.0', '30.0 | 500.0', '200.0 | 20.0', 'nan | 1000.0 | 1012.0', 'nan | 2000.0 | 1000.0 | nan', '97.0 | nan', 'nan | 800.0 | 500.0', '100.0 | 1000.0 | 500.0', '50.0 | 80.0', '49.0', '40.0 | 468.0', '31.2', 'nan | 610.0', '60.0 | 2.5', '30.0 | 910.0', '8.0 | 50.0', '20.0 | 20.0 | nan', 'nan | 450.0 | 400.0', 'nan | 52.0', '30.0 | 1.0 | 8.0', '50.0 | 80.0 | nan', '10.0 | 17.0', '67.0', '30.0 | 7.0', '45.0 | 25.0', 'nan | 430.0', '1.0 | 15.0 | 10.0', '24.6', '60.0 | 5.0', 'nan | 23.0 | 8.0', '13.3 | 40.0 | 6.0', 'nan | 118.0', '380.0', '50.0 | 1.6', '700.0', '50.0 | 300.0 | nan | nan', '300.0 | 1.0', '40.0 | 3.0 | 1.0', 'nan | nan | 1.2', 'nan | 400.0 | 900.0', '1.0 | 30.0 | 8.0', '60.0 | 100.0', '37.0', '110.0 | nan', '7.5 | 20.0', 'nan | 150.0 | nan', '45.0 | 1.0', '5.0', '900.0', '20.0 | 3.0', '50.0 | 440.0', '8.9 | 40.0 | 6.0', '500.0 | 3000.0 | 10000.0', '15.0 | 300.0', 'nan | 240.0', '10.0 | 48.0', '45.0 | 125.0', '20.0 | 7.0', '80.0 | 720.0 | 1.0', '30.0 | 100.0', '840.0', '8.3 | 40.0 | 6.0', 'nan | nan | 4.0', '15.0 | 40.0', 'nan | 3.5', '20.0 | 250.0', '600.0', '12000.0 | nan', '40.0 | 174.0', '10.0 | 130.0', '6.0 | nan', '40.0 | 100.0', '105.0', '100.0 | 500.0', '69.0', '17.0 | 80.0', 'nan | 300.0 | 150.0', '68.5', '10000.0 | nan', '40.0 | 7.0', '70.0 | 40.0', 'nan | nan | 3.0', '110.0 | 700.0', 'nan | 30.0 | 8.0', 'nan | 1250.0', '30.0 | 342.0', '4.0 | 80.0', '45.0 | 8.0', '0.5 | 25.0 | 6.0', '70.0 | 500.0', 'nan | 8300.0', '0.84 | 3.0', '10.0 | 1.0', 'nan | 5000.0', '30.0 | 386.0', '1.0 | 10.0 | 6.0', '300.0 | 3.0', '60.0 | 13.0', '64.0 | 200.0', 'nan | 300.0 | 400.0', '100.0 | 800.0', '50.0 | 3.8', '45.0 | 2.0', '1.5 | nan | nan', '50.0 | 400.0 | nan', '117.0', '25.0 | 3.0', '36.0 | 20.0 | 8.0', 'nan | 1000.0 | 4000.0', 'nan | 25.0 | 8.0', '52.0 | 270.0', 'nan | 50.0', 'nan | 5800.0', '30.0 | 170.0', '60.0 | 270.0', '60.0 | 50.0 | 70.0', '300.0 | nan', 'nan | 480.0 | 600.0', '30.0 | 175.0', 'nan | 451.0', '30.0 | 310.0', '2.5 | 10.0', 'nan | 390.0', '35.0 | 2.0', 'nan | 1000.0 | 1500.0', '189.0', '55.0 | 365.0', '80.0 | nan', '6.0', '100.0 | 20.0', '20.0 | 100.0', '80.0 | 190.0', '40.0 | 1000.0 | 1000.0', '61.0', '20.0 | 80.0', '80.0 | 500.0', '55.0 | 0.5', '1.0 | 340.0', '50.0 | 280.0', 'nan | 20.0 | 8.0', '15.0', '52.2', 'nan | 1000.0 | 3000.0', '100.0 | nan | 10.0', '430.0', '41.0 | 10.0', '70.0 | 80.0', '1.0 | 30.0 | nan | nan', '80.0 | 1.0', '50.0 | 700.0 | 450.0', 'nan | 800.0 | 1500.0', '60.0 | 280.0', '80.0 | 200.0', '20.0 | 8.0', '100.0 | 365.0', 'nan | 1200.0', '27.0 | nan', '1000.0', '25.0 | nan', '16.0 | 150.0', 'nan | 500.0 | nan | 1200.0', 'nan | 238.0', '15.0 | 15.0', 'nan | 650.0', 'nan | 40.0', '40.0 | 1.0', '80.0 | 800.0', 'nan | 850.0', '8.0 | 40.0', '30.0 | 150.0 | nan', '390.0', '70.0 | 350.0', '10.0', '80.0 | 3.0', '42.0', '30.0 | 45.0', '30.0 | nan', '20.0 | 1.0', '65.0 | 250.0', '52.0 | 10.0', '40.0 | 2.0', 'nan | 1000.0 | 1007.0', '15.0 | 260.0', 'nan | 2.8', '51.0 | 270.0', '5.0 | 10.0', '25.0 | 0.5', '30.0 | 201.0', 'nan | 40.0 | 8.0', '5.0 | 12.0 | 20.0', '265.0 | nan', '90.0 | 350.0', 'nan | 500.0 | nan | 3000.0', 'nan | 100.0 | 400.0', '5.0 | 20.0 | 7.0', '8.0 | 340.0', 'nan | nan | 4.8', '42.0 | 10.0', '3.0 | 200.0', 'nan | 5500.0', 'nan | 450.0 | 1200.0', '30.0', '35.0 | 30.0', '20.0 | 12.0', '88.0 | nan', '70.0 | 150.0', '745.0', '20.0 | 18.0', 'nan | 480.0', 'nan | nan | 2.0', '3.2 | 40.0 | 6.0', '10.0 | nan | nan', '30.0 | 200.0 | 1.9', '152.0', '26.0 | nan', '10.0 | 15.0', '10.0 | 400.0', '60.0 | 20.0', 'nan | 1.2', 'nan | 20.0 | 3.0', '60.0 | 190.0', 'nan | 285.0', '30.0 | 265.0', '50.0 | 430.0', '80.0 | 550.0 | 1.0', '62.0 | nan', '60.0 | 260.0', 'nan | 2000.0 | 1100.0', '50.0 | 190.0', '140.0', 'nan | 1500.0 | 2000.0', '70.0 | 100.0', '20.0 | 150.0', 'nan | 3900.0', '6.0 | nan | nan', '60.0 | 40.0', 'nan | 618.0', 'nan | 400.0', '80.0 | 175.0', '40.0 | 30.0 | 30.0', '50.0 | 13.6', '24.0 | nan | nan', '15.0 | 10.0', '89.0', 'nan | 580.0', '100.0 | 800.0 | 1000.0', '220.0', 'nan | 210.0 | nan | nan', '20.0 | 40.0', 'nan | nan | 450.0', '35.0 | 0.1', '40.0 | 1900.0', '47.0 | 34.0', '30.6', '30.0 | 2000.0', 'nan | 160.0', '55.0 | 250.0', '40.0 | 3.0 | 1.0 | 1.0', '40.0 | 500.0', '17.0 | 200.0', '70.0 | nan | 150.0', '60.0 | 200.0 | nan', '100.0 | 400.0', '30.0 | 0.0', 'nan | 500.0 | 3000.0 | 10000.0', 'nan | 40.0 | 9.0', '24.0 | 8.0', '60.0 | nan | 5.0', '15.0 | 365.0', '95.0', 'nan | nan | 121.0', '60.0 | 350.0', '42.4', 'nan | 400.0 | 10.0', '5.6 | 40.0 | 6.0', '50.0 | 40.0', '20.0 | 7.5', '130.0 | nan', '100.0 | 1000.0 | 1000.0', '193.0', '50.0 | 8.0', '73.0', '57.0 | 250.0', '1300.0', 'nan | nan | 258.0', '2000.0', '40.0 | 180.0 | nan', 'nan | 27.0 | 1.0', '5.0 | 7.0', '10000.0 | 5.0', '17.0 | nan', '55.0 | 300.0', '175.0', '60.0 | 70.0', 'nan | nan | 20.0', 'nan | nan | 40.0 | 8.0', '55.0 | 10.0', '50.0 | 800.0 | 1200.0', '30.0 | 216.0', '112.0', '17.0 | 230.0', '2.0 | 20.0 | 8.0', '30.0 | 308.0', '33.0 | nan', 'nan | 500.0 | 1000.0', '101.0', '3.0 | nan | nan', 'nan | 330.0', '10.0 | 10.0 | 10.0', '50.0 | 30.0 | 8.0', '30.0 | 7.5', '32.0 | nan | nan', 'nan | 224.0', '176.0', '341.0', '60.0 | 50.0 | 150.0', '34.0 | nan | 1.0', 'nan | 480.0 | nan', 'nan | 80.0', 'nan | 540.0', '650.0', '60.0 | 50.0 | 30.0', '220.0 | nan', '60.0 | 8.0', '60.0 | 360.0', '60.0 | 200.0', '10.0 | 25.0', '30.0 | 1730.0', 'nan | 280.0', '24.0 | 30.0', 'nan | 110.0', '100.0 | 450.0', '56.0 | nan', '37.8 | 8.0', '20.0 | 2.0', '80.0 | 10.0', '80.0 | 30.0', 'nan | 500.0 | 1000.0 | 10000.0', '40.0 | 190.0', 'nan | 8000.0', '70.0 | 1.0', 'nan | 1000.0 | 1001.0', 'nan | 380.0 | nan', '150.0', '50.0 | 19360.0', 'nan | 70.0', '20.0 | 220.0', 'nan | 140.0', '30.0 | 910.0 | nan', 'nan | 1000.0', '30.0 | 30.0', '46.0 | nan', 'nan | 20.0', '43.8', '15.0 | nan', '56.0 | 200.0', '30.0 | 70.0', 'nan | 7.5', '39.4', '40.0 | 165.0 | nan', 'nan | 1050.0', '30.0 | nan | nan', '33.0', '51.0', '50.0 | 0.8', '1.0 | 5.0', '30.2', '16.0 | nan', 'nan | 600.0 | 2500.0', '60.0 | 50.0', '50.0 | 300.0', '100.0 | 150.0', 'nan | 500.0 | 1300.0 | 70.0', '27.0 | 20.0 | 8.0', '100.0 | 390.0', 'nan | nan | 1.0', '54.0 | 250.0', '2.0 | 340.0', '5.0 | 1.0', 'nan | 585.0', '45.0 | 3.0', '25.0', '1.0 | 20.0', '72.0 | nan', '80.0 | 1000.0', '2.0 | 40.0', '40.0 | 350.0', '100.0 | 700.0 | 1500.0', '60.0 | 6.0', '25.0 | 6.0', '15.0 | 175.0', '35.0 | nan', '100.0 | 220.0', '30.0 | 1000.0 | 2000.0', '100.0 | 844.0', '30.0 | 100.0 | 100.0', '10.0 | nan', '40.0 | 200.0', '35.0 | 365.0', '3.0 | nan', '45.0 | 30.0', 'nan | nan | 75.0', '115.0 | nan', '40.0 | 6.0', '40.0 | 40.0 | 5.0', '45.0 | 55.0', 'nan | 480.0 | 500.0', '30.0 | 400.0', 'nan | 550.0', '60.0 | 60.0', '40.0 | 230.0', '100.0 | nan | 5.0', 'nan | 160.0 | nan', '125.0', 'nan | 30.0', '250.0 | 100.0', '550.0 | nan', '4.0 | 0.0', '50.0 | 170.0', '50.0 | 250.0 | 300.0', 'nan | 15.0', 'nan | 400.0 | 600.0', '20.0 | 240.0', '510.0', '24.0 | nan', 'nan | 79.0', '80.0 | 150.0', '20.0 | 200.0', 'nan | 275.0', 'nan | 10.0 | 3.0', 'unkown', '0.8 | nan', '4.0', '50.0 | 585.0', '7.0 | 20.0 | 8.0', '40.0 | 120.0', 'nan | 850.0 | nan', '740.0', '8.0 | nan', '30.0 | 330.0', '252.0', 'nan | 230.0', '31.7 | 6.0', '0.5', '54.0 | 10.0', '10.0 | 20.0 | 8.0', '88.0 | 200.0', '100.0 | 15.0 | 1.0', '995.0', '350.0', '20.0 | 600.0', '3.0', '76.2', 'nan | 300.0 | 1100.0', '20.0 | nan | 5.0', '4.0 | 20.0 | 8.0', '43.0 | nan', '1.0 | 10.0', 'nan | nan', '50.0 | 130.0', '100.0 | 8.4', '80.0 | 2.0', '20.0 | 160.0', '100.0 | 15.0 | 5.0', 'nan | 500.0 | 1500.0', 'nan | 500.0 | nan', '160.0', 'nan | 564.0', '100.0 | 8.0', '20.0 | 50.0', '18.0 | nan', '25.0 | 100.0', '40.0 | 20.0 | 8.0', '3.0 | 0.0', 'nan | 210.0', '25.0 | 35.0', '40.0 | 165.0', '15.0 | 45.0', 'nan | 900.0', '55.0', '10.0 | 210.0', '23.0 | nan', '60.0 | 1.0', '60.0 | 365.0', '17.0', '300.0 | 200.0', '5.0 | 60.0', '42.0 | nan', '70.0 | 350.0 | nan', '700.0 | 420.0', '17.0 | 5.0', '19.0', 'nan | 1000.0 | 12000.0', 'nan | 30.0 | 7.0', '79.0', '40.0 | 150.0 | 150.0', '18.0', '34.0 | 200.0', '130.0', '39.0', '30.0 | 1000.0', 'nan | 90.0', '80.0 | 5.0', '310.0', '10.0 | 100.0', 'nan | 300.0 | 6.0', 'nan | 10000.0', '70.0 | 180.0', '78.0', '100.0 | 0.6', '60.0 | 500.0', 'nan | 2200.0', '65.0 | 2.0', '30.0 | 50.0', '120.0 | 2.0', '235.0', 'nan | 1000.0 | 60.0 | 1000.0', '1050.0', '45.0 | 7.5', 'nan | 8.0 | 5.0', '25.0 | 400.0', '40.0 | 400.0', '20.0 | 35.0', '140.0 | 0.5', '45.0 | 80.0', '90.0 | 7.0', 'nan | 25.0 | 7.0', '80.0 | 170.0', '74.0 | 200.0', '10.0 | 370.0', '27.0 | 80.0 | 27.0 | 80.0 | 27.0', '30.0 | 6.0', '141.0 | nan', 'nan | 410.0', '65.0 | 300.0', '50.0 | 300.0 | nan', '525.0', '20.0 | nan | 10.0', '50.0 | 1000.0 | 1800.0', '370.0', '30.0 | 850.0', '56.1', '80.0 | 500.0 | 1400.0', '35.0 | 200.0', '24.0', 'nan | 480.0 | 300.0', '30.0 | 400.0 | 450.0', 'nan | 473.0', 'nan | 8600.0', '50.0 | 130.0 | 1.0', '200.0 | 200.0', 'nan | 375.0', '41.2', '23.0 | 8.0', '30.0 | 260.0', 'nan | 1500.0', 'nan | 75.0 | 1400.0', '50.0 | 0.3', '38.0 | nan', '0.5 | 7.5', '27.0 | 60.0 | 27.0 | 60.0 | 27.0 | 60.0 | 27.0', '60.0 | 20.0 | 7.0', '5.0 | 400.0', 'nan | 8.0 | 1.0', '50.0 | 500.0 | 500.0', 'nan | 700.0 | 1800.0', '100.0 | 350.0', '460.0', '30.0 | 5.0', '60.0 | 450.0', '35.0 | nan | 1.0', '45.0 | 7.0', 'nan | 230.0 | nan', '100.0 | 250.0', '100.0 | 200.0', 'nan | 222.0', '80.0', '31.0 | nan', '12.0 | nan', '45.0 | 300.0', '131.0 | 200.0', 'nan | 5.0', '46.0', '320.0', 'nan | 195.0', '50.0 | 830.0', '40.0 | 80.0', '1.0 | 30.0 | 6.0', '20.0 | 130.0', '25.0 | 120.0', '50.0 | 10.0', '39.0 | 206.0 | 186.0', '50.0 | 16.0', '25.0 | 5.0', '60.0 | 93.0', 'nan | nan | 213.0', 'nan | nan | 1500.0', '80.0 | 200.0 | 200.0', 'nan | 1400.0', '30.0 | 1.0', '8.0 | 23.0', 'nan | 250.0', '24.0 | 500.0', '100.0 | 10.0', '12.0 | 600.0 | 600.0', '70.0 | 90.0', '95.0 | 20.0 | 8.0', '50.0', 'nan | 405.0', '180.0', '45.0', '40.0 | 70.0', '22.0 | 80.0', '70.0 | 800.0', 'nan | 260.0', 'nan | 400.0 | 400.0', '40.0 | 6.0 | 2.0', 'nan | 800.0 | 2500.0', '123.0', '50.0 | 350.0', '60.0 | 10.0', '120.0 | nan', '40.0 | 2000.0 | nan', '60.0 | 150.0', '5.0 | 35.0', '41.0', '130.0 | 40.0', '0.5 | 50.0', '60.0 | 900.0', '114.0', '5.0 | nan', 'nan | 2.5', 'nan | 1000.0 | 1006.0', '1.0 | 7.5', 'nan | 175.0', '1.0', '4.0 | 340.0', '54.0', '50.0 | nan | nan', '80.0 | 22.0', '32.0 | 200.0', '38.0 | 20.0 | 8.0', '17.0 | 110.0', '630.0', '50.0 | 130.0 | 100.0', '20.0 | 5.0 | 10.0', '1.1 | nan', '50.0 | 450.0', '145.0 | nan', '25.0 | 8.0', '80.0 | 400.0', '50.0 | 50.0', '35.0 | 8.0', '30.0 | 500.0 | 2000.0', '85.0 | 30.0 | 7.0', 'nan | nan | 8.0', '80.0 | 600.0', '21.0', '60.0 | 560.0', 'nan | 5501.0', '1000.0 | 340.0', '50.0 | 1400.0 | 500.0', '420.0', '45.0 | 200.0', '50.0 | 640.0', '70.0 | 100.0 | nan', '85.0', '20.0 | 20.0 | 8.0', '60.0 | 250.0', '53.0 | 250.0', '25.0 | 500.0', 'nan | 150.0', '70.0 | 600.0', '50.0 | 700.0 | 700.0', 'nan | 370.0', '50.0 | 700.0 | 500.0', 'nan | 36.0 | 1.0', '5.0 | 40.0', '60.0 | 750.0', '620.0', '10.0 | 200.0', '184.2', '22.0 | nan', '13.0', '50.0 | 15.0', '13.0 | 80.0', '20.0 | 10.0 | 0.5', 'nan | 1000.0 | 1000.0', 'nan | nan | nan', 'nan | 250.0 | nan', '20.0', '30.0 | 300.0', '31.0 | 20.0 | 8.0', '1400.0', '65.0 | 0.5', 'nan | 717.0', '25.0 | 500.0 | 1000.0', '2.3', 'nan | 4800.0', '90.0 | 440.0', 'nan | 790.0', '1100.0', '30.0 | 1650.0', '25.0 | 7.0', '92.0', '60.0 | 700.0', 'nan | 600.0 | 2000.0', '30.0 | 120.0', '30.0 | 80.0', '20.0 | 300.0', 'nan | 90.0 | nan', '55.0 | 650.0', '0.0 | 340.0', '250.0', '35.0 | 300.0', '19.0 | nan | nan', '10.0 | 10.0', '60.0 | 20.0 | 8.0', 'nan | 1.5', '60.0 | 600.0', '60.0 | 550.0', '37.0 | 1.0 | 1.0', '40.0 | 55.0', '3.0 | 57.0', '60.0 | 28.0', '33.7 | 67.5', '57.0 | nan', '50.0 | 7.5', 'nan | nan | 5.0', '100.0 | 0.5', '6.0 | 2.0', '27.0 | 70.0 | 27.0 | 70.0 | 27.0 | 70.0 | 27.0', '60.0 | 300.0', '50.0 | 270.0', '60.0 | 400.0', '610.0', '44.2 | 8.0', 'nan | 1000.0 | 1009.0', 'nan | nan | 1.3', 'nan | 0.5', '700.0 | 1970.0', '55.0 | 2.0', 'nan | 35.0', '70.0 | 5.0', '35.0', '60.0 | 125.0', '100.0 | 5.0', '30.0 | 10.0', '8.0 | 80.0', '40.0 | 3.0 | 3.0 | 1.0', '3.0 | 20.0 | 8.0', 'nan | 2.0', '50.0 | 60.0', '2.5', '60.0 | nan', '50.0 | 27.0', '21.0 | nan', 'nan | 350.0 | 150.0', '80.0 | 350.0', '20.0 | 20.0', '60.0 | 4.0', '25.0 | 10.0', '23.0', '35.0 | 10.0 | 1.0', '10.0 | 9.0', '30.0 | 230.0', '65.0 | 350.0', '100.0 | 35.0', '30.0 | 650.0', '550.0 | 2500.0', '54.0 | nan', 'nan | nan | 50.0', '40.0', '126.0 | nan', '230.0', '51.0 | 250.0', '60.0 | 420.0', '3.5', '28.0', '28.0 | 8.0', 'nan | 45.0 | nan', '50.0 | nan', 'nan | 300.0', '30.0 | 600.0 | 2500.0', 'nan | 400.0 | 500.0', '780.0', '48.8', 'nan | 2000.0', '0.8', '60.0 | 1300.0', 'nan | 1000.0 | 1003.0', '74.4', '60.0 | 7.0', '100.0 | 30.0', 'nan | 700.0 | 700.0', '27.0 | 80.0 | 27.0', '122.0', '300.0 | 2.0', '55.0 | 30.0', '181.0 | nan', '2.0', '2.0 | 0.0', '48.0 | 150.0', '130.0 | 10.0', '52.0 | 200.0', '6.0 | 10.0', '80.0 | 2100.0', '30.0 | 340.0', '50.0 | nan | 1200.0', '400.0 | 17.0', '60.0 | 105.0', 'nan | nan | 10.0', 'nan | 600.0 | 3000.0', '10.0 | 40.0 | nan', 'nan | 20.0 | 6.0', '44.0 | 200.0', '60.0 | 160.0', '0.5 | nan', '40.0 | 40.0', '80.0 | 1800.0', '64.7', '50.0 | nan | nan | 1200.0', '68.0', '30.0 | 172.0', '30.0 | 5.5', '50.0 | 250.0 | nan', '200.0', '20.0 | 370.0', '150.0 | nan', '80.0 | 8.0', '70.0 | 2.0', '30.0 | 264.0', '1.6 | 40.0 | 6.0', '100.0 | 40.0', 'nan | 500.0 | 2000.0', '30.0 | 258.0', '10.0 | 30.0', '80.0 | 2300.0', '40.0 | 450.0', '90.0 | 100.0', '15.0 | 20.0 | 8.0', '930.0', 'nan | 500.0 | 750.0', '25.0 | 20.0 | 5.0', '60.0 | 1000.0 | 1000.0', '20.0 | 180.0', '38.0', 'nan | 20.0 | 7.0', '40.0 | 350.0 | 1000.0', 'nan | 51.0', '270.0', '62.0', '170.0', 'nan | 12000.0', '99.4', '76.0 | 200.0', 'nan | 520.0', '130.0 | 20.0', '50.0 | 400.0 | 450.0', '10.1 | 3.0', '40.0 | 118.0', 'nan | nan | 167.0', '20.0 | 450.0', '45.0 | 0.5', 'nan | 20.0 | 7.5', '100.0 | 413.0', 'nan | 54.0', '8.0 | 100.0', '300.0', '190.0 | 40.0', 'nan | 500.0 | 600.0', '200.0 | 400.0', '30.0 | nan | 150.0', '450.0', '88.0', '60.0 | 9.0', '31.0 | 200.0', 'nan | 350.0', 'nan | 1700.0', '150.0 | 10.0', '5.8 | 40.0 | 6.0', '54.0 | 150.0', '33.0 | 1.0', '27.0', '66.0', 'nan | 4.0', '30.0 | 3.0', '10.0 | 35.0', '1200.0', '48.0 | 8.0', '17.5', 'nan | 2300.0', '1.7 | 40.0 | 6.0', '60.0 | 1000.0', '50.0 | 700.0 | 250.0', '60.0 | nan | nan', '2.0 | 25.0 | 6.0', '20.0 | nan | 1.0', '150.0 | 860.0', '800.0', '50.0 | 630.0', 'nan | 190.0', '48.0 | nan | 1.0', '55.0 | 0.5 | 30.0 | 0.5 | 0.5', '32.0', '1000.0 | 60.0 | 150.0', '227.5', '40.0 | 20.0', '20.0 | 150.0 | 1.0', '149.0', '40.0 | 390.0', '52.0 | 250.0', 'nan | 500.0 | 1400.0', '95.0 | nan', '100.0 | 3.3', '30.0 | 180.0', '120.0 | 365.0', '40.0 | 15.0', '20.0 | 60.0', '383.0', '25.0 | 187.0 | nan', 'nan | 500.0', 'nan | 38.0 | 1.0', '60.0 | 50.0 | 15.0', '11.0 | 150.0', '45.0 | 10.0', '96.0 | nan', '100.0 | 370.0', '40.0 | 20.0 | nan | 90.0', '40.0 | 400.0 | nan', '60.0 | 50.0 | 75.0', 'nan | 200.0 | nan', '40.0 | 175.0', '40.0 | 14.0', '70.0 | 50.0', '2.0 | 4.0 | 10.0', '60.0 | 2.0', '50.0 | 400.0 | 1500.0', '65.0 | 150.0', '30.0 | 500.0 | 1000.0', '25.0 | 300.0', '50.0 | 210.0', '50.0 | 120.0', '50.0 | 6.0', '41.7 | 8.0', '50.0 | 5.0', '80.0 | 40.0', '80.0 | 225.0', '400.0 | 200.0', '16.0', '80.0 | 250.0', '100.0 | 1.0', '10000.0', '30.0 | 450.0'])))

    additives_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    List of the dopants and additives that are in each layer of the ETL-stack
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- The layers must line up with the previous fields.
- If several dopants/additives, e.g. A and B, are present in one layer, list the dopants/additives in alphabetic order and separate them with semicolons, as in (A; B)
- If no dopants/additives, state that as “Undoped”
- If the doping situation is unknown, stat that as‘Unknown’
Example
Undoped | Li-TFSI
TiCl4
Nb
Undoped | Undoped | Undoped
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'Undoped | Li-FTSI', 'PFO | Unknown', 'Er; Yb', 'Unknown | B; F; PEI', 'Unknown | Zr', 'Al(NO3)3\xa0· 9H2O', 'PMo12 | Unknown | Unknown', 'Unknown | TiCl4; Mg', 'nan | Al', 'nan | Au-np', 'N-DPBI', 'Unknown | Li-TFSI; TiCl4', 'Unknown | Au-np; Li-TFSI', 'Bi2O2S-np', 'PEI', 'Unknown | CsBr', 'Unknown | Au@Ag-np; Li-TFSI | Unknown', 'N-Graphene', 'Unknown | I', '1-butyl-3-methylimidazolium tetrafluoroborate', 'Unknown | NaCo2O4', 'H2PtCl6', 'Polystyrene', 'CH3NH3I', 'CsAc', 'UV', 'Unknown | CsI', 'Unknown | N', 'Unknown | Oleic acid', 'Unknown | Ruthenium', 'N-Graphene-nanosheets | Unknown', 'Unknown | Ag@SiO2 | Unknown', 'Unknown | NaYF4:Yb3:Er:@SiO2-np | Unknown', 'Unknown | Eu', 'Unknown | N; Ta', 'PMMA | Unknown', 'Y', 'Unknown | BF4', 'Undoped | Undoped', 'Galliumnitrate\xa0hydrate', 'PFNOX', 'bis-C60', 'Ta', 'Eu(NO3)3·6H2O', 'Acetylacetone', 'Ni', 'Al(NO3)3\xa0· 9H2O; La(NO3)3\xa0· 6H2O', 'Ga', 'Pyridine | Undoped', 'Ag', 'Unknown | NaYF4:Yb:Er-np', 'Mg', 'Unknown | Zn', 'Cs', 'Unknown | FeN3O9', 'Unknown | Ag@SiO2', 'ITIC | Undoped', 'InCl3', 'Unknown | TiO2-nw', 'In2O3', 'Unknown | Zn0.5Cd0.5S-np', 'DBU', 'Undoped | Mg | Undoped | Undoped', 'Unknown | TiCl4; Ethyl cellulose', 'D35', 'rGraphene oxide', 'Unknown | Ag-np', 'nan | MAI', 'nan | FK209', 'Urea', 'nan | Thiourea', 'EDTA', 'Tetraisopropil titanate butanol | TiCl4', '(RuCp*mes)2 | Undoped', 'Unknown | N-DBPI', 'TiCl4 | Nb', 'Nb2O5', 'Unknown | SDBAC', 'Ethanolamine', 'CoSe', 'Unknown | ZnGa2O4:Eu(III)', '1H molecule | Undoped', 'Ti', 'nan | Au-nw', 'CF4', 'AlCl3', 'Hydrogen | Undoped', 'Li-TFSI; Mg(TFSI)2', 'Unknown | Pluronic P-123', 'Al', 'Unknown | TiCl4 | Unknown', 'Ga2O3', 'Sb | Unknown', 'NaCl | Unknown', 'Al | Undoped', 'Al | nan', 'Unknown | Mg', 'Unknown | Er', 'DMOPA | Unknown', 'Dopamine', 'Undoped | P', 'Glycine', 'Unknown | Au@SiO2-np', 'Er', 'Phosphorene nanocomposites', 'ethanolamine', 'Unknown | NaYF4:Yb3:E3', 'oTb', 'Unknown | Fe', 'oTb | Unknown', 'Unknown | Graphene oxide', 'Yttrium', 'Graphene oxide | Unknown', 'F', 'Unknown | Zn0.25Cd0.75S-np', 'Unknown | EA | Unknown', 'Unknown | Au@TiO2 NPs', 'Unknown | Unknown | Cu', 'Undoped | p-Toluenesulfonic acid', 'SnCl2', 'Unknown | Nb', 'TMAH', 'tert-butanol', 'BF4', 'CF3NaO2S', 'Unknown | ZnCdS-np', 'Nb | TiCl4', 'Unknown | TPFPB; LiClO4', 'Unknown | TPFPB', 'N:Graphene-oxide', 'Unknown | Terpineol', 'Unknown | Unknown | Li-TFSI', 'Cs2CO3', 'Unknown | Au@Ag-np; Li-TFSI', 'Graphene oxide | Graphene oxide', 'Li-TFSI; Mg-TFSI | Li-TFSI', 'Li', 'La(NO3)3\xa0· 6H2O', '2,2,2-trifluoroethanol', 'Urea | Unknown', 'RGraphene oxide | RGraphene oxide', 'Unknown | PEG', 'Graphene; TiCl4 | Graphene', 'NbCl5', 'Cl', 'DPM2; OC10H21', 'Triton X-100', 'Li-TFSI; TiCl4', 'TiCl4 | TiCl4', 'TiCl4 | Decamethylcobaltocene', 'Unknown | SiW12', 'AgInS2-QD', 'Unknown | Li-TFSI | Unknown', 'Graphdiyne', 'Oleamide', 'Ti(acac)2', 'nan | Li-TFSI', 'F8BT | Unknown', 'Phen-I', 'Unknown | Graphene oxide | Unknown', 'Unknown | Mg; Er', 'Unknown | Ag-nw', 'CNT', 'Unknown | Li-TFSI', 'Bi | nan', 'TBABF4 | Unknown', 'Y2O3', 'Undoped | Undoped | Cu', 'Unknown | rGraphene oxide', 'nan | Ga', 'Yb', 'F | F', 'Unknown | H20', 'Chlorine', 'Ta | Undoped', 'Unknown | H', 'Unknown | SnCl2', 'DMOAP | Unknown', 'Unknown | Li; Er; Yb', 'TiCl4 | Ag-np', 'Ionic liquid', 'Unknown | NbCl5', 'nan | AuAg-np', 'nan | TiCl4', 'Unknown | Ge-np', 'Li-TFSI', 'Unknown | Al | Unknown', 'Unknown | BaTiO3', 'Fe | nan', 'EA', 'Unknown | N-DPBI', 'HCl', 'TAA', 'Unknown | Au@SiO2', 'Graphene-nanosheets | Unknown', 'Unknown | Au@Pt@Au-np | Unknown', 'TiCl4 | Undoped | Undoped', 'Er; Mg', 'DIO', 'Li-TFSI | nan', 'NaCl', 'Unknown | Triethylamine; HCl | Unknown', 'LiCl2; PEG', 'Cd; Y', 'Unknown | CeO2', 'SWCNTs | SWCNTs', 'Pluronic P123 surfactant', 'TiCl4 | Na-TFSI', 'DMBI', 'CoCl2', 'Unknown | Co-TFSI', 'Ga(acac)3 | Ga(acac)3', 'DPM; OE', 'Unknown | Triton 100-X', 'KCl', 'KOH', 'Potassium O-hexyl xanthate', '2-CP', 'Ru | Unknown', 'SnOCl2', 'Al(NO3)3; Ethanolamine', 'DMOAP | Undoped', 'Unknown | SrO', 'Li2CO3', 'Ru', 'BaSnO3', 'Fe', 'Compound 2 | Unknown', 'Zn', 'Zr | N', 'Unknown | Unknown | Unknown | MoO3', 'Unknown | HI', 'Unknown | TiCl4 | Tm; Yb', 'Unknown | Al; In', 'Unknown | TiO4', 'Unknown | Li-TSFI', 'CTAB | Unknown', 'Unknown | Ta', 'Unknown | Ethylene cellulose; TiCl4', 'Phosphotungstic acid; WCl6', 'Undoped', 'PNDI-2T | Undoped', 'Unknown | Yb:Er', 'TiCl4 | Unknown', 'Mxene | Mxene', 'Nb; TiCl4', 'NACl', 'nan | CsBr', 'Unknown | Undoped', 'Ethyl cellulose | Unknown', 'Glucose', 'Unknown | Unknown | Nb', 'Unknown | LiFTSI', 'Sn | Unknown', 'SnCl2; MercaptoPropionic acid; Urea', 'Al | Unknown', 'HCl | Unknown', 'TOPD', 'Unknown | Li-TFSI; TiCl4 | Unknown', 'Tantalum(V) ethoxide', 'Acetic Acid', 'MAI | Unknown', 'IL-BF4', 'Undoped | AlCl', 'Unknown | La', 'B-TiO2', 'CNT, DMSO', 'RuCl3', 'Unknown | InCl3 | Unknown', 'rGraphene oxide | Unknown', 'Unknown | TiCl4; SWCNTs', 'Unknown | Graphene', 'Unknown | NaYF4:Yb:Tm-np', 'TiCl4', 'Undoped | Li-TFSI', 'Carbon-np', 'Unknown | Li', 'In | Unknown | Unknown', 'Unknown | Unknown | NaYbF4:Ho-np', 'nan | TAA', 'Mg | Unknown', 'Unknown', 'Samarium', 'Unknown | Au-np; TiCl4', 'TiCl4 | Undoped', 'nan | Nb', 'TiCl4 | nan', 'K', 'nan | Ag', 'Unknown | YCl3', 'Graphene', 'Unknown | SWCNTs', 'Undoped | W', 'Yb:Er', 'Unknown | Ag', 'Pyridine | Unknown', 'In', 'Unknown | Ho; Yb; Mg', 'N; PEI', 'Unknown | ZnGa2O4-np', 'Graphene | Graphene', 'Nb', 'H2O', 'PEIE', 'Unknown | 2,6-Py | Unknown', 'Unknown | Cl', 'Ga | Undoped', 'HMB', 'TBAPF6', 'Ethanolamine | Unknown', 'Unknown | Sb | Unknown', '4,4′-BiPy | nan', 'W2(hpp)4', 'N-Graphene | Unknown', 'DBU | Unknown', 'La', 'Unknown | F127', 'Unknown | Yb', 'Unknown | CTAB', 'N2H8S', 'Unknown | Zn0.75Cd0.25S-np', 'Unknown | TiCl4', 'TBAB', 'PF6', 'Unknown | SnOCl2', 'BIZ | Undoped', '2H molecule | Undoped', 'Al2O3', 'LiCl', 'MoCl5', 'PMMA', 'Li-TFSI; Mg(TFSI)2 | Li-TFSI', 'F; Sn', 'N', 'Gd', 'TiCl4 | Li-TFSI', 'Co', 'Nb(OCH2CH3)5', 'n-DMBI', 'Unknown | CeO2:Eu', 'TiCl4 | polystyrene', 'Unknown | B', 'V | Undoped', 'SnCl4', 'TBABF4', 'Unknown | Ba(OH)2', 'TiAcAc', 'Unknown | AlCl3:NH3', 'Graphene-QDs', 'Titanium acetylacetonate', 'Unknown | In', '2,6-Py | Unknown', 'Bphen', 'Unknown | Cs', 'Guanidinium chloride', 'N-DMBI | Unknown', 'Zr', 'Unknown | Ni | Unknown', 'Unknown | Carbon-np', 'ZnCl2', 'In | Unknown', 'Oleic Acid', 'C60-substituted catechol | C60-substituted catechol', 'TiCl4 | Unknown | Unknown', 'CdS', 'Undoped | TiCl4', 'Stearic acid; EDA', 'N2', 'Unknown | TAA', '2,2′-BiPy | nan', 'Undoped | Acetylacetone; Triton X-100', 'Cd', 'Carbon-QDs', 'W', 'Bi | Unknown', 'Sn', 'Unknown | F', 'Undoped | TiCl4 | TiCl4', 'Unknown | Sn', 'Unknown | PVC-g-POEM', 'Unknown | rGraphene oxide; Li-TFSI', 'Undoped | Undoped | Undoped', '2D graphene', 'Mxene | Mxene | Unknown', 'Graphdiyne | Graphdiyne', 'NH4Cl', 'Nb | Unknown', 'Na2S', 'AgNO3 | Undoped | Undoped', 'TiCl4 | K-TFSI', 'MAI | Unknown | Unknown', 'TaCl', 'Unknown | In | Unknown', 'Unknown | Polystyrene', 'TaCl5', 'Unknown | DMBI', 'Fe(NO3)3 | Unknown', 'Mg | Undoped | Undoped', 'Unknown | Al', 'PS', 'IZ | Undoped', 'CTAB', 'NH4F', 'Unknown | HCl', 'CeOx; TiCl4 | Unknown', 'TiAc2', 'Unknown | Sb', 'Unknown | Li; Mg | Unknown', 'Unknown | Li; Ho; Yb', 'Triethylamine | Unknown', 'Sb', 'NOBF4', 'Unknown | B; F', 'Nb | Undoped', 'Unknown | Li-acetat', 'P123 | Unknown', 'Unknown | Li-FTSI', 'Unknown | InCl3', 'Na2CO3', 'Ag; In | Undoped', 'K2CO3', 'nan | Cs2CO3', 'DMBI | Unknown', 'DPM2; OE2', 'Unknown | Unknown | Unknown | Co2O3', 'Unknown | PAAb-PEO', 'Unknown | Er; Yb', 'Ti3C2', 'titanium diisopropoxide bis(acetylacetonate)', 'Unknown | PEI', 'Unknown | NaYF4:Yb3:Er-np | Unknown', 'TiCl4 | Cs-TFSI', 'Unknown | Sr', 'Unknown | Unknown | TiCl4', 'CdCl2', 'Unknown | Unknown | Unknown | NiO', 'Ti(acac)2 | TiCl4', 'Undoped | nan', 'rGS', 'DMOAP', 'C60-substituted catechol', 'Unknown | Unknown | Unknown | CuO', 'ClGD | Unknown', 'Unknown | Li-TFSI; TBP', 'Mo', 'PFNOX; Polystyrene', 'Li2SiO3'])))

    additives_concentrations = Quantity(
        type=str,
        shape=[],
        description="""
    The concentration of the dopants/additives.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- If more than one dopant/additive in the layer, e.g. A and B, separate the concentration for each dopant/additive with semicolons, as in (A; B)
- For each dopant/additive in the layer, state the concentration.
- The order of the dopants/additives must be the same as in the previous filed.
- For layers with no dopants/additives, state this as ‘none’
- When concentrations are unknown, state that as ‘nan’
- Concentrations can be stated in different units suited for different situations. Therefore, specify the unit used.
- The preferred way to state the concentration of a dopant/additive is to refer to the amount in the final product, i.e. the material in the layer. When possible, use on the preferred units
o wt%, mol%, vol%, ppt, ppm, ppb
- When the concentration of the dopant/additive in the final product is unknown, but where the concentration of the dopant/additive in the solution is known, state that concentration instead. When possible, use on the preferred units
o M, mM, molal; g/ml, mg/ml, µg/ml
- For values with uncertainties, state the best estimate, e.g write 4 wt% and not 3-5 wt%.
Example
4 wt%
5 vol%; nan | 10 mg/ml
0.3 mol% | 2 mol%; 0.2 wt% | 0.3 M
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '4 % | nan', 'nan | 0.04 | 0.04', '1', '2', 'nan | 0.5 mg/ml', '0.005', '5 vol%', '3 mol%', '50 vol%', 'nan | 12 %', 'nan | 0.5 %', '0.2', '0.1 mol%', '0.005 M', '1 mol%', '0 | 50 ppm', '100 vol%', '0.33', '0.01', '1.0 mol%', '0.025 M | nan', '0.003', '0.1', '0.66', '0.4 % | nan', '2.5 vol%', '0.05 % | nan', '0.07', '40 mM | nan', '10 mol%', '0.025 M', '0.15 M | 20 wt% | 0.5 mg/ml', '0.05', '2 mol%', 'nan | 7.5 % | nan | nan', '0.15', '0.2 mM/ml', '0.015', '0.3 mM', '2 % | nan', '1.2 mg/ml', '0.5 % | nan', '1.5 vol%', 'nan | 1 %', '3.0 mol%', '0.5', '75 vol%', '6 wt%', '0.5 %; 0.5 %', '0.4 mg/ml', '0.15 M | nan', 'nan | 0.04', '0 | 100 ppm', '0.355 vol%', '0.15 M | 20 wt% | 1 mg/ml', '0.02', '0.007', '0.2 wt%', '2.4 vol%', '0.6 M', '7.5 % | nan | nan', '50 mM', '6.25 wt% | nan', '0.1 mM/ml', '0.15 mM', '0.6 mM', 'nan | nan', '0.4 mM/ml', 'nan | 0.1 M', '0.04 M', '0.001', 'nan | 6 %', '2.0 mg/ml', '0.15 M | 20 wt% | 2 mg/ml', 'nan | 9 %', '0.1 wt%', 'nan | 3 %', '12.5 wt% | nan', '0.5 mol%', '3 % | nan', '0 | 10000 ppm', '20 mg/ml | 0.5 mg/ml', '0.01 M', '5 % | nan', '0.8 mg/ml', '2.5 wt% | nan', '5 mol%', '0.5 wt%', '1.6 mg/ml', ' undoped', '1.5 wt%', '1 % | nan', '100 mM | nan | nan', '1 wt%', '0.15 M | 20 wt% | 4 mg/ml', '0.45 mM', 'nan | 100 mg/ml', '0.3 mM/ml', '3 wt%', 'nan | nan | nan', 'nan | 5 %', '0.0025', '5 wt%', '25 vol%', '0 | 1000 ppm', '0.03'])))

    deposition_procedure = Quantity(
        type=str,
        shape=[],
        description="""
    The deposition procedures for the ETL stack.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate them by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- Thermal annealing is generally not considered as an individual reaction step. The philosophy behind this is that every deposition step has a thermal history, which is specified in a separate filed. In exceptional cases with thermal annealing procedures clearly disconnected from other procedures, state ‘Thermal annealing’ as a separate reaction step.
- Please read the instructions under “Perovskite. Deposition. Procedure” for descriptions and distinctions between common deposition procedures and how they should be labelled for consistency in the database.
Example
Spin-coating
Spin-coating | Spin-coating
Spray-pyrolys | Spin-coating
Evaporation | Evaporation
Spin-coating | Evaporation
CBD
Spray-pyrolys
Spin-coating | Evaporation | Evaporation
Spray-pyrolys >> CBD | Spin-coating >> CBD
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=sorted(['Spin-coating | Spin-coating >> Spin-coating', 'Spin-coating | Spin-coating >> CBD', 'ALD | ALD | Spin-coating', 'Spin-coating | Spin-coating', 'Magnetron sputtering | Spin-coating | Spin-coating', 'Sputtering', 'Electrospraying | Hydrothermal | Spin-coating', 'Evaporation | CVD', 'Evaporation | Co-evaporation', 'Spin-coating | Sputtering', 'Sputtering | Spray-pyrolys | Spin-coating', 'Electrodeposition | Spin-coating', 'DC Magnetron Sputtering | Electrochemical anodization', 'Brush painting | Evaporation', 'Spray-pyrolys | Screen printing | Spray-coating | Screen printing', 'Electrochemical anodization', 'Spin-coating >> Spin-coating >> Spin-coating', 'Photo-thermal CVD', 'Spray-pyrolys | Electrodeposition | Screen printing | Screen printing', 'Hydrothermal | Hydrothermal | Hydrothermal', 'Spin-coating | Spin-coating >> CBD >> Rinsing', 'ALD | Spray-pyrolys | Spin-coating', 'Spin-coating | Spin-coating >> Spin-coating | Spin-coating >> CBD', 'Comersial | Spin-coating', 'Spray-pyrolys | Screen printing | CBD', 'Spray-pyrolys | PVD', 'Spin-coating | Lithography', 'Sputtering >> CBD >> CBD', 'Evaporation | Evaporation | ALD | ALD', 'Spin-coating | Dipp-coating', 'Spin-coating | Spin-coating | Spin-coating', 'Spin-coating | Electrospraying', 'Aerosol-assisted CVD | Spin-coating', 'CBD | Screen printing | Dipp-coating', 'Dipp-coating | Doctor blading | Doctor blading', 'Spray-pyrolys | Spin-coating >> Hydrothermal >> Ion exchange >> CBD', 'Electrodeposition | Screen printing', 'E-beam evaporation | Spin-coating', 'PVD', 'Condensation | Spin-coating', 'Evaporation | ALD | ALD', 'Spray-coating | Spin-coating | Spin-coating', 'Inkjet printing | Evaporation', 'Temperature gradient solid-phase sintering', 'Unknown | Screen printing', 'Spray-pyrolys', 'Spin-coating >> CBD | Spin-coating', 'Spin-coating | ALD | Evaporation', 'Drop-infiltration', 'Solution combustion | Spin-coating', 'ALD | Spin-coating', 'CVD | CVD | Spin-coating', 'CVD | Doctor blading', 'Electrospraying | Electrospraying', 'Screen printing', 'Spin-coating | Ultrasonic spray', 'Meniscus coating | Evaporation', 'Spin-coating | E-beam evaporation', 'Spin-coating >> Hydrothermal', 'Evaporation | CVD >> ALD', 'Spray-pyrolys | Spin-coating >> CBD | Spin-coating', 'Doctor blading | Dipp-coating', 'CBD >> Screen printing >> CBD | Screen printing | Screen printing', 'Sputtering | Screen printing | Screen printing', 'Spin-coating | CBD | Spin-coating', 'Spin-coating | Lithography | Spin-coating', 'Spin-coating | Evaporation | Evaporation | Evaporation', 'Spray-coating | Solvothermal', 'Spin-coating >> Hydrothermal | Spin-coating', 'Spin-coating | Spin-coating | Evaporation', 'Sputtering | E-beam evaporation', 'Doctor blading | Evaporation', 'Spray-pyrolys | Screen printing | Spray-pyrolys | Screen printing', 'Dipp-coating | Spin-coating >> Plasma treatment', 'E-beam evaporation | E-beam evaporation', 'Dipp-coating | Spin-coating', 'CVD | Spin-coating', 'CBD | Spin-coating >> CBD', 'RF sputtering | Spin-coating', 'Spin-coating | PVD', 'Spray-pyrolys | Spray-coating', 'Spin-coating | ALD', 'Spin-coating | Doctor blading | Doctor blading', 'Spin-coating | Spin-coating | Spin-coating | Spin-coating | Spin-coating', 'RF Magnetron sputtering', 'Spray-pyrolys | Spin-coating >> Spin-coating', 'Thermal oxidation', 'Unknown | Screen printing | Screen printing', 'Spin-coating | Evaporation >> Electrohemical anodization >> Etching', 'Spin-coating | Hydrothermal | Doctor blading', 'Roller coating', 'Spray-pyrolys | Spin-coating | Spin-coating', 'Evaporation | Evaporation | CVD', 'Spray-pyrolys | Screen printing', 'Unknown | Unknown', 'Slot-die coating', 'Spin-coating >> CBD', 'Spin-coating | Evaporation', 'Ultrasonic spray', 'Dipp-coating | Spin-coating | Spin-coating', 'Spin-coating | Electrodeposition', 'Spin-coating | Spin-coating | Hydrothermal', 'Sputtering >> Spin-coating | Spin-coating', 'Sputtering >> Oxidation | Spin-coating', 'Ultrasonic spray pyrolysis', 'Spin-coating | Spin-coating | Spin-coating | Spin-coating', 'Spin-coating | Slot-die coating', 'Spin-coating | Hydrothermal', 'SILAR', 'Inkjet printing', 'Spin-coating | Spin-coating >> Dipp-coating', 'Condensation | Evaporation | Evaporation', 'Spin-coating | Spin-coating | SILAR', 'Evaporation | Evaporation', 'Spin-coating | RF sputtering', 'Spin-coating | Sputtering >> Hydrothermal >> ALD', 'Spin-coating | Doctor blading', 'ALD | Spin-coating | Hydrolysis', 'Spin-coating | Air brush spray', 'ALD | Hydrolysis', 'CBD | Spin-coating | Spin-coating', 'Hydrothermal | Spin-coating', 'Spin-coating | Spin-coating | Spin-coating | Spin-coating | Spin-coating | Spin-coating | Spin-coating', 'Spray-coating | Evaporation', 'Dipp-coating | Hydrothermal | CBD', 'Electrochemical anodization | CBD', 'Sputtering | Hydrothermal | ALD', 'Dipp-coating | Hydrothermal', 'Evaporation | Sputtering', 'Dipp-coating', 'Spin-coating | Hydrolysis', 'Spin-coating | SILAR', 'Oxidation | Dipp-coating', 'DC Magnetron Sputtering | Spin-coating', 'ALD | Flame aerosol | ALD', 'CBD | Hydrothermal', 'Spin-coating | Dipp-coating | Spin-coating', 'Spin-coating | Spin-coating | Evaporation | Evaporation | Evaporation', 'ALD | Evaporation', 'Meniscus-coating', 'Spin-coating | Solvothermal', 'Magnetron sputtering | Hydrothermal', 'ALD | Screen printing', 'Spray-pyrolys | Evaporation >> Electrochemical anodization', 'Spin-coating | Magnetron sputtering >> Oxdation', 'Hydrothermal >> Solvothermal', 'Electrochemical anodization | Electrochemical anodization', 'Magnetron sputtering', 'Substrate vibration assisted dropcasting', 'RF Magnetron Sputtering', 'Spin-coating | Hydrothermal >> Solvothermal etching', 'Chemical etching >> Thermal oxidation', 'Sputtering >> Electrochemical anodization | Spin-coating', 'Spin-coating | Electrospinning | Spin-coating', 'Spray-pyrolys | Doctor blading', 'Doctor blading | Spin-coating | Spin-coating', 'Spin-coating | Spin-coating | SILAR method', 'Evaporation | Evaporation | CVD | CVD', 'Spin-coating | Hydrothermal >> Spin-coating', 'E-beam evaporation | Spin-coating | Spin-coating', 'Spray-pyrolys | Spin-coating | Spray-pyrolys', 'RF sputtering | CBD', 'Reactive sputtering', 'E-beam evaporation >> CVD | ALD', 'Spray-pyrolys | Screen printnig', 'Spin-coating | Dropcasting', 'Spray-pyrolys | Evaporation', 'Spray-pyrolys >> CBD', 'DC Sputtering | Spin-coating', 'Spin-coating | Sputtering | Spin-coating', 'CBD | Spin-coating | Dipp-coating', 'Spin-coating | Spin-coating | RF sputtering', 'CVD >> ALD', 'Spray-pyrolys | Spin-coating >> CBD', 'Spray-pyrolys | Spin-coating | Screen printing', 'RF plasma sputtering | Spin-coating', 'Sputtering | Evaporation', 'Slot-die coating | Slot-die coating', 'Doctor blading | Hydrothermal', 'Spin-coating | Spin-coating | Spin-coating | Dipp-coating', 'Spin-coating >> litography', 'Spin-coating', 'ALD | Screen printing | Screen printing', 'Sputtering | Spin-coating | Spin-coating', 'Spray-coating | Spray-pyrolys | Spin-coating', 'Spray-coating', 'Electrospraying | Hydrothermal', 'Spin-coating | Spin-coating | Doctor blading', 'Spin-coating >> Spin-coating >> Spin-coating | Spin-coating', 'Screen printing | Screen printing | Screen printing | Screen printing', 'Co-evaporation | Evaporation', 'Screen printing | Screen printing', 'Spin-coating | Spin-coating >> CBD | Spin-coating', 'Spin-coating | Spin-coating | Screen printing', 'Spray-pyrolys | Blow-drying', 'Screen printing | Screen printing | Screen printing', 'Spray-coating | Spray-coating', 'Spin-coating >> Spin-coating | Spin-coating', 'Spin-coating | Screen printing >> CBD', 'Unknown | Hydrothermal', 'Hydrothermal | CBD', 'Spin-coating | Spin-coating | Dipp-coating', 'Solution combustion', 'CBD | Spin-coating', 'Spin-coating | Evaporation >> Anodisation >> Oxidation >> Etching', 'CBD | Hydrothermal | Dipp-coating', 'Electrodeposition | Electrodeposition', 'Spray-pyrolys | Screen printing | Screen printing | Dipp ccoating', 'Spray-pyrolys | Hydrothermal', 'Spray-pyrolys | Dropcasting', 'Spin-coating | Unknown', 'Spin-coating >> Evaporation | Evaporation', 'Spin-coating | Lamination', 'Spin-coating | E-beam evaporation >> Electrochemical anodization', 'Spray-pyrolys >> Hydrothermal | PVD-OAD', 'Sputtering | Dipp-coating', 'Spray-pyrolys | PVD | PVD | PVD', 'CBD >> Screen printing >> CBD | Screen printing', 'Dropcasting | Spin-coating | Spin-coating', 'Spin-coating | Spray-coating', 'Sputtering | Sputtering', 'Spin-coating | Evaporation | Spin-coating | CBD', 'Pulsed laser deposition | Spin-coating', 'Electrodeposition | CBD', 'Spray-coating | Spin-coating', 'Photo-thermal CVD >> Spin-coating', 'Oxygen plasma treatment', 'Spin-coating | Spin-coating | Unknown | Unknown', 'Spin-coating | Hydrothermal | LBLAR', 'Lamination', 'Dipp-coating | Spin-coating | Spin-coating | CBD', 'Evaporation | Evaporation | ALD', 'Evaporation | Evaporation | Evaporation', 'Spin-coating | Unknown | Unknown', 'Magnetron sputtering | Hydrothermal | ALD', 'Dipp-coating >> CBD', 'Spray-pyrolys | Screen printing | Spin-coating', 'Spray-pyrolys | ALD', 'Hydrothermal >> Dipp-coating', 'Evaporation', 'RF Magnetron sputtering | RF Magnetron sputtering', 'Spin-coating | Evaporation | Spin-coating', 'Unknown', 'Electrospraying', 'Spin-coating | RF Magnetron Sputtering', 'Sputering', 'CVD', 'Spin-coating | Spin-coating >> Hydrothermal', 'Slot-die coating | Spin-coating', 'Spin-coating >> Spin-coating >> CBD', 'Evaporation | Unknown', 'Spin-coating | Hydrothermal | Dipp-coating', 'Doctor blading', 'CBD | CBD', 'Spin-coating | Hydrothermal | Spin-coating | Spin-coating', 'Sputtering | Spin-coating', 'Spray-pyrolys >> Hydrothermal | Spin-coating', 'Spin-coating | Electrospraying | Spin-coating', 'Dipp-coating | Screen printing | Screen printing', 'Hydrothermal | Dipp-coating', 'Electrospinning', 'Spin-coating | Spin-coating | Spin-coating | ALD', 'Electrospraying | Hydrothermal | Hydorthermal', 'Spin-coating | CBD', 'Spray-pyrolys | Screen printing | Screen printing | Screen printing', 'DC Magnetron Sputtering', 'CVD | CVD | Evaporation', 'Electrodeposition | Spin-coating >> CBD', 'Hydrothermal', 'Electrodeposition', 'Spray-pyrolys | Spin-coating', 'Spin-coating | Hydrothermal | SILAR', 'Dipp-coating | Evaporation', 'DC Sputtering >> Electrochemical anodization', 'ALD | Spin-coating | Spin-coating', 'Electrospraying | Electrospraying | Spin-coating', 'Spin-coating | Electrodeposition | Spin-coating', 'Electrospraying | Spin-coating', 'CVD | CVD', 'CBD | Evaporation', 'Spin-coating >> Spin-coating', 'Spray-pyrolys | Electrospinning', 'Sputtering | CBD', 'Electrodeposition | Hydrothermal', 'Dipp-coating | Dipp-coating', 'CBD | Screen printing', 'Spin-coating | Hydrothermal | Sputtering', 'Spin-coating >> Solvent annealing', 'Spin-coating | Electrodeposition >> CBD', 'Evaporation | Spin-coating', 'Sputtering | Sputtering | Sputtering', 'Magnetron sputtering >> Electrochemical anodization | Electrodeposition', 'Spray-pyrolys | Spin-coating >> Dipp-coating', 'Hydrolysis', 'Hydrothermal | Spin-coating | CBD', 'Spray-pyrolys | ALD | Spin-coating', 'Screen printing | Spin-coating', 'Evaporation | ALD', 'Spin-coating >> Spin-coating >> Spin-coating | Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating >> Spin-coating', 'Spray-pyrolys | Spray-pyrolys', 'Spin-coating >> CBD >> Rinsing >> Rinsing | Spin-coating', 'RF sputtering', 'Sputtering | Pulsed laser deposition | Hydrothermal | Spin-coating', 'Spray-pyrolys | PVD | PVD', 'CBD | Screen printing | Screen printing', 'Spin-coating | Hydrothermal | CBD', 'Evaporation >> Oxidation | Spin-coating', 'Unknown | Unknown | Unknown', 'Spin-coating | Hydrothermal | Spin-coating', 'Spin-coating | Spin-coating >> Hydrothermal | Spin-coating', 'Spray-pyrolys | Electrospraying', 'Sputtering >> Electrochemical anodization', 'DC Reactive Magnetron Sputtering', 'Spin-coating | Spin-coating | Sputtering', 'Spin-coating | Spray-pyrolys', 'Frequency Magnetron Sputteirng', 'ALD | Microwave hydrothermal', 'Spin-coating | Screen printing', 'Magnetron sputtering | Spin-coating', 'Lamination | Spin-coating', 'CVD | Spray-pyrolys', 'Spray-pyrolys | Screen printnig | Screen printing', 'Spray-pyrolys | Screen printing | Screen printing', 'Spin-coating | Spin-coating | Evaporation | Evaporation | Evaporation | Evaporation', 'ALD | Magnetron sputtering | ALD | ALD', 'Spray-pyrolys | Screen printing | Evaporation | Screen printing', 'Solvothermal', 'Spray-pyrolys >> CBD | Spin-coating', 'E-beam evaporation | CVD', 'Spin-coating >> CBD | Evaporation', 'Doctor blading | Spin-coating | Dipp-coating', 'Slot-die coating | Evaporation', 'Spray-pyrolys | Spin-coating | Dipp-coating', 'CBD', 'Spin-coating | Electrospinning', 'Spray-pyrolys | CVD', 'E-beam evaporation >> CVD', 'CBD >> Rinsing >> Rinsing', 'Magnetron sputtering >> Electrochemical anodization', 'Unknown | Unknown | Spin-coating', 'ALD | Flame aerosol', 'Sputtering | Electrodeposition | Spin-coating', 'Sputtering | Hydrothermal', 'Spin-coating | Hydrothermal | Evaporation', 'E-beam evaporation', 'Langmuir-Blodgett deposition', 'Unknown | Spin-coating', 'CBD | Hydrothermal >> Etching', 'Spray-pyrolys | Inkjet-Printed', 'Spin-coating | Spin-coating | CBD', 'Dropcasting', 'Hydrothermal | Hydrothermal', 'Pulsed laser deposition', 'CBD | Inkjet printing | Inkjet printing', 'Spin-coating | Spin-coating | Evaporation | Evaporation', 'Spin-coating | Hydrothermal | Hydrothermal', 'Spray-pyrolys | Ultrasonic spray', 'Unknown | CVD', 'Spin-coating | Evaporation | Spin-coating | Spin-coating', 'Spin-coating | Spin-coating | ALD', 'Evaporation | Evaporation | Spin-coating | ALD | ALD', 'Spin-coating | Screen printing | Screen printing', 'Doctor blading | Doctor blading', 'Spin-coating | Evaporation | Evaporation', 'Spray-pyrolys >> Hydrothermal', 'Spin-coating | Transfer', 'Spin-coating | Hydrothermal | ALD', 'ALD']))))

    deposition_aggregation_state_of_reactants = Quantity(
        type=str,
        shape=[],
        description="""
    The physical state of the reactants
- The three basic categories are Solid/Liquid/Gas
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the aggregation state associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- Most cases are clear cut, e.g. spin-coating involves species in solution and evaporation involves species in gas phase. For less clear-cut cases, consider where the reaction really is happening as in:
o For a spray-coating procedure, it is droplets of liquid that enters the substrate (thus a liquid phase reaction)
o For sputtering and thermal evaporation, it is species in gas phase that reaches the substrate (thus a gas phase reaction)
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Liquid
Gas | Liquid
Liquid | Liquid >> Liquid
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Liquid | Liquid', 'Liquid | Liquid >> Liquid | Liquid >> Liquid', 'Liquid >> Liquid >> Liquid >> Liquid | Liquid', 'Gas | Liquid | Liquid', 'Liquid | Liquid | Liquid | Liquid', 'Liquid >> Liquid >> Liquid | Liquid', 'Gas', 'Liquid | Liquid >> Liquid', 'Liquid >> Liquid >> Liquid', 'Gas | Gas', 'Liquid | Gas', 'Gas | Gas | Gas', 'Unknown', 'Liquid | Liquid | Liquid', 'Liquid >> Liquid', 'Gas | Gas >> Gas', 'Gas >> Gas', 'Liquid | Liquid | Gas', 'Liquid', 'Liquid | Gas | Gas', 'Liquid >> Liquid | Liquid', 'Liquid | Gas | Liquid', 'Liquid | Liquid >> Liquid >> Liquid', 'Unknown | Gas | Gas', 'Gas >> Liquid | Liquid', 'Solid | Solid', 'Gas >> Liquid >> Liquid', 'Gas | Liquid'])))

    deposition_synthesis_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The synthesis atmosphere
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the atmospheres associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- If the synthesis atmosphere is a mixture of different gases, e.g. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
N2
Vacuum | N2
Air | Ar; H2O >> Ar
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['N2 | Vacuum', 'N2', 'Air | Air >> Air', 'Air >> Air | Air', 'Air >> Air >> Air', 'Unknown', 'Air | N2', 'Vacuum | Vacuum | Vacuum', 'Vacuum >> Vacuum >> Unknown', 'N2 | N2 | N2', 'N2 | > N2', 'N2 | N2', 'Vacuum | Vacuum >> Vacuum', 'Ar | Ar', 'Ar', 'N2 | Air', 'Air | Air | Air', 'Air | Vacuum', 'N2 | N2 | Vacuum', 'Air | Air', 'Ar; O2 | Air', 'Vacuum | Air', 'Air | Vacuum | Vacuum', 'Air | Air >> Air | Air >> Air', 'Air | Air | Air | Air', 'Dry air', 'Vacuum | Vacuum', 'Air', 'Dry air | Dry air', 'Vacuum', 'Air | Ar', 'Ar; O2', 'Vacuum >> Vacuum', 'Dry air | Vacuum', 'Air >> Air', 'Air; O2 | Air', 'Vacuum | N2', 'N2 | Vacuum | Vacuum'])))

    deposition_synthesis_atmosphere_pressure_total = Quantity(
        type=str,
        shape=[],
        description="""
    The total pressure during each synthesis step
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the pressures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- Pressures can be stated in different units suited for different situations. Therefore, specify the unit. The preferred units are:
o atm, bar, mbar, mmHg, Pa, torr, psi
- If a pressure is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 100 pa and not 80-120 pa.
Example
1 atm
0.002 torr | 10000 Pa
1 atm >> 1 atm | nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1 Torr', '1 atm >> 1 atm', '0.00002 Torr | 1 Torr >> 1 Torr', '1 atm | 1 atm', '0.000001 mbar | 0.0000001 mbar', '1 *10-6bar | 1 *10-6bar', '0.0000002 Torr', '0.0000001 mbar | 0.0000001 mbar | 0.0000001', '0.0005 Pa | 0.0005 Pa', '0.00002 Torr | 1 Torr', '1 atm | 1 atm >> 1 atm', '0.000001 mbar', '0.0000048 Torr | 0.0000048 Torr', '0.0000001 Torr', '1 atm | 1 atm | 1 atm | 1 atm', '0.005 Torr | 1 atm', 'nan >> nan | nan', '0.000005 mbar | 0.000005 mbar', '0.00001 Pa | 0.00001 Pa', '0.000001 mbar | 0.000001 mbar', 'nan | nan', '1 atm | 1 atm | 1 atm', 'nan | 0.000001 mbar', 'nan | 1 atm', '0.000001 Torr', '0.0075 Torr', '1 atm >> 1 atm | 1 atm', 'nan |  E-6torr', '1 atm | 0.000001 mbar', 'nan | 0.000009 mbar', '0.00002 Torr', 'nan | 5 E-4mbar', '1 Torr >> 1 Torr', 'nan | 0.0005 Pa | 0.0005 Pa', '1 atm'])))

    deposition_synthesis_atmosphere_pressure_partial = Quantity(
        type=str,
        shape=[],
        description="""
    The partial pressures for the gases present during each reaction step.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the pressures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- If the synthesis atmosphere is a mixture of different gases, e.g. A and B, list the partial pressures and separate them with semicolons, as in (A; B). The list of partial pressures must line up with the gases they describe.
- In cases where no gas mixtures are used, this field will be the same as the previous filed.
Example
1 atm
0.002 torr | 10000 Pa
nan >> 0.99 atm; 0.01 atm | 1 atm
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1 Torr', '1 atm >> 1 atm', '0.0004023 Torr; 0.0046 Torr | 1 atm', '0.001 Torr; 0.004 Torr | 1 atm', '0.00002 Torr | 1 Torr >> 1 Torr', '1 atm | 1 atm', '0.000001 mbar | 0.0000001 mbar', '1 *10-6bar | 1 *10-6bar', '0.00002 Torr | 1 Torr', '1 atm | 1 atm >> 1 atm', '0.3 Torr', '0.000001 mbar', '1 atm | 1 atm | 1 atm | 1 atm', 'nan >> nan | nan', 'nan | 0.3 Torr', '0.0065 Torr; 0.001 Torr', '1 atm; 1 bar | 1 atm', '0.000001 mbar | 0.000001 mbar', 'nan | nan', '1 atm | 1 atm | 1 atm', 'nan | 1 atm', '0.000001 Torr', '1 atm >> 1 atm | 1 atm', '1 atm | 0.000001 mbar', '0.00002 Torr', '1 Torr >> 1 Torr', '0.0004545 Torr; 0.004545 Torr | 1 atm', '1 atm', '1 amt'])))

    deposition_synthesis_atmosphere_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relative humidity during each deposition step
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the relative humidity associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns
- If the relative humidity for a step is not known, stat that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 35 and not 30-40.
Example
35
0 | 20
25 >> 25 | 0
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '25', '30 >> 30', '0 >> 0', '15', '48 | 48', '0 | 0 >> 0', '20 | 20', '25 | 25', '30 | 30', '40', '30; 30', '50 | 50', '20', 'nan >> nan | nan', '50 | 50 | 50', '30', '35 | 0', 'nan | nan', '30 | 30 | 30 | 30', '0 | 0', '55; nan', '48', '30 | 30 | 30', '30 >> 30 | 30', '35 | 35 >> 35', '30 | 0', '35 | 35'])))

    deposition_solvents = Quantity(
        type=str,
        shape=[],
        description="""
    The solvents used in each deposition procedure for each layer in the stack
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvents associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the solvents in alphabetic order and separate them with semicolons, as in (A; B)
- The number and order of layers and deposition steps must line up with the previous columns.
- For non-liquid processes with no solvents, state the solvent as ‘none’
- If the solvent is not known, state this as ‘Unknown’
- Use common abbreviations when appropriate but spell it out when risk for confusion
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
DMF
Acetonitil; Ethanol | Ethanol
None | Chlorobenzene
H2O >> H2O | Methanol
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Ethanol | Ethanol', 'Unknown | IPA', 'Dichlorobenzene | none', 'Acetyl acetone; IPA | Water', 'Ethanol | anhydrous 1-butanol | Water >> Water; Ethanol >> Methanol; Water >> Water; Ethanol', '1-butanol >> 1-butanol | Ethanol', 'Ethanol; distilled Water >> nitric acid >> NaOH aqueous solution >> distilled Water; HCl | distilled Water', 'IPA | Unknown | Unknown', 'IPA >> Water | Ethanol; Water', 'Ethanol | Ethanol | Water', 'none >> 1-Butanol; IPA | Terpineol', 'IPA | Chlorobenzene', 'Ethanol | Terpineol; 2-Methoxy ethanol', '2-methoxyethanol | Chlorobenzene', 'Unknown | Unknown', 'none', 'Ethanol | P25; polyethylenglycol; OP; Water', 'Unknown >> Water >> Water >> Ethanol | Ethanol', 'n-butyl alcohol | n-butyl alcohol', 'IPA | Methanol >> Water >> Water', 'IPA >> Water | Ethanol', 'Water >> Water >> Ethanol', 'IPA | IPA', 'Chlorobenzene', '1-Butanol; IPA | Etanol >> Water', 'Ethanol | Dichlorobenzene', '1-Butanol | Ethanol | DMF', 'Ethanol', 'urea | hydrochloric acid | thioglycolic acid | SnCl2·2H2O | DI water', '2-methoxyethanol; Ethanolamine', '1-butanol | Water', 'butanol | Unknown', 'butanol | Ethanol', 'Chloroform | IPA', 'Water | 1-butanol >> Water', 'IPA | TiO2-np', 'butanol | IPA | Water', 'Ethanol | Ethanol | Ethanol', 'Terpineol | Terpineol | none', 'Ethanol; distilled Water >> nitric acid', 'Water | Ethanol', 'Chlorobenzene | none | none', 'Chloroform', 'Chlorobenzene | Ethyl alcohol', 'Acetyl acetone; IPA | Ethanol', 'Ethanol >> Water', '2-Butanol | Chlorobenzene', 'Water >> Water', 'Ethanol | Unknown | Unknown', '1-butanol | Unknown', 'IPA | none', 'Chlorobenzene | IPA | none', 'Ethanol | Ethanol | Ethanol | none', 'o-xylene >> tetrabutylammonium hydroxide 30-hydrate', 'Ethanol; distilled Water >> nitric acid >> none >> distilled Water; HCl', '2-methoxyethanol | Methanol', 'IPA; Ethanol | Terpineol | Unknown', 'Anh ethanol', 'Acetonitil; Acetyl aceton; IPA | Ethanol >> acetonitrile', 'Chloroform | Isopropyl alcochol', 'Ethanol | Ethanol | Ethanol | Unknown', 'Water | Unknown', '2-methoxyethanol >> 2-Butanol | Chlorobenzene', 'IPA | Water', 'none | Terpineol', 'Chlorobenzene | Ethanol', 'ethonal | 2-methoxyethanol | terpineol | acetonitrile', 'Water >> Ethanol | a-Terpineol >> Ethanol', 'Unknown >> Water | Chlorobenzene', 'Dicholorobenzene | IPA', 'Water | Methanol', 'Methanol | Water', 'Ethanol | Ethanol | Unknown', 'Ethanol >> Ethanol', '1-butanol  ethanol >> Water', 'IPA | Ethanol', 'Water | Water', 'Unknown | none | Unknown', 'Chloroform; IPA', '1-butanol | Ethanol', 'Ethanol | Water', 'n-butylalcohol | Ethanol', '1-Butanol >> 1-Butanol >> 1-Butanol | Acetylacetone; Polyethylene glycol; Triton X-100', 'Acetonitil; Acetyl aceton; IPA | Ethanol', 'Ethanol; HCl | Ethanol', 'Ethanol | Chlorobenzene', 'IPA >> Water | none', 'Dichlorobenzene', 'Acetyl acetone; Ethanol | Ethanol', '1-Butanol; IPA | Terpineol', 'Unknown >> Water', 'Unknown', 'Ethanol >> Water | Ethanol', 'none | Ethanol', 'Ethanol | Ethanol >> acetonitrile', 'Chlorobenzene | none', 'Chlorobenzene; DCB | IPA', 'Water | Chlorobenzene', 'Ethanol >> Ethanol | IPA', 'n-butyl alcohol | Unknown', 'terpineol; Ethanol', '1-Butanol', '2-methoxyethanol | Water', 'Water2; Water | Chlorobenzene', 'Chlorobenzene; Octane | none', 'IPA >> IPA >> IPA | Unknown >> Unknown >> Unknown >> Unknown >> Unknown >> Unknown >> acetonitrile', 'IPA; Ethanol | Ethanol', 'none >> Water >> Water', 'IPA >> Ethanol', 'Water', 'Chlorobenzene | 2-methoxyethanol', 'Anisole; tetralin; TAA', 'Water | IPA', 'none | Chlorobenzene', 'none | none', 'Unknown | Ethanol', 'none | terpineol; Ethanol', '1-butanol', 'Ethanol; Water', 'Ethanol | Methanol', '1-butanol | Ethanol >> Water | Ethanol >> Water', '1-Butanol; IPA | 1-Butanol; Ethylcellulose; Llauric acid; Terpineol', 'Chlorobenzene | Methanol', '2-methoxyethanol', '2-methoxyethanol >> 2-Butanol', 'IPA; Etanol | Etanol', 'Chlorobenzene | Unknown', 'n-butylalcohol | 2-methoxyethanol', 'IPA >> Water', 'n-butyl alcohol', 'Dichlorobenzene | IPA', 'IPA; Ethanol | none', 'n-butylalcohol', 'Ethanol | anhydrous 1-butanol', 'IPA | Unknown', 'Ethanol | Unknown', 'Ethanol | none', '1-Butanol | Ethanol', 'Methanol; n-butanol; Chloroform', 'Chlorobenzene | Trifluorethanol', 'Chlorobenzene | Unknown | Unknown', 'Chlorobenzene | Water', 'Chlorobenzene | Chlorobenzene | Ethanol', 'Water2; Water', 'deionized water', 'n-butyl alcohol | Ethanol', 'IPA', 'n-butyl alcohol | n-butyl alcohol | Unknown', 'Ethanol | IPA', 'Chlorobenzene | IPA'])))

    deposition_solvents_mixing_ratios = Quantity(
        type=str,
        shape=[],
        description="""
    The mixing ratios for mixed solvents
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvent mixing ratios associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- For pure solvents, state the mixing ratio as 1
- For non-solvent processes, state the mixing ratio as 1
- For unknown mixing ratios, state the mixing ratio as ‘nan’
- For solvent mixtures, i.e. A and B, state the mixing ratios by using semicolons, as in (VA; VB)
- The preferred metrics is the volume ratios. If that is not available, mass or mol ratios can be used instead, but it the analysis the mixing ratios will be assumed to be based on volumes.
Example
9; 0.6; 0.4 | 1
1 >> 1 | 1
9; 1 | 3; 2
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=[''])))

    deposition_solvents_supplier = Quantity(
        type=str,
        shape=[],
        description="""
    The suppliers of all the solvents.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvent suppliers associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the associated suppliers and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- For non-liquid processes with no solvents, mark the supplier as ‘none’
- If the supplier for a solvent is unknown, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Sigma Aldrich
Sigma Aldrich; Fisher | Acros
none >> Sigma Aldrich; Sigma Aldrich | Unknown
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Sigma Aldrich | Unknown >> Unknown', 'Sigma Aldrich | Sigma Aldrich | Unknown >> Unknown; Sigma Aldrich >> Unknown; Unknown >> Unknown; Sigma Aldrich', 'Acros Organics; Sigma Aldrich', 'sigma aldrich', 'Sigma Aldrich; Sigma Aldrich | Unknown >> Unknown', 'Sigma Aldrich', 'Alfa Aesar', 'Sigma-Aldrich', 'Unknown', 'NanoPac >> Unknown | NanoPac', 'Millipore Sigma | Milllipore Sigma', 'Unknown | Unknown', 'Sigma Aldrich | Sigma Aldrich', 'Sigma Aldrich | Unknown >> Unknown | Unknown >> Unknown', 'Unknown >> Unknown | Unknown', 'Sigma Aldrich; Sigma Aldrich', 'Wako; Wako; Wako; Unknown', 'Unknown >> Unknown | Alfa Aesar', 'Sigma Aldrich | Fischer Scientific', 'Kanto Chemical Tokyo; Unknown', 'Unknown | Sigma Aldrich', 'Unknown >> Sigma Aldrich; Sigma Aldrich | Sigma Aldrich', 'NanoPac >> Unknown', 'Sigma Aldrich; Sigma Aldrich; Fisher | Sigma Aldrich >> Acros', 'Sigma Aldrich | Unknown', 'Sigma Aldrich; Sigma Aldrich | Sigma Aldrich', 'Unknown; Sigma Aldrich', 'Sigma Aldrich; Unknown >> Sigma Aldrich >> Sigma Aldrich >> Unknown; Sigma Aldrich | Unknown', 'Sigma Aldrich | Sigma Aldrich >> Sigma Aldrich', 'Kanto Chemical Tokyo; Unknown | Unknown', 'Alfa Aesar | Alddin', 'Sigma Aldrich | Unknown | Unknown', 'Sigma Aldrich | Sigma Aldrich | Unknown', 'Nacalai Tesque', 'Sigma Aldrich; Unknown >> Sigma Aldrich', 'Unknown | Wako Pure Chemical Industries; Nacalai Tesque; Sigma Aldrich', 'Unknown | Alfa Aesar', 'Unknown; Unknown | Unknown', 'Sigma Aldrich; Unknown >> Sigma Aldrich >> Unknown >> Unknown; Sigma Aldrich', 'Sinopharm Chemical Reagent Co. Ltd.'])))

    deposition_solvents_purity = Quantity(
        type=str,
        shape=[],
        description="""
    The purity of the solvents used.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the solvent purities associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solvent is a mixture of different solvents, e.g. A and B, list the associated purities and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- Use standard nomenclature for purities, e.g. pro analysis, puris, extra dry, etc.
- For non-liquid processes with no solvents, state the purity as ‘none’
- If the purity for a solvent is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Pro analysis
Puris; Puris| Tecnical
none >> Pro analysis; Pro analysis | Unknown
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Puris | Unknown >> Unknown | Unknown >> Unknown', 'Puris | Unknown >> Unknown', 'Puris | Puris | Unknown >> Unknown; Puris >> Unknown; Unknown >> Unknown; Puris', '99.8%; 99.5% | Uknown >> Unknown', 'Technical | Puris', '99.5% | 99.5%', 'Unknown', '99.8% | 99.5%', '99.8% | Unknown | Unknown', 'Unknown | Unknown', 'Unknown | Unknown | Unknown', 'Unknown >> Unknown | Unknown', '0.998', '99.8% >> Unknown | 99.8%', 'Puris', 'Puris; Puris', '99.8 >> Unknown | 99.8%', '99.8% >> Unknown', 'Pro analysis; Pro analysis; Pro analysis | Puris >> Pro analysis', 'Unknown; Puris', 'Puris | Puris', 'Anhydrous 99.8%'])))

    deposition_reaction_solutions_compounds = Quantity(
        type=str,
        shape=[],
        description="""
    The non-solvent precursor chemicals used in each reaction step
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the non-solvent chemicals associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several compounds, e.g. A and B, list the associated compounds in alphabetic order and separate them with semicolons, as in (A; B)
- Note that also dopants/additives should be included
- When several precursor solutions are made and mixed before the reaction step, it is the properties of the final mixture used in the reaction we here describe.
- The number and order of layers and reaction steps must line up with the previous columns.
- For gas phase reactions, state the reaction gases as if they were in solution.
- For solid-state reactions, state the compounds as if they were in solution.
- For reaction steps involving only pure solvents, state this as ‘none’
- If the compounds for a deposition step is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Titanium diisopropoxide bis(acetylacetonate) | TiO2-np
C60 | BCP
Titanium diisopropoxide bis(acetylacetonate) | TiO2-np >> Li-TFSI
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'nan | TiO2-np Anatase; TiO2-np Rutile', 'PEIE >> nTi-MOF | PCBM-60', 'TiO2-np; titanium diisopropoxide bis(acetylacetonate)', 'C60 | TDMASn', 'TiOx >> TiOx', 'Zinc Acetate dehydrate; ethanolamine | 3, 4, 5- trimethoxybenzoic acid', 'SnO2-np | PCBM-60; PEG', 'SnCl4', 'ICBA | BCP', 'SnO2-np | Choline Chloride', 'Titanium diisopropoxide bis(acetylacetonate) >> Titanium diisopropoxide bis(acetylacetonate) | CsAc', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2-np >> TiCl4 >> nan', 'TiCl4 | TiO2 paste', 'SnCl2', 'Titanium isopropoxide; diethanolamine | Titanium tetrabutanolate', 'SnO2-np', 'PCBM-60 | tetrakisdimethylamino-tin; H2O >> tetrakisdimethylamino-tin; H2O', 'Titanium diisopropoxide bis(acetylacetonate) | Titanium diisopropoxide bis(acetylacetonate) | (3-aminopropyl)trimethoxysilane (APTMS)', 'nan >> TiCl4 >> nan >> nan | TiO2-np', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2-np', 'Titanium(IV) isopropoxide >> nan >> nan >> NaOH >> nan | magnesium methoxide', 'Acetylacetone; Titanium isopropoxide | TiO2 paste NR30-D', 'Titanium isopropoxide (TTIP); HCl | TiO2 paste 18NRT', 'Zinc acetate dihydrate; KOH; ZnO', 'PCBM-60 | PFN', 'PEIE >> nTi-MOF', 'PCBM-60 | PEI', 'Zinc Acetate dehydrate; ethanolamine | 2-methoxybenzoic acid', 'PCBM | BCP', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2-np | ZrO-np', 'diethanolamine; Titanium isopropoxide; H2O', 'SnO2 | C60', 'Ti >> NaOH >> HCl', 'nan | TiO2-np', 'Zinc Acetate dehydrate; ethanolamine | 4-dimethoxybenzoic acid', 'TiO2 np', 'Titanium oxysulfate | PDI-glass', 'ZnO-np', 'SnCl2 | C60', 'Titanium diisopropoxide bis(acetylacetonate) >> Titanium diisopropoxide bis(acetylacetonate) >> Titanium diisopropoxide bis(acetylacetonate) | TiO2-np', 'PCBC6 | BCP', 'Titanium isopropoxide (TTIP); acetyl acetone >> NR30-D; ethanol', 'synthesized | synthesized | synthesized', 'tetrakisdimethylamino-tin; H2O', 'PCBM-60 | PEIE', 'Zinc Acetate dehydrate; ethanolamine', 'TiO2-np; Ethylcellulose', 'SnO2-np | 4-Bromobenzoic acid', 'nan | TiO2-np; Ethylcellulose', 'SnO2-np | ZnO-np', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2-np >> Li-TFSI', 'TPE-DPP-8 | C60 | BCP', 'SnCl5', 'HCl; Titanium isopropoxide | TiO2 paste | nan', 'TiO2 pellets | TTIP', 'SnO2', 'Titanium diisopropoxide bis(acetylacetonate) | Al2O3-np | Cu:NiO-np', 'Titanium diisopropoxide bis(acetylacetonate) | MgCl6 6H2O; SnCl2 2H2O | TiO2-np | ZrO2-np', 'Titanium isopropoxide (TTIP); HCl', 'TiO2-np; titanium diisopropoxide bis(acetylacetonate) | PPDI-F3N', 'PCBM-60 | Rhodamine 101 | LiF', 'B2F | C60 | BCP', 'Titanium diisopropoxide bis(acetylacetonate) | CaSc2O4:0.15Eu3+', 'titanium tetrachloride', 'Titanium diisopropoxide bis(acetylacetonate); TiO2-np', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste NR30-D', 'SnO2-np | KOH', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste NR30-D | SnCl4', 'Titanium diisopropoxide bis(acetylacetonate); TiO2-np; PCBM', 'Titanium isopropoxide | TiO2 paste', 'Acetylacetone; Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste', 'Titanium diisopropoxide bis(acetylacetonate) | Titanium diisopropoxide bis(acetylacetonate)', 'Titanium isopropoxide | TiO2-np | Zn(NO3)2.6H2O >> nan >> Na2S >> nan', 'tantalum(V) ethoxide in titanium; Titanium diisopropoxide bis(acetylacetonate)', 'PCBM-70 | TiO2', 'TPE-DPP-6 | C60 | BCP', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2-np >> TiCl4', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste | Al2O3 paste', 'Titanium Orthotitanate | TiO2-np', 'PCBM-60', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste', 'SnO2 2H2O', 'nan | Al2O3-np', 'Titanium diisopropoxide bis(acetylacetonate)', 'Titanium diisopropoxide bis(acetylacetonate) >> TiCl4 | C60', 'Titanium isopropoxide (TTIP); HCl | C60 solution', 'nan | TiO2-np Rutile', 'PCBM-60 | Bphen', 'PEIE; C60', 'PCBM-60 | tetrakisdimethylamino-tin; H2O', 'SnCl2.H2O | ethanol | ( 3-aminopropyl)triethoxysilane (APTES) | IPA', 'Tetraisopropyl orthotitanate | TiO2-np', 'Titanium isopropoxide', 'tetrakisdimethylamino-tin; H2O >> tetrakisdimethylamino-tin; H2O', 'PCBM-70', 'SnO2-np | NaOH', 'Titanium tetrachloride', 'Titanium diisopropoxide bis(acetylacetonate); vanadium(V)oxytriethoxide | TiO2 powder; polyethylene glycol >> acetylacetone; triton X-100', 'C60 | LiF | BCP', 'HCl; Titanium isopropoxide | TiO2 paste', 'Titanium(IV) isopropoxide >> nan >> nan >> NaOH >> nan', 'Titanium diisopropoxide bis(acetylacetonate) | Polystyrene latex microsphere solution >> TiCl4 | TiO2-np >> TiCl4', 'synthesized | BCP', 'Tetra-nbutyl titanate; diethanolamine >> TiCl4 | TiO2 paste >> TiCl4 | ZrO2 paste', 'Titanium oxysulfate', 'C60', 'nan | TiO2 paste 18NRT', 'nan | TiO2-np | ZrO-np', 'Titanium(IV) isopropoxide >> nan', 'SnCl2 | PCBM-60', 'PCBM-60 | PFN-Br', 'nan | C60-SAM', 'HCl; TiCl3', 'C60; (RuCp*mes)2', 'PCBM-60 | Rhodamine 101', 'TiOx >> TiOx >> TiOx', 'TiCl4', 'PCBM-60 | AZO', 'Titanium diisopropoxide bis(2,4-pentanedionate) | In(NO3)3·xH2O', 'nan | TiO2-np >> TiCl4', 'TPE-DPP-16 | C60 | BCP', 'Titanium isopropoxide | Ethanol', 'PCBM | TBAOH', 'CdI2 | C60 | BCP', 'Titanium isopropoxide >> TiCl4 | TiO2-np', 'nan | TiO2-np Anatase', 'Titanium diisopropoxide bis(acetylacetonate) >> TiCl4 | TiO2-np', 'Zinc acetate; Tin Acetate', 'TiOx', 'Titanium isopropoxide >> TiCl4 | PCBA', 'Titanium tetrabutanolate', 'titanium diisopropoxide bis(acetylacetonate) | TiO2-np | ZrO2-np', 'Titanium diisopropoxide bis(acetylacetonate) >> TiCl4', 'Titanium isopropoxide; diethanolamine | TiO2-np >> TiCl4', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2-np | SbI3', 'TiO2-crystalline anatase np', 'Titanium isopropoxide (TTIP)', 'nan | nan', 'Tetrabutyl titanate | TiO2-np', 'TiO2-c | PCBM-61', 'nan | TiO2-np Anatase >> CdSO4; CS(NH2)2; NH3.H2O', 'SnCl2.H2O | ethanol', 'Titanium tetrachloride | TiO2-np', 'MgCl6 6H2O; SnCl2 2H2O | TiO2-np | ZrO2-np', 'TiCl4 | PCBM-60', '1,4,5,8-Naphthalenetetracarboxylic dianhydride; (R)-(-)-aminoindane', 'Ti', 'Tetrabutyl titanate', 'Tetra-nbutyl titanate; diethanolamine | TiO2 paste NR30-D', 'COi8DFIC | BCP', 'Titanium isopropoxide >> TiCl4', 'TiO2 -np | Ti | ZrO2-np', 'C60 | BCP', 'Acetylacetone; IPA; tetrabutyl titanate; Triton X100 | TiO2 paste', 'NDI3HU-DTYM2 | BCP', 'TiO2-anatase >> Titanium diisopropoxide bis(acetylacetonate) | TiO2-np', 'titanium tetrachloride | TiO2-np >> titanium tetrachloride', 'Titanium diisopropoxide bis(acetylacetonate) >> Titanium diisopropoxide bis(acetylacetonate)', 'TiCl4 >> TiCl4', 'Titanium diisopropoxide bis(acetylacetonate); niobium(V)ethoxide | TiO2 powder; polyethylene glycol >> acetylacetone; triton X-100', 'SnO2-np | PCBM-60', 'PCBM-70 | Rhodamine 101', 'Titanium diisopropoxide bis(acetylacetonate) | SnCl4', 'PCBM | Bis-C60', 'PEIE', 'Nb | TiO2-np', 'Titanium isopropoxide | PCBM-60', 'titanium isopropoxide', 'ITIC | BCP', '(DTYM-NDI-DTYA)2 | BCP', 'PCBM-60 | ZnO-np', 'TiO2-nw', 'Titanium isopropoxide | TiO2-np >> Li-TFSI', 'TiCl4 >> nan >> nan', 'Titanium diisopropoxide bis(2,4-pentanedionate)', 'Titanium diisopropoxide bis(acetylacetonate) >> Titanium diisopropoxide bis(acetylacetonate) | TiO2-np', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste 18NR-T', 'MoS2-nanosheets', 'Titanium diisopropoxide bis(acetylacetonate); acetylacetone', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 powder; polyethylene glycol >> acetylacetone; triton X-100', 'PCBM-60 | C60 | LiF', 'Tetrabutyl titanatein; HCl', 'Zinc Acetate dehydrate; ethanolamine | PCBM-60', 'TPE-DPP-12 | C60 | BCP', 'SnO2-np | ethylphosphonic acid', 'TiO2-anatase | TiO2-np', 'HCl; Titanium isopropoxide', 'Titanium isopropoxide | TiO2-np', 'IT-4f | BCP', 'Titanium diisopropoxide bis(acetylacetonate); tantalum(V)ethoxide | TiO2 powder; polyethylene glycol >> acetylacetone; triton X-100', 'tin chloride bihydrate', 'PCBM-61 | BCP', 'Titanium tetraisopropoxide; acetylacetone | TiO2-np | Carbon-QDs', 'Titanium diisopropoxide bis(acetylacetonate) | TiO2 paste | ZrO2 paste | carbon paste', 'Titanium diisopropoxide bis(acetylacetonate) >> titanium tetrachloride | TiO2-np', 'CdSO4; thiourea; NH4OH', 'HCl; Titanium isopropoxide | 2-mIm; Zn(NO3)2', 'PCBM | LiF', 'PCBM-60 | BCP', 'SnCl4 | 1‐butyl‐3‐methylimidazolium bromide', 'Titanium tetraisopropoxide; acetylacetone | TiO2-np', 'PCBM | PNDI-2T | LiF', 'tetraamminezinc(II) hydroxide', 'HCl; Titanium isopropoxide | TiO2 paste 22NR-T Solaronix', 'Titanium isopropoxide | HCl | Ethanol', 'titanium (diisopropoxide) bis(2,4-pentanedionate) | TiO2-np'])))

    deposition_reaction_solutions_compounds_supplier = Quantity(
        type=str,
        shape=[],
        description="""
    The suppliers of the non-solvent chemicals.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the non-solvent chemical suppliers associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, e.g. A and B, list the associated suppliers and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- For gas phase reactions, state the suppliers for the gases or the targets/evaporation sources that are evaporated/sputtered/etc.
- For solid state reactions, state the suppliers for the compounds in the same way.
- For reaction steps involving only pure solvents, state the supplier as ‘none’ (as that that is entered in a separate filed)
- For chemicals that are lab made, state that as “Lab made” or “Lab made (name of lab)”
- If the supplier for a compound is unknown, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Dysole; Sigma Aldrich; Dyenamo; Sigma Aldrich
Sigma Aldrich; Fisher | Acros
Lab made (EPFL) | Sigma Aldrich >> none
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Pegasus; Uppsala University', 'Unknown | Pegasus; Uppsala University >> Pegasus; Uppsala University', 'Sinopharm Chemical Reagent Co., Ltd; Macklin | Macklin | Shanghai MaterWin New Material', 'Fisher Scientific; Greatcell Solar', "Xi'an p-OLED Corp. | Xi'an p-OLED Corp.", 'Unknown | Unknown', 'Sigma Aldrich | Sigma Aldrich', 'Sigma Aldrich | Dysole >> Sigma Aldrich >> Unknown', 'Solenne B.V. | Sigma-Aldrich', 'Sinopharm', 'Merck | Solaronix', 'ENB Korea >> Sigma Aldrich', 'Nichem Fine Technology | Nichem Fine Technology', 'Sigma Aldrich | Alfa-Aesar >> Junsei Chemicals | Dyesol >> Junsei Chemicals', 'Nichem Fine Technology Co. Ltd.', 'ENB Korea >> Sigma Aldrich >> ENB Korea', 'Nano-c', 'Sigma Aldrich | Dysole', 'Sigma Aldrich | Sigma Aldrich | Sigma Aldrich', 'nano-c; Unknown', 'Sinopharm | America Dye Sources', 'CBMM | Dyesol', 'Acros', '1-Material Inc', 'Sigma Aldrich', 'Nichem', 'Solenne | Sigma Aldrich', 'Sigma Aldrich | Dysole >> Sigma Aldrich', 'Millipore Sigma | Milllipore Sigma', 'Sinopharm; Sinopharm', 'Han Feng Chemical | P-OLED', 'Unknown | Dyesol', 'Sigma Aldrich; Synthetized', 'Lab made', 'Unknown | Sigma Aldrich', 'Unknown >> Unknown | JGC Catalysts and Chemicals Ltd.', 'Unknown | Dyesole', 'Sigma Aldrich | Sinopharm Chemical Reagent Co., Ltd; Macklin | Macklin | Shanghai MaterWin New Material', 'Sigma Aldrich | Lab-made', 'Xi’an Polymer Light Technology Corp', 'Unknown | Degussa', 'Sigma Aldrich >> Unknown', 'Sigma Aldrich | Unknown >> Sigma Aldrich', 'Sigma Aldrich; Solaronix; Solaronix', 'Alfa Aesar', 'Sigma Aldrich | Unknown >> Sinopharm', "Xi'an Polymer Light Technology Corp. | Xi'an Polymer Light Technology Corp.", 'Unknown', 'Solaronix | Unknown', 'NanoPac >> synthsized', 'Unknown | Nichem Fine Technology', 'Nano-C | Alfa-Aesar', 'Pegasus; Uppsala University >> Pegasus; Uppsala University', 'Sigma Aldrich; Sigma Aldrich', 'Sigma Aldrich | Dyesol >> Junsei Chemicals', 'Aldrich; Aldrich | Nippon Aerosil; Nacalai Tesque >> Wako Pure Chemical; Wako Pure Chemical', 'Ossila | Unknown', 'Alfa-Aesar', '1-Material', 'Aldrich | Nippon Aerosil; Nacalai Tesque >> Wako Pure Chemical; Wako Pure Chemical', 'Sigma Aldrich | SureChem', 'Unknown; Sigma Aldrich', "Lab made | Xi'an Polymer Light Technology Corp. | Xi'an Polymer Light Technology Corp.", 'Aldrich; Solaronix Ti-Nanoxide N/SP', 'NanoPac >> Lab made | NanoPac', '1-Material | 1-Material', 'Nano-C', 'Sigma Aldrich >> Unknown >> Sigma Aldrich >> Unknown', 'Sigma Aldrich | Greatcell', 'Unknown | Dyesole | Solaronix', 'Unknown | Pegasus; Uppsala University', 'Solarmer Material | 1-Material', 'Sigma Aldrich | Solaronix PST-18NR | Sigma Aldrich | Borun New Material Technology', 'Unknown | 1-Materials', 'Luminescence Technology Corp', 'Luminescence Technology Corp | Xi’An Polymer Light Technology Corp', 'Sigma Aldrich >> ENB Korea', 'Alfa Aesar >> Unknown >> Unknown', 'Sigma Aldrich | Dyesol', 'Unknown | Sigma Aldrich; Degussa', 'ITASCO >> Unknown >> Unknown', 'Alfa-Aesar | Lab made', 'Sigma Aldrich >> Unknown >> Sigma Aldrich >> Unknown | Sigma Aldrich', 'Frontier Carbon Corp. | Tokyo Chemical Industry', 'Sigma Aldrich | Dyesol | Sigma Aldrich >> Unknown >> Sigma Aldrich >> Unknown', 'Unknown | NanoCleantech', 'Sigma Aldrich | Aerosil', 'America Dye Sources'])))

    deposition_reaction_solutions_compounds_purity = Quantity(
        type=str,
        shape=[],
        description="""
    The purity of the non-solvent chemicals.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the compound purities associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, i.e. A and B, list the associated purities and separate them with semicolons, as in (A; B)
- The number and order of layers, reaction steps, and solvents must line up with the previous columns.
- Use standard nomenclature for purities, e.g. pro analysis, puris, extra dry, etc.
- For reaction steps involving only pure solvents, state this as ‘none’ (as that is stated in another field)
- If the purity for a compound is not known, state this as ‘Unknown’
- This category was included after the projects initial phase wherefor the list of reported categories is short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
Pro analysis
99.999; Puris| Tecnical
Unknown >> Pro analysis; Pro analysis | none
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Pro analysis', 'Pro analysis; Unknown', '99%; 99.99%', 'Puris | Unknown >> Puris | Unknown >> Puris', '0.97', '98%; 99.8%', '99.99% >> Unknown', 'Unknown >> Unknown >> Unknown >> Unknown | Unknown', 'Unknown', 'Unknown | Unknown', 'Puris | Unknown', 'Unknown; 97%', 'Pro analysis; Puris | Puris >> Puris', 'Pro analysis | Tecnical >> Pro analysis', '0.98', 'Unknown >> Unknown | Unknown', 'Puris', '0.999', 'Technical | Unknown', '96% | Unknown', 'Unknown >> Unknown >> Unknown >> Unknown', 'Unknown >> Unknown', '99.5% | 99%', '99.99% >> Unknown | Unknown', 'Puris | Pro-analysis', 'Unknown | 99%', '99.9% | Unkown', 'Puris | Unknown >> Puris', 'Pro analysis | Puris >> Puris', 'Unknown | Unknown | Puris >> Unknown >> Puris >> Unknown', 'Unknown | 99.8%'])))

    deposition_reaction_solutions_concentrations = Quantity(
        type=str,
        shape=[],
        description="""
    The concentration of the non-solvent precursor chemicals.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the concentrations associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a solution contains several dissolved compounds, e.g. A and B, list the associated concentrations and separate them with semicolons, as in (A; B)
- The order of the compounds must be the same as in the previous filed.
- For reaction steps involving only pure solvents, state this as ‘none’
- When concentrations are unknown, state that as ‘nan’
- Concentrations can be stated in different units suited for different situations. Therefore, specify the unit used. When possible, use one of the preferred units
o M, mM, molal; g/ml, mg/ml, µg/ml, wt%, mol%, vol%, ppt, ppm, ppb
- For values with uncertainties, state the best estimate, e.g write 4 wt% and not 3-5 wt%.
Example
4 wt%
0.2 M; 0.15 M| 10 mg/ml
0.3 mol% | 2 mol%; 0.2 wt% | nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '0.05 M', '0.15 M | 33.33 wt%', '15 wt%', '16 mg/ml', '15 mg/ml | nan', '0.42 M', '120 mg/ml; 640 mg/ml', '25 mg/ml | nan', '20 mg/ml; nan', '52 wt% | 208 mg/ml; 14 mg/ml | 20 wt% | 20 wt%', '0.15 M | 0.20 M', '20 mg/ml | 30 mg/ml', 'nan | nan >> 80 mM', '8 mg/ml | nan', '20 mg/ml | 1 mg/ml', '15 mg/ml | 1 mg/ml', '2 mg/ml | 0.6 mg/ml | nan', '164 mg/ml; 50 mg/ml', '1 M; 0.5 M', '14 vol%; 20 vol%', '3 mg/ml | nan', '0.2 M', 'nan >> 0.04 M >> nan >> nan | 20 wt%', '0.15 M | 0.15 M', '13 wt% | 20 wt%', '2.564 vol%; 25 wt%; nan; nan', '10 wt% | 20 wt%', '5 mg/ml', '12 wt% | 20 wt%', '208 mg/ml; 14 mg/ml | 20 wt% | 20 wt%', '20 mg/ml | nan | nan', 'nan | nan >> 20 mM', '2.5 wt%; 20 wt%', '5 mg/ml | nan', '0.03 M', '15 mg/ml; 2 mg/ml', '0.254 M; 0.02 M; 0.1 mg/ml', '0.15 M; nan', '2 mg/ml | nan | nan', '0.16 M', '33 wt% | 10 mg/ml; 10 mg/ml', 'nan | nan >> 100 mM', '20 wt%', '0.2 M; 2 M | 150 mg/ml', '25 wt%; 28 wt%', '400 mM >> nan >> nan', '75 wt% | nan', '0.15 M | 7.5 mg/ml', '20 mg/ml | 0.1 wt%', '11 wt% | 20 wt%', '20 mM; 150 mg/ml', '0.2 M | nan', '200 mM >> nan >> nan', '2 vol%; 15 vol%', '15.38 vol%', '20 mg/ml | 0.2 %', 'nan | 10 mg/ml', '0.286 vol%; 0.2 wt%', '0.3 M; 10 mg/ml', 'nan; 0.9 vol%', '20 mg/ml; 0.5 mg/ml', '0.3 M', 'nan | 2.0 M', '1.8 wt% | nan', '20 mg/ml', '40 mg/ml | 0.5 mg/ml', '8.6 vol%; 5.71 vol% >> 12 wt%', '14 wt% | 20 wt%', '6 vol% | 125 mg/ml', '0.2 M | 15 mg/ml', '6 vol% | 150 mg/ml >> 10 mg/ml', '0.355 vol%; 6.4 vol%', '4 wt%', '46.7 vol% >> nan', '17 wt% | 20 wt%', '8 mg/ml', '2 wt%', '100 mg/ml; 2.8 mg/ml | 10 mg/ml', '7.5 vol% | 28 %', '0.08', '16 wt% | 20 wt%', '2 wt% | 1 mg/ml', '20 mg/ml | nan | 0.5 mg/ml', 'nan | nan >> 0.1 M', 'nan | 150 mg/ml', '0.3 M >> 40 mM | nan', '20', '0.15', '40 mg/ml | 11.11 vol%', '20 mM >> 0.11 mg/ml >> 20 mM', '0.04 M | 20 mg/ml', 'nan | nan | 5 mM | nan', '15 wt% | 20 wt%', '100 mM >> nan >> nan', '2.5 wt%', '1.25 vol% | nan | nan', '20 wt% | 20 wt%', '46.7 vol% >> nan >> 20 mg/ml >> nan | nan', 'nan | 28.6 vol% >> 0.02 M', '0.3 M >> 40 mM', '20 mg/ml | 0.2 wt%', '5.26 vol% >> 4.2 vol%', '10 vol%', 'nan | 4 wt%', '6 vol% | 10 wt% | 1 mM', '40 mM', '0.0267', '0.3 M >> 40 mM | 14 wt%', '2.2 vol% >> 0.22 vol%', '2.67 wt% | 20 mM', '10 mg/ml', 'nan | 0.1 g/0.8mL >> 0.1 M', 'nan | 0.04 M', '0.2 M | 5 mg/ml', '75 wt% | 25 wt% >> 0.05 M >> nan', 'nan >> nan | 22.2 wt%', '20 mg/ml | 40 mg/ml', '0.15 M | nan', 'nan >> 1 M >> 0.4 M', 'nan | 22.22 wt%', '0.2 M | 10 mg/ml', '20 mg/ml >> 0.7 mg/ml', '18 mg/ml', 'nan | 22.2 wt%', 'nan | 1.5 M', '2 vol%; 15 vol% | 22 mg/ml; 9.9 mg/ml', '0.125 M >> 0.025 M | 0.1 mg/ml', '20 mg/ml | 1.5 mg/ml', '0.15 M | 130 mg/ml >> 0.02 M', 'nan | 0.12 g/ml | 0.2 M >> nan >> 0.1 M >> nan', '0.15 M', '2.4 vol%', 'nan | nan >> 40 mM', '13.3 mg/ml; 3.6 vol%; 0.098 vol%', '20 mg/ml | 2.5 wt%', '15 wt% | 0.5 mg/ml', '20 mg/ml; 0.8 mg/ml', '14.6 vol%; 1 M; 22.2 wt%', 'nan | 41.6 wt% | nan', '20 mg/ml | 4.61 mg/ml', '33 wt% | 10 mg/ml', '0.3 M | 33 vol% >> 0.04 M | 28.6 wt% >> 0.04 M', '0.3 M | 28.6 wt% >> 0.04 M', '18 wt% | 20 wt%', '0.7 vol%; 8 vol% | 1.8 wt%', '0.15 M | 15.15 mg/ml >> 0.02 M', '0.5 M; 0.5 M | nan', 'nan | 0.5 M', '0.15 M | 0.3 M | nan', '0.15 M >> 0.3 M | 60 mg/ml', '10 vol% | nan', '2.25 vol%', 'nan | 14.3 wt%', '0.1 M', '22 wt% | 20 wt%', '2 mg/ml', '11.4 wt%', 'nan | nan', '10 mg/ml | 0.5 mg/ml', '164 mg/ml; 50 mg/ml | 0.7 mg/ml', '30 mg/ml | 0.5 mg/ml', '33 wt%', '0.04 M', '15 mg/ml | 2 mg/ml', '15 wt% | 1 mg/ml', '10 mg/ml | nan', '20 mg/ml | 0.6 mg/ml', '5.3 mg/ml; nan', '30 mg/ml', '16 wt% | 6.67 wt% | 0.5 wt%', '25 wt%28wt%', '23.6 mg/ml; 22.77 mg/ml; 6 mg/ml', '0.15 M | 2 :7wt', '20 mg/ml | 5 mg/ml', '0.4 wt% | nan', '20 mg/ml | 0.5 mg/ml', '30 mg/ml | nan', '46.7 vol% >> nan >> 20 mg/ml >> nan', 'nan | 22 wt%', '250 mg/ml', 'nan | 1.0 M', 'nan >> 0.15 M | nan', '1.43 mg/ml | nan', 'nan | 0.08 wt%', '1.5 mM; 1.5 mM; 30 %', '5.3 mg/ml; nan | 0.1 mg/ml', '20 mg/ml | nan', '0.15 M >> 0.30 M', '5 mol%; 10 vol%', '2.67 wt%', 'nan | 0.25 mg/ml', '0.15 M | 10 vol%', '0.254 M; 0.02 M', 'nan | 4 mg/ml', '10 vol% >> 10 vol%', '0.15 M >> 0.3 M >> 0.3 M | nan', '0.4 wt%', '200 mM | 22 wt%', '0.2 M | 0.066 wt%', '0.5 M; 0.5 | nan >> 0.04', '0.15 M | 0.10 M', '0.2 wt% >> 8 mg/ml | nan', '19 wt% | 20 wt%', '0.15 M | 0.05 M', '0.15 M; 20 wt%; 0.0002 M', '0.15 M; 20 wt%', '2 M; 16.67 wt%', '20 mg/ml | 20 mg/ml', 'nan; 60 mg/ml', '6 mg/ml', '15 mg/ml', '0.2 M | 7.5 mg/ml', '7 mg/ml | nan', 'nan; 4 mg/ml', '100 mg/ml; 2.8 mg/ml', '3 mol%; 10 vol%', '10 wt% | 0.8 mg/ml', '10 vol% >> 10 vol% | 0.1 M', '3 wt%', '200 mM', '10 vol% | 25 wt%', '10 vol% | 18 wt%', '1 mol%; 10 vol%', '6 vol%; 0.67 vol%', '0.15 M | 0.3 M', '22 mg/ml', '21 wt% | 20 wt%', 'nan | 0.7 mh/ml', '20 mg/ml | 10 mg/ml', '30 mg/ml | 0.1 wt%', '300 mM >> nan >> nan', 'nan | 0.12 g/ml', '0.2 wt% >> 8 mg/ml', 'nan | 0.2 M', '1 M'])))

    deposition_reaction_solutions_volumes = Quantity(
        type=str,
        shape=[],
        description="""
    The volume of the reaction solutions
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the volumes associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The volumes refer the volumes used, not the volume of the stock solutions. Thus if 0.15 ml of a solution is spin-coated, the volume is 0.15 ml
- For reaction steps without solvents, state the volume as ‘nan’
- When volumes are unknown, state that as ‘nan’
Example
0.1
0.1 >> 0.05 | 0.05
nan | 0.15
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['1.0 | Unknown', '54.35', '0.9 >> 0.1 >> 15.0', '10.0', '125.0; 65.0; Unknown', 'Unknown >> Unknown >> Unknown >> Unknown | Unknown', 'Unknown', '7.0', '250.0 | Unknown', 'Unknown | Unknown', '100.0; 100.0', '8.0', 'Unknown >> Unknown | Unknown', '10.2', '20.0 | 30.0', '250.0', '0.369; 0.07 | Unknown', '50.0 | Unknown | Unknown | Unknown', '50.0 | Unknown | Unknown', 'Unknown | 0.1', '10.0 | 0.05 >> 0.1', '2.2; 2.2; 2.8', '0.15 | 0.3', 'Unknown >> Unknown >> Unknown >> Unknown', 'Unknown >> Unknown', '0.6; 0.4 >> 0.04', '30.0 | Unknown', '1.0', '1.0 | 1.0'])))

    deposition_reaction_solutions_age = Quantity(
        type=str,
        shape=[],
        description="""
    The age of the solutions
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the age of the solutions associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- As a general guideline, the age refers to the time from the preparation of the final precursor mixture to the reaction procedure.
- When the age of a solution is not known, state that as ‘nan’
- For reaction steps where no solvents are involved, state this as ‘nan’
- For solutions that is stored a long time, an order of magnitude estimate is adequate.
Example
2
0.25 |1000 >> 10000
nan | nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['0.0 | Unknown', '0.0 | 0.0', '0.0 | 1.0', '10.0', '0.5 | Unknown | Unknown', 'Unknown >> Unknown >> Unknown >> Unknown | Unknown', 'Unknown', 'Unknown | Unknown', '0.5 | Unknown | Unknown | Unknown', '8.0', 'Unknown >> Unknown | Unknown', '6.0', '0.0 | 6.0', 'Unknown >> Unknown >> Unknown | 12.0', '30.0', 'Unknown >> Unknown >> Unknown >> Unknown', 'Unknown >> Unknown', 'Unknown | Unknown >> 0.66', '1.0', '0.5 | 1000.0 >> 1000.0', '4.0'])))

    deposition_reaction_solutions_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature of the reaction solutions.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the temperatures of the solutions associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If a reaction solution undergoes a temperature program, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons, e.g. 25; 100
- When the temperature of a solution is unknown, state that as ‘nan’
- For reaction steps where no solvents are involved, state the temperature of the gas or the solid if that make sense. Otherwise state this as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- Assume an undetermined room temperature to be 25
Example
25
100; 50 | 25
nan | 25 >> 25
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Unknown | 300', '', '25', '25 | 25 >> 70 >> 25', '70 >> 25 >> 25', '40; ', '500 | 25', '70 | 25 >> 70', 'Unknown | Unknown >> Unknown | Unknown >> 70', '70', '40;  >> 40; ', '25 >> 70 >> 25 >> 25 | 25', '80', '25 | 25', 'Unknown', 'Unknown | Unknown', '100', '25 | 25 >> 25', '25 | 25 >> 70', '77', '25 | Unknown | Unknown', '70 | Unknown', 'Unknown >> Unknown | Unknown', 'Unknown >> 220 >> Unknown', 'Unknown | Unknown >> 70', '75', 'Unknown | 200', '25 | 25 >> 90', '25 | 80', '60', ' | 40; ', '25 | 70; 25', '150 | Unknown', '25 >> 70', 'Unknown >> 80', '60 | Unknown', '100 | 25', 'Unknown | 105', 'Unknown >> 80; 450 >> 150 >> 600 | Unknown', 'Unknown >> 80; 450', '25 | Unknown | Unknown | Unknown', 'Unknown | 450', '450', ' | 40;  >> 40; ', '230 | Unknown', '25 >> 70 | 25', '25 >> 70 | 25 | 25', 'Unknown >> 80; 450 >> 150 >> 600', '200 | Unknown', '25 >> 70 | Unknown', '450 | Unknown', '25 | Unknown'])))

    deposition_substrate_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperature of the substrate.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the temperatures of the substrates (i.e. the last deposited layer) associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The temperature of the substrate refers to the temperature when the deposition of the layer is occurring.
- If a substrate undergoes a temperature program before the deposition, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons (e.g. 25; 100)
- When the temperature of a substrate is not known, state that as ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- Assume that an undetermined room temperature is 25
Example
125; 325; 375; 450 | 25 >> 25
100
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=[' | 60', '450 >> 70 | 25', '25', '', '25 | 25 >> 70 >> 25', '300', '70 >> 25 >> 25', '60 | 25', '500 | 25', '70 | 25 >> 70', '70', '25 >> 70 >> 25 >> 25 | 25', '80', '25 | 25', '450 | 25 >> 25', 'Unknown', 'Unknown | Unknown', '100', '500 | 25 >> 25', '25 | 25 >> 70', '500', '450 | 95', '150', '77', '70 | Unknown', '450 | 25', '450 | 25 | 25', 'Unknown >> 220 >> Unknown', '25 | 25 | 25 | 25', '60', '25 | 25 >> 90', '70 | 25', '25 >> 70', '90', 'Unknown | Unknown >> Unknown | Unknown >> Unknown', '100 | 25', ' | 90 >> 90', '300 >> Unknown | Unknown', '450 | Unknown | Unknown', '450', 'Unknown | Unknown >> Unknown', '25 | 25 | 25', ' | 90', '90 >> 90', '455 >> Unknown', '500; 25', '455 | 25', '500 | 25 | 25', '455 | Unknown', 'Unknown | 120', '15 | 15', '25 | Unknown'])))

    deposition_thermal_annealing_temperature = Quantity(
        type=str,
        shape=[],
        description="""
    The temperatures of the thermal annealing program associated with depositing the layers
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the annealing temperatures associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the thermal annealing involves a temperature program with multiple temperature stages, list the temperatures (e.g. start, end, and other important points) and separate them with semicolons (e.g. 25; 100)
- For values with uncertainties, state the best estimate, e.g. write 120 and not 110-130.
- If no thermal annealing is occurring after the deposition of a layer, state that by stating the room temperature (assumed to 25°C if not further specified)
- If the thermal annealing program is not known, state that by ‘nan’
Example
450 | 125; 325; 375; 450 >> 125; 325; 375; 450
50 | 25
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['80 | Unknown', '100 >> 500 | 70', '25', ' | 60', '125 >> 500 | 500', '', '25 | 150 >> 500', '450 | 510', '500 >> 500 >> 500 | 500 >> 500 >> 500 >> 500 >> 500 >> 500 >> 500', '500 | 25', '80.0 | Unknown', '180', '135; 500 | 500', '400', '450 | 95; 350', 'Unknown | 125; 325; 375; 450; 500', 'Unknown | Unknown', '130', '450 | 150', '450 | 125; 375; 450 >> 450', '135; 500', '120 | 450', '125; 500 | Unknown', 'Unknown | 100', '160; 500', '150 >> 180', '25 | 80', '75', '500 | 500 >> 500', '420', '25 | 150', '125 >> 500 | 125 >> 500', '100 | 25', '450 | 100 >> 500', '500 | 70; 500', '450; 500 | 20 >> 500 >> 20', '500 | 150; 500', '455 | 100 >> 500', '90 >> 90', '100; 180', '400 | 400', '125 | 500 >> 25; 500', '501', '140', 'Unknown | 500', '130 | 70', '410', '450 | 125; 250; 350; 450; 500', '480 | 500', '160', '125 >> 500 | 125 >> 500 | 125 >> 500', ' | 90 >> 90', '100 >> 500 | 100 >> 500', '550', '450 | 100 >> 450', '450 | 25 | 500', '500 | 550', '450 | 125; 500', '500 | 70 >> 70 | 500 >> 500', '150 >> 500', '510 >> 70 >> 510 | 510', '25 | 325; 375; 450; 500', '70', '125 >> 450 | Unknown', '150 | 500 | 500 | 500', '550 | 550 >> 550', '500 | 125; 500', '500 | 550 >> 500', '200 | 25', '500 | 450 >> 450', 'Unknown | 125 >> 500', '100', '500 | 550 | Unknown >> Unknown >> Unknown >> 450', '100 >> 500 | 100 >> 125 >> 325 >> 375 >> 450 >> 500', '455 >> 100; 500', '500', '150 | 500', '90 | 50', '500 >> 70 >> 500 | 500', '165', '125 | 125; 500 | 25', '500 | Unknown', '125; 125', '100; 150; 185', '125; 150 >> 150; 190', '20', '150 >> 550', '25 >> 125; 500 | Unknown', '450 | 450 >> 150', '120 | 120', '450 | 120; 500', '120 >> 500 | 120 >> 500', '150 | 25', 'Unknown | 180', '300 >> 500 | 550', '60 | Unknown', '120 >> 500', '25 | 25 | 25', '250 | 250 | 250', '150 >> 290 >> 200 | 80', '125 | 125; 550 >> 25; 500', '550 | 300', '450 | 500 | 500', '120 >> 500 | 500', '125 | 500 >> 25 >> 500', '501 | 450', '25 >> 25 >> 500', '125 >> 500 >> 500', '125 >> 450 | 500', '500 | 70', '100; 185', '120 | 500', '455 | 100; 500', '25 | 25', '550 | 150', 'Unknown', '125 >> 450 | 125 >> 450', '500 | 125 >> 500', '500 >> 70 | 100; 500 >> 70 | 500', '500 | 500 | 25', '150', '500 | 450', '500 | 500 | 450', '25 | 480', '500 | 500', '500 | 25 | 400', '100 | 100', '125 | 500', '500 >> 500 | 500 | 25', '510 >> 25 >> 25 >> 510 | 510', '150 | 120', '200 | 150', '25 | 125 >> 500', '90', '180 >> 400 >> 450', '500 | 120', '25; 500', '25 >> 500 | 100; 500', '450 | 500 | 190', 'Unknown | 450', '500 | 110 >> 500', '450', '100 | 80', '80; 500 | 500', '150 | 150', '500; 25', '118 | 500 >> 500', '480', '150 >> 290 >> 200', '125 >> 125 >> 125; 500 | 120; 500', '300 | 500 | 400 | 100', '100 | Unknown', '185', '150; 500', '70 >> 180', '450 | 100', '25 | 125 >> 500 | 150 >> 500', '125 | 125; 500', '25 | 0', '100; 100', '165 | 100', '500 | 120 >> 500', '300', '150 | 100', '120 >> 500 | 150', '25 >> 25 >> 100', '450 | 500', '150 >> 500 | 125 >> 500', '25 | 500', '80', '170', '200', 'Unknown | 70; 500', '125 | 100; 550', '500 | 500 >> 450', '450 | 500 >> 450', '450 | 450', '120', '90 | Unknown', '500 >> 500 | Unknown', '110', '500 | 50', '25 | 500 | 500', '450 >> 450', '500 | 500 | 500', '25 | 500 >> 25; 500', '450 | 450 | Unknown', '80.0', '60', '510 | 540', '150 | Unknown', '125 >> 450', '450 | 500 | 400', '410 | 400', ' | 90', '150 | 450 >> 500', '100; 500', '450 | 125 >> 500', '100; 150; 185 | 100', '450 | 450 >> 500', '100; 150; 185 | 25', '450 | 450 | 450'])))

    deposition_thermal_annealing_time = Quantity(
        type=str,
        shape=[],
        description="""
    The time program associated to the thermal annealing program.
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the annealing times associated to each reaction step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- If the thermal annealing involves a temperature program with multiple temperature stages, list the associated times at those temperatures and separate them with semicolons.
- The annealing times must align in terms of layers¸ reaction steps and annealing temperatures in the previous filed.
- If a time is not known, state that by ‘nan’
- If no thermal annealing is occurring after the deposition of a layer, state that by ‘nan’
- For values with uncertainties, state the best estimate, e.g. write 20 and not 10-30.
Example
30 | 5; 5; 5; 30 >> 5; 5; 5; 30
60 | 1000
nan
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['5.0 | 30.0', '15.0 | 10.0', '90.0 | 90.0 >> 30.0', '30.0; 30.0 | 30.0', 'Unknown >> Unknown >> 60.0', '5.0 | 5.0; 60.0', '60.0; 60.0; 60.0 | Unknown', 'Unknown | Unknown | 40.0', '60.0 | 60.0', '30.0 | 10.0; 30.0', '5.0 | 5.0; 60.0 | Unknown', '60.0', '5.0', '0.0 | 30.0 | 30.0', '120.0', '45.0 | 5.0; 5.0; 30.0 >> 30.0', '180.0', 'Unknown | Unknown', '45.0', '120.0 | 30.0 >> 30.0', 'Unknown | 2.0', '210.0 >> 60.0 >> 60.0', '5.0 >> 5.0 >> 5.0; 30.0 | 5.0; 30.0', '20.0 >> 60.0 | 30.0 >> 5.0 >> 5.0 >> 5.0 >> 5.0 >> 15.0 >> 15.0', '20.0; 10.0', '10.0 | 180.0', 'Unknown | 5.0; 5.0; 5.0; 5.0', '30.0 | 30.0 | Unknown', '10.0 >> 30.0 | 30.0', '10.0 | 10.0', '30.0 | 30.0 | 1440.0', '2.0', '60.0 | 15.0; 60.0', '40.0 >> 10.0; 30.0', '5.0 | Unknown', 'Unknown >> 20.0 | 30.0', '5.0 >> 30.0', '30.0 | 30.0; Unknown', '15.0 | 15.0', '5.0 | 60.0 >> Unknown >> 60.0', '90.0 | 5.0 >> 5.0 | 90.0 >> 30.0', '5.0 >> 30.0 | 5.0 >> 30.0 | 5.0 >> 30.0', '60.0 | 60.0 | 60.0', '2.0 | 2.0', '4.0', '30.0 | 0.0', '40.0 | 10.0 >> 30.0', '60.0 | 10.0', '53.0 | 35.0', '30.0 | 30.0 | 60.0', '2.0 >> 30.0 >> 30.0', '60.0 | Unknown', '120.0 | 10.0 >> 30.0', '5.0 | 0.0', '10.0', 'Unknown >> 5.0; 30.0 | Unknown', '15.0 >> 30.0', '30.0 | 30.0', '25.0 | 5.0 >> 20.0', '10.0 >> 10.0 >> 10.0 | 5.0', '15.0 | 30.0', '12.0', '30.0 >> 40.0 >> 30.0 | 30.0', '25.0 | 25.0', '5.0 | 5.0; 120.0', 'Unknown | Unknown | Unknown', '10.0 >> 60.0 | 60.0', '30.0 >> Unknown >> Unknown >> 30.0 | 30.0', '5.0 >> 30.0 | Unknown', '10.0 >> 10.0 >> 10.0', 'Unknown | Unknown; 20.0', 'Unknown; Unknown', '5.0; 30.0 | Unknown', '2.0 | 30.0', 'Unknown >> 30.0 | 5.0; 30.0', '5.0 >> 60.0 | 60.0', '40.0 | 10.0; 30.0', '10.0 >> 60.0', '25.0 | 0.0', '0.0 | 0.0 | 0.0', '18.0 | 28.0 >> 28.0', '30.0 >> 30.0 | 30.0 | Unknown', '30.0 | 60.0 | Unknown >> Unknown >> Unknown >> 30.0', 'Unknown | 60.0', '45.0 | 45.0 >> 30.0', '35.0 | 10.0 >> 30.0', '30.0 | 10.0', '60.0; 60.0', '10.0 >> 120.0', '6.0 | 30.0', '5.0; 30.0 >> 5.0; 60.0', '120.0 | 30.0', '30.0 >> 60.0', 'Unknown; 500.0', '0.0 | 0.0', '30.0 | 15.0', '53.0', 'Unknown | 5.0; 5.0; 15.0; 15.0', 'Unknown | 30.0', '5.0 >> 30.0 | 5.0 >> 30.0', 'Unknown', '10.0 | 30.0', '20.0 | 20.0', '30.0 | 60.0 >> 30.0', 'Unknown | 10.0; 30.0', '30.0 | 20.0; 10.0; 10.0; 10.0; 30.0', '5.0 | 30.0 >> Unknown; 30.0', '20.0 | 60.0', '0.0 | 30.0', '5.0; 60.0', '80.0 | Unknown | 110.0', '10.0; 30.0 | 30.0', '30.0', '25.0 | 5.0 >> 30.0 | 5.0 >> 30.0', '30.0 | 40.0 | 40.0', '60.0 >> 60.0 | Unknown', '5.0 | 5.0; 60.0 >> Unknown; 30.0', '5.0 >> 30.0 | 30.0', '30.0 | Unknown', '25.0', '45.0 | 10.0', '100.0 | 15.0; 30.0', 'Unknown | Unknown >> 15.0', '30.0 >> 30.0', '20.0; 30.0', 'Unknown | Unknown; 30.0', '30.0 | 20.0', '10.0 | 10.0 | 10.0', '10.0 >> 30.0 | 10.0 >> 30.0', '10.0 | 30.0 >> 30.0', '30.0 | 30.0 | 30.0', '60.0 | 20.0', '30.0 | 5.0', '30.0 | 10.0 >> 30.0', 'Unknown | 20.0', '240.0 >> 60.0', '1440.0', 'Unknown >> Unknown >> 180.0', '25.0 | 500.0', '30.0 >> 30.0 >> 30.0 | 50.0', '20.0 | 10.0 >> 30.0', '15.0 >> 30.0 | 10.0 >> 30.0', '30.0 | 60.0', '60.0; 60.0; 60.0 | 10.0', '60.0 | 30.0 | 30.0', '420.0 >> 60.0 >> 60.0', '0.0 | 10.0 >> 30.0', '1.0 | 30.0 >> 30.0', 'Unknown | 30.0 >> Unknown; 30.0', '30.0 >> 30.0 | 30.0; 30.0 >> 30.0 | 30.0', '30.0 | 30.0 >> 30.0', '10.0 >> 30.0 | 10.0', '10.0 | Unknown', '10.0 | 10.0; 60.0', '30.0 | 30.0 >> Unknown', '10.0 | 30.0 | 30.0 | 30.0', '12.0 | Unknown', '20.0', '45.0; Unknown', '10.0 | 30.0 | 30.0 | 15.0', '10.0; 30.0', '60.0; 60.0; 60.0', 'Unknown | 15.0 >> 30.0', '300.0 >> 60.0 >> 60.0', '10.0 >> 10.0 >> 10.0 | 10.0 >> 10.0 >> 10.0 >> 10.0 >> 10.0 >> 10.0 >> 10.0', '0.0; 30.0', '15.0'])))

    deposition_thermal_annealing_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere during thermal annealing
- Every layer should be separated by a space, a vertical bar, and a space, i.e. (‘ | ‘)
- When more than one reaction step, separate the atmospheres associated to each annealing step by a double forward angel bracket with one blank space on both sides (‘ >> ‘)
- The number and order of layers and deposition steps must line up with the previous columns.
- If the atmosphere is a mixture of different gases, i.e. A and B, list the gases in alphabetic order and separate them with semicolons, as in (A; B)
- “Dry air” represent air with low relative humidity but where the relative humidity is not known
- “Ambient” represent air where the relative humidity is not known. For ambient conditions where the relative humidity is known, state this as “Air”
- “Vacuum” (of unspecified pressure) is for this purpose considered as an atmospheric gas.
- This is often the same as the atmosphere under which the deposition is occurring, but not always.
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example
N2
Vacuum | N2
Air | Ar >> Ar
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['N2', 'Air; Air; Air | N2', 'Ambient | Ambient | Ambient', 'Ambient | N2', 'Air | Air >> Air', 'Air | Air | Vacuum', 'Ambient | Unknown', 'Ambient >> Ambient | Ambient', 'Air; chlorobenzene', 'Unknown', 'Air; Air; Air', 'Air | N2', 'Unknown | Unknown', 'Vacuum >> Vacuum >> Unknown', 'Steam', 'N2 | N2', 'Ambient | Ambient >> Ambient | Ambient >> Ambient', 'Air | Air | Air', 'N2 | N2 | Vacuum', 'Ambient', 'Air | Air', 'Ambient | Ambient | Ambient >> Ambient >> Ambient >> Ambient', 'Unknown | Ambient', 'Ambient | Ambient >> Ambient', 'Air | Air | Air | Air', 'Dry air', 'Vacuum | Vacuum', 'Air', 'Dry air | Dry air', 'Ambient | Ambient', 'Ambient >> Ambient >> Ambient', 'Vacuum', 'Air | Ar', 'Dry air | Vacuum'])))

    storage_time_until_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    The time between the HTL stack is finalised and the next layer is deposited
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '1.0', '0.25', '0.1', '0.16', '0.3'])))

    storage_atmosphere = Quantity(
        type=str,
        shape=[],
        description="""
    The atmosphere in which the sample with the finalised HTL stack is stored until the next deposition step.
Example
Air
N2
Vacuum
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['Ar', 'N2', 'Unknown', 'Air'])))

    storage_relative_humidity = Quantity(
        type=str,
        shape=[],
        description="""
    The relive humidity under which the sample with the finalised HTL stack is stored until next deposition step
- If there are uncertainties, only state the best estimate, e.g. write 35 and not 20-50.
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', '40.0', '0.9', '30.0', '20.0'])))

    surface_treatment_before_next_deposition_step = Quantity(
        type=str,
        shape=[],
        description="""
    Description of any type of surface treatment or other treatment the sample with the finalised ETL-stack undergoes before the next deposition step.
- If more than one treatment, list the treatments and separate them by a double forward angel bracket (‘ >> ‘)
- If no special treatment, state that as ‘none’
- This category was included after the projects initial phase wherefor the list of reported categories is
short. Thus, be prepared to expand the given list of alternatives in the data template.
Example:
none
Ar plasma
                    """,
        a_eln=dict(
            component='EnumEditQuantity', props=dict(suggestions=['', 'Water', 'Plasma', 'ZnAl-LDH and thermal annealing', 'Ozone', 'UV', 'UV-Ozone', 'CO2', 'H2', 'He plasma', 'Washed with methanol', 'Wash with IPA', 'O2 plasma', 'Reactive ion etching'])))

    def normalize(self, archive, logger):
        add_solar_cell(archive)
        if self.stack_sequence:
            archive.results.properties.optoelectronic.solar_cell.electron_transport_layer = self.stack_sequence.split(' | ')

