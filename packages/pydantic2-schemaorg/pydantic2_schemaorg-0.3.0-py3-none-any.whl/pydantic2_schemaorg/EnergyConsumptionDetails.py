from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.Intangible import Intangible


class EnergyConsumptionDetails(Intangible):
    """EnergyConsumptionDetails represents information related to the energy efficiency of a product that consumes
     energy. The information that can be provided is based on international regulations such as for example [EU
     directive 2017/1369](https://eur-lex.europa.eu/eli/reg/2017/1369/oj) for energy labeling and the
     [Energy labeling rule](https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/energy-water-use-labeling-consumer)
     under the Energy Policy and Conservation Act (EPCA) in the US.

    See: https://schema.org/EnergyConsumptionDetails
    Model depth: 3
    """

    type_: str = Field(default="EnergyConsumptionDetails", alias="@type", const=True)
    energyEfficiencyScaleMin: Optional[
        Union[
            List[Union["EUEnergyEfficiencyEnumeration", str]],
            "EUEnergyEfficiencyEnumeration",
            str,
        ]
    ] = Field(
        default=None,
        description="Specifies the least energy efficient class on the regulated EU energy consumption scale for the product category a product belongs to. For example, energy consumption for televisions placed on the market after January 1, 2020 is scaled from D to A+++.",
    )
    hasEnergyEfficiencyCategory: Optional[
        Union[
            List[Union["EnergyEfficiencyEnumeration", str]],
            "EnergyEfficiencyEnumeration",
            str,
        ]
    ] = Field(
        default=None,
        description="Defines the energy efficiency Category (which could be either a rating out of range of values or a yes/no certification) for a product according to an international energy efficiency standard.",
    )
    energyEfficiencyScaleMax: Optional[
        Union[
            List[Union["EUEnergyEfficiencyEnumeration", str]],
            "EUEnergyEfficiencyEnumeration",
            str,
        ]
    ] = Field(
        default=None,
        description="Specifies the most energy efficient class on the regulated EU energy consumption scale for the product category a product belongs to. For example, energy consumption for televisions placed on the market after January 1, 2020 is scaled from D to A+++.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.EUEnergyEfficiencyEnumeration import (
        EUEnergyEfficiencyEnumeration,
    )
    from pydantic2_schemaorg.EnergyEfficiencyEnumeration import (
        EnergyEfficiencyEnumeration,
    )
