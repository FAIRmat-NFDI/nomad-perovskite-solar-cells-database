import json
import os

SYNONYMS = {
    # Deposition method synonyms
    'Spin-coating': [
        'Spin-coating',
        'Spin coating',
        'One-step spin coating',
        'One-step spin-coating',
        'Intermittent spin-coating',
    ],
    'Thermal-annealing': ['Thermal-annealing', 'Thermal annealing'],
    'Doctor blading': [
        'Blade coating',
        'Blade-coating',
        'Doctor blading',
        'Doctor blade',
        'Doctor-blading',
        'Meniscus coating',
        'Meniscus-coating',
        'Meniscus-modulated blade coating',
    ],
    'CBD': [
        'Chemical bath deposition',
        'Chemical Bath Deposition',
        'Chemical-bath deposition',
        'Chemical bath',
        'Chemical bath co-deposition',
        'CBD',
    ],
    'Antisolvent-quenching': [
        'Antisolvent-quenching',
        'Antisolvent technique',
        'one-step anti-solvent method',
        'Antisolvent-fumigated',
    ],
    'Screen printing': ['Screen-printing', 'Screen printing'],
    'Slot-die coating': ['Slot-die coating', 'Slot die coating', 'Slot-die printing'],
    'Drop-infiltration': [
        'Drop-infiltration',
    ],
    'Sputtering': [
        'Sputtering',
    ],
    'Unknown': [
        'Unknown',
    ],
    'Spray coating': [
        'Spray coating',
    ],
    'Spray pyrolysis': [
        'Spray pyrolysis',
    ],
    'Atomic layer deposition': [
        'Atomic layer deposition',
        'ALD',
        'Atom layer deposition',
        'Atomic Layer Deposition',
    ],
    'Thermal evaporation': ['Thermal evaporation'],
    'Co-evaporation': ['Co-evaporation'],
    'Magnetron sputtering': ['Magnetron sputtering'],
    'Drop-casting': [
        'Drop-casting',
        'Drop casting',
        'Drop-coating',
        'Drop coating',
        'Dropcasting',
    ],
    'SILAR': ['SILAR'],
    'Gas quenching': ['Gas quenching'],
    'Sol-gel': ['Sol-gel'],
    'RF magnetron sputtering': ['RF magnetron sputtering'],
    'Inkjet printing': ['Inkjet printing'],
    'Hydrothermal': ['Hydrothermal'],
    'TiCl4 treatment': ['TiCl4 treatment'],
    'Air brush spray': [
        'Air brush spray',
        'Air-brush spray',
        'Airbrush spray',
        'air brush-spray',
    ],
    'Blow-drying': [
        'Blow drying',
        'Blow-drying',
    ],
    'Brush painting': [
        'Brush painting',
        'Brush-painting',
    ],
    'Closed space sublimation': [
        'Closed space sublimation',
        'Close space sublimation',
        'Closed-space sublimation',
    ],
    'Condensation': [
        'Condensation',
    ],
    'Crystallization': [
        'Crystallization',
        'Crystallisation',
    ],
    'CVD': [
        'CVD',
        'Chemical vapor deposition',
        'Chemical Vapor Deposition',
        'Chemical vapour deposition',
    ],
    'Diffusion': [
        'Diffusion',
    ],
    'Diffusion-gas reaction': [
        'Diffusion gas reaction',
        'Diffusion-gas reaction',
    ],
    'Dipp-coating': [
        'Dipp-coating',
        'Dip-coating',
        'Dip coating',
    ],
    'Dripping': [
        'Dripping',
    ],
    'Electrodeposition': [
        'Electrodeposition',
        'Electro-deposition',
    ],
    'Electrospinning': [
        'Electrospinning',
        'Electro-spinning',
    ],
    'Electrospraying': [
        'Electrospraying',
        'Electro-spraying',
    ],
    'Evaporation': [
        'Evaporation',
    ],
    'Flash evaporation': [
        'Flash evaporation',
        'Flash-evaporation',
    ],
    'Gas-assisted fast crystallisation': [
        'Gas-assisted fast crystallisation',
        'Gas-assisted fast crystallization',
        'Gas assisted fast crystallisation',
    ],
    'Gas reaction': [
        'Gas reaction',
        'Gas-reaction',
    ],
    'GC-LCG': [
        'GC-LCG',
        'GC LCG',
    ],
    'Hot-casting': [
        'Hot-casting',
        'Hot casting',
    ],
    'Hot-pressed': [
        'Hot-pressed',
        'Hot pressed',
        'Hot pressing',
    ],
    'Inverse temperature crystallization': [
        'Inverse temperature crystallization',
        'Inverse temperature crystallisation',
        'ITC',
    ],
    'Ion exchange': [
        'Ion exchange',
        'Ion-exchange',
    ],
    'Lamination': [
        'Lamination',
    ],
    'Ligand exchange': [
        'Ligand exchange',
        'Ligand-exchange',
    ],
    'Printing': [
        'Printing',
    ],
    'Pulsed laser deposition': [
        'Pulsed laser deposition',
        'PLD',
    ],
    'PVD': [
        'PVD',
        'Physical vapor deposition',
        'Physical vapour deposition',
    ],
    'Recrystallization': [
        'Recrystallization',
        'Recrystallisation',
    ],
    'Rinsing': [
        'Rinsing',
    ],
    'Roller-coating': [
        'Roller-coating',
        'Roller coating',
    ],
    'Sandwiching': [
        'Sandwiching',
    ],
    'Single crystal growth': [
        'Single crystal growth',
        'Single-crystal growth',
    ],
    'Single-source thermal evaporation': [
        'Single-source thermal evaporation',
        'Single source thermal evaporation',
    ],
    'Soft-cover deposition': [
        'Soft-cover deposition',
        'Soft cover deposition',
    ],
    'Solvent annealing': [
        'Solvent annealing',
        'Solvent-annealing',
    ],
    'Solvent evaporation crystallization': [
        'Solvent evaporation crystallization',
        'Solvent-evaporation crystallization',
        'Solvent evaporation crystallisation',
    ],
    'Space-confined single crystal formation': [
        'Space-confined single crystal formation',
        'Space confined single crystal formation',
    ],
    'Space-limited inverse temperature crystallization': [
        'Space-limited inverse temperature crystallization',
        'Space limited inverse temperature crystallization',
        'Space-limited ITC',
    ],
    'Substrate vibration assisted dropcasting': [
        'Substrate vibration assisted dropcasting',
        'Substrate-vibration-assisted dropcasting',
        'Substrate vibration-assisted drop casting',
    ],
    'Sulfurization': [
        'Sulfurization',
        'Sulphurization',
    ],
    'Ultrasonic spray': [
        'Ultrasonic spray',
        'Ultrasonic-spray',
    ],
    'Vacuum flash evaporation': [
        'Vacuum flash evaporation',
        'Vacuum-flash evaporation',
    ],
    'Vapour annealing': [
        'Vapour annealing',
        'Vapor annealing',
    ],
    'Washing': [
        'Washing',
    ],
    # Substrate synonyms
    'RF sputtering': ['RF sputtering'],
    'FTO': [
        'FTO',
        'FTO glass',
        'FTO/glass',
        'Glass/FTO',
        'FTO-30',
        'FTO-70',
        'FTO-50',
        'FTO-glass',
    ],
    'ITO': ['ITO', 'ITO glass', 'ITO/glass', 'Glass/ITO', 'ITO-glass'],
    'SLG': ['Glass', 'glass', 'SLG'],
    'Silicon': ['Silicon', 'Si', 'Si substrate', 'Silicon wafer', 'c-Si'],
    'p-type silicon': ['p-type silicon', 'p-type Cz silicon', 'p-Si', 'PSi'],
    'n-type silicon': ['n-type silicon', 'n-Si', 'n+Si'],
    'PEN/ITO': ['PEN/ITO', 'PEN-ITO', 'ITO-PEN', 'PEN/ITO strip'],
    'PET/ITO': ['PET/ITO', 'PET-ITO', 'ITO-PET'],
    # Contact synonyms
    'Au': [
        'Au',
        'Gold',
    ],
    'Ag': [
        'Ag',
        'Silver',
    ],
    'Carbon': [
        'Carbon',
        'C',
        'carbon',
        'Carbon paste',
        'Carbon electrode',
        'Carbon black electrode',
    ],
    'Carbon-mp': [
        'Carbon-mp',
        'mp-Carbon',
        'Carbon mesoporous',
        'm-Carbon',
        'm-carbon electrode',
        'porous carbon',
    ],
    'Cu': [
        'Cu',
        'Copper',
    ],
    # ETL synonyms
    'SnO2-c': [
        'SnO2',
        'SnO2-c',
        'SnOx',
        'c-SnO2',
        'ALD-SnO2',
        'SnO2-SnOx',
        'SnO2-x',
        'ALD-SnOx',
        'CBD-SnO2',
        'ALD SnOx',
        'Crystalline SnO2',
    ],
    'TiO2-c': [
        'TiO2-c',
        'TiO2',
        'c-TiO2',
        'Compact TiO2',
        'compact-TiO2',
        'cp-TiO2',
        'C-TiO2',
        'compact TiO2',
        'compacted TiO2',
        'TiO2 compact',
        'cTiO2',
        'TiO2 compact layer',
        'TiO2 CL',
        'Compact-TiO2',
    ],
    'C60': ['C60'],
    'PCBM-60': ['PCBM', 'PC60BM', 'PCBM-60'],
    'BCP': ['BCP'],
    'PC61BM': ['PC61BM'],
    'TiO2-mp': [
        'TiO2-mp',
        'mp-TiO2',
        'm-TiO2',
        'mesoporous TiO2',
        'TiO2 mesoporous',
        'Mesoporous TiO2',
        'mesoporous-TiO2',
        'meso-TiO2',
        'Mesoscopic TiO2',
        'mp TiO2',
        'ms-TiO2',
        'Meso.TiO2',
        'mpTiO2',
        'TiO2 scaffold',
        'M-TiO2',
        'Thin mp-TiO2',
    ],
    'TiO2-np': ['TiO2-np', 'TiO2-NPs'],
    'SnO2-np': [
        'SnO2-np',
        'SnO2 QD',
        'SnO2 QDs',
        'SnO2 NP',
        'SnO2 NPs',
        'np-SnO2',
        'QD-SnO2',
        'NP-SnO2',
        'SnO2 QDs-TQDs',
    ],
    'TiO2-bl': ['TiO2-bl', 'bl-TiO2', 'b-TiO2'],
    # HTL synonyms
    # === Organic HTLs ===
    'Spiro-OMeTAD': [
        'Spiro-OMeTAD',
        'spiro-OMeTAD',
        'Spiro-MeOTAD',
        'spiro-MeOTAD',
        'SpiroOMeTAD',
        'spiroOMeTAD',
        'spiroMeOTAD',
        'SpiroMeOTAD',
        'spiro-OMETAD',
        'spiro-OSMeTAD',
        'spiro-MEOTAD',
        'spiro-OMeTAD (doped)',
        'Commercial spiro-OMeTAD',
        'spiro-SMeTAD',
        'Spiro',
    ],
    'PTAA': ['PTAA'],
    'P3HT': ['P3HT'],
    # === Oxide HTLs ===
    'NiOx': ['NiOx', 'NiO', 'NiOX', 'NIO', 'nio', 'Nickel oxide'],
    # === Polymer / inorganic ===
    'PEDOT:PSS': ['PEDOT:PSS', 'PEDOT', 'PEDOT/PSS', 'PEDOT-PSS'],
    'CuSCN': ['CuSCN'],
    'Cu2O': ['Cu2O'],
    'CuI': ['CuI'],
    # === SAM families (PACz) ===
    '2PACz': [
        '2PACz',
        '2PACZ',
        '2Pacz',
        '2pacz',
        '2-PACz',
        '2-PACZ',
        '2-Pacz',
        '2-pacz',
        '2 PACz',
        '2 PACZ',
    ],
    'Me-2PACz': [
        'Me-2PACz',
        'Me 2PACz',
        'Me2PACz',
        'ME-2PACZ',
        'ME2PACZ',
        'me-2pacz',
        'Me-2Pacz',
        'Me-2PACZ',
        'Me2Pacz',
        'Me-2 Pacz',
    ],
    'MeO-2PACz': [
        'MeO-2PACz',
        'MeO 2PACz',
        'MeO2PACz',
        'MEO-2PACZ',
        'MEO2PACZ',
        'Meo-2PACz',
        'Meo2PACz',
        'MeO-2Pacz',
        'MeO-2PACZ',
        'Meo-2Pacz',
        'MeO-2PACz SAM',
    ],
    '4PACz': [
        '4PACz',
        '4PACZ',
        '4Pacz',
        '4pacz',
        '4-PACz',
        '4-PACZ',
        '4-Pacz',
        '4-pacz',
        '4 PACz',
        '4- PACZ',
    ],
    'Me-4PACz': [
        'Me-4PACz',
        'Me 4PACz',
        'Me4PACz',
        'ME-4PACZ',
        'ME4PACZ',
        'Me-4Pacz',
        'me-4pacz',
        'Me-4PACZ',
        '4PACz-Me',
        'Me-4 Pacz',
        'SAM_Me_4PACz',
    ],
    'MeO-4PACz': [
        'MeO-4PACz',
        'MeO 4PACz',
        'MeO4PACz',
        'MEO-4PACZ',
        'MEO4PACZ',
        'MeO-4Pacz',
        'Meo-4PACz',
        'Meo4PACz',
        'MeO-4PACZ',
    ],
    'Ph-4PACz': [
        'Ph-4PACz',
        'Ph 4PACz',
        'Ph4PACz',
        'PH-4PACZ',
        'PH4PACZ',
        'ph-4pacz',
        'Ph-4Pacz',
        'Ph-4PACZ',
        'ph- PACZ',
        'Ph-4pacz',
    ],
    'MePhpPACz': ['MePhpPACz', 'MEPHPPACZ', 'MePhpPacz', 'mephpPACZ'],
    '4PADCB': ['4PADCB'],
    # === Generic SAM (unspecified) ===
    'SAM': ['SAM'],
}


def main():
    synonym_map = {}
    for standard_name, synonym_list in SYNONYMS.items():
        if len(synonym_list) < 2:
            continue
        for synonym in synonym_list:
            synonym_map[synonym] = standard_name
    with open(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'src',
            'perovskite_solar_cell_database',
            'synonym_map.json',
        ),
        'w',
    ) as f:
        json.dump(synonym_map, f, indent=2)


if __name__ == '__main__':
    main()
