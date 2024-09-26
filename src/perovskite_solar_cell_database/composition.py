#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import TYPE_CHECKING

from nomad.datamodel.data import EntryData, EntryDataCategory
from nomad.datamodel.datamodel import EntryArchive
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.datamodel.metainfo.basesections import (
    Component,
    CompositeSystem,
    PubChemPureSubstanceSection,
    PureSubstance,
    SystemComponent,
)
from nomad.metainfo.metainfo import (
    Category,
    MEnum,
    Package,
    Quantity,
    Reference,
    Section,
    SubSection,
)
from nomad.units import ureg
from structlog.stdlib import BoundLogger

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = Package()


class PerovskiteCompositionCategory(EntryDataCategory):
    m_def = Category(label='Perovskite Composition', categories=[EntryDataCategory])


class PerovskiteIon(PureSubstance):
    """
    Abstract class for describing a general perovskite ion.
    """

    m_def = Section()
    abbreviation = Quantity(
        type=str,
        description='The standard abbreviation of the ion. If the abbreviation is in the archive, additional data is complemented automatically',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    pure_substance = SubSection(
        section_def=PubChemPureSubstanceSection,
        description="""
        Section with properties describing the substance.
        """,
    )
    source_compound = SubSection(
        section_def=PubChemPureSubstanceSection,
        description="""
        Section with properties describing the substance.
        """,
    )


class PerovsktieAIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite A Ion',
    )


class PerovsktieBIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite B Ion',
    )


class PerovsktieCIon(PerovskiteIon, EntryData):
    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite C Ion',
    )


class PerovskiteIonComponent(SystemComponent):
    abbreviation = Quantity(
        type=str,
        description='The standard abbreviation of the ion. If the abbreviation is in the archive, additional data is complemented automatically',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    coefficient = Quantity(
        type=float,
        description='The stoichiometric coefficient',
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        shape=[],
    )
    common_name = Quantity(
        type=str,
        description='The common trade name of the ion',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    molecular_formula = Quantity(
        type=str,
        description='The molecular formula',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    smile = Quantity(
        type=str,
        description='The canonical SMILE string',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    iupac_name = Quantity(
        type=str,
        description='The standard IUPAC name',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    cas_number = Quantity(
        type=str,
        description='The CAS number if available',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_smile = Quantity(
        type=str,
        description='The canonical SMILE string',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_iupac_name = Quantity(
        type=str,
        description='The standard IUPAC name',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    source_compound_cas_number = Quantity(
        type=str,
        description='The CAS number if available',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        shape=[],
    )
    system = Quantity(
        type=Reference(PerovskiteIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `IonComponent` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)
        if not isinstance(self.system, PerovskiteIon):
            return
        if self.abbreviation is None:
            self.abbreviation = self.system.abbreviation
        if isinstance(self.system.pure_substance, PubChemPureSubstanceSection):
            if self.molecular_formula is None:
                self.molecular_formula = self.system.pure_substance.molecular_formula
            if self.smile is None:
                self.smile = self.system.pure_substance.smile
            if self.iupac_name is None:
                self.iupac_name = self.system.pure_substance.iupac_name
            if self.cas_number is None:
                self.cas_number = self.system.pure_substance.cas_number
        if isinstance(self.system.source_compound, PubChemPureSubstanceSection):
            if self.source_compound_smile is None:
                self.source_compound_smile = self.system.source_compound.smile
            if self.source_compound_iupac_name is None:
                self.source_compound_iupac_name = self.system.source_compound.iupac_name
            if self.source_compound_cas_number is None:
                self.source_compound_cas_number = self.system.source_compound.cas_number


class PerovskiteAIonComponent(PerovskiteIonComponent):
    system = Quantity(
        type=Reference(PerovsktieAIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )


class PerovskiteBIonComponent(PerovskiteIonComponent):
    system = Quantity(
        type=Reference(PerovsktieBIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )


class PerovskiteCIonComponent(PerovskiteIonComponent):
    system = Quantity(
        type=Reference(PerovsktieCIon.m_def),
        description='A reference to the component system.',
        a_eln=dict(component='ReferenceEditQuantity'),
    )


class PerovskiteComposition(CompositeSystem, EntryData):
    """
    Schema for describing a perovskite composition.
    """

    m_def = Section(
        categories=[PerovskiteCompositionCategory],
        label='Perovskite Composition',
    )
    short_form = Quantity(
        type=str,
    )
    long_form = Quantity(
        type=str,
    )
    composition_estimate = Quantity(
        type=MEnum(
            [
                'Estimated from precursor solutions',
                'Literature value',
                'Estimated from XRD data',
                'Estimated from spectroscopic data',
                'Theoretical simulation',
                'Hypothetical compound',
                'Other',
            ]
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    sample_type = Quantity(
        type=MEnum(
            [
                'Polycrystalline film',
                'Single crystal',
                'Quantum dots',
                'Nano rods',
                'Colloidal solution',
                'Amorphous',
                'Other',
            ]
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    dimensionality = Quantity(
        type=MEnum(['0D', '1D', '2D', '2D/3D', '3D', 'Other']),
        description='The dimensionality of the perovskite, i.e. 3D, 2D, 1D (nanorods), quantum dots (0D), etc.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
    )
    band_gap = Quantity(
        type=float,
        description='Band gap of photoabsorber in eV.',
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.NumberEditQuantity, defaultDisplayUnit='eV'
        ),
        unit='eV',
        shape=[],
    )
    a_ions = SubSection(
        section_def=PerovskiteAIonComponent,
        repeats=True,
    )
    b_ions = SubSection(
        section_def=PerovskiteBIonComponent,
        repeats=True,
    )
    c_ions = SubSection(
        section_def=PerovskiteCIonComponent,
        repeats=True,
    )
    impurities = SubSection(
        section_def=Component,
        repeats=True,
    )

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        The normalizer for the `PerovskiteComposition` class.

        Args:
            archive (EntryArchive): The archive containing the section that is being
            normalized.
            logger (BoundLogger): A structlog logger.
        """
        super().normalize(archive, logger)
        ions: list[PerovskiteIonComponent] = self.a_ions + self.b_ions + self.c_ions
        self.components = ions
        self.short_form = ''
        self.long_form = ''
        for ion in ions:
            if ion.abbreviation is not None and ion.coefficient is not None:
                self.short_form += f"{ion.abbreviation}{ion.coefficient:.2f}"


m_package.__init_metainfo__()
