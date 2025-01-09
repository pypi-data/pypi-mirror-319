from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union
from pydantic.v1 import StrictInt, StrictFloat


from pydantic.v1 import Field
from pydantic2_schemaorg.PhysicalActivity import PhysicalActivity
from pydantic2_schemaorg.CreativeWork import CreativeWork


class ExercisePlan(PhysicalActivity, CreativeWork):
    """Fitness-related activity designed for a specific health-related purpose, including defined exercise
     routines as well as activity prescribed by a clinician.

    See: https://schema.org/ExercisePlan
    Model depth: 3
    """

    type_: str = Field(default="ExercisePlan", alias="@type", const=True)
    restPeriods: Optional[
        Union[
            List[Union[str, "Text", "QuantitativeValue"]],
            str,
            "Text",
            "QuantitativeValue",
        ]
    ] = Field(
        default=None,
        description="How often one should break from the activity.",
    )
    workload: Optional[
        Union[
            List[Union["Energy", "QuantitativeValue", str]],
            "Energy",
            "QuantitativeValue",
            str,
        ]
    ] = Field(
        default=None,
        description="Quantitative measure of the physiologic output of the exercise; also referred to as energy expenditure.",
    )
    repetitions: Optional[
        Union[
            List[Union[StrictInt, StrictFloat, "Number", "QuantitativeValue", str]],
            StrictInt,
            StrictFloat,
            "Number",
            "QuantitativeValue",
            str,
        ]
    ] = Field(
        default=None,
        description="Number of times one should repeat the activity.",
    )
    intensity: Optional[
        Union[
            List[Union[str, "Text", "QuantitativeValue"]],
            str,
            "Text",
            "QuantitativeValue",
        ]
    ] = Field(
        default=None,
        description="Quantitative measure gauging the degree of force involved in the exercise, for example, heartbeats per minute. May include the velocity of the movement.",
    )
    activityFrequency: Optional[
        Union[
            List[Union[str, "Text", "QuantitativeValue"]],
            str,
            "Text",
            "QuantitativeValue",
        ]
    ] = Field(
        default=None,
        description="How often one should engage in the activity.",
    )
    activityDuration: Optional[
        Union[
            List[Union["Duration", "QuantitativeValue", str]],
            "Duration",
            "QuantitativeValue",
            str,
        ]
    ] = Field(
        default=None,
        description="Length of time to engage in the activity.",
    )
    exerciseType: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="Type(s) of exercise or activity, such as strength training, flexibility training, aerobics, cardiac rehabilitation, etc.",
    )
    additionalVariable: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="Any additional component of the exercise prescription that may need to be articulated to the patient. This may include the order of exercises, the number of repetitions of movement, quantitative distance, progressions over time, etc.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.QuantitativeValue import QuantitativeValue
    from pydantic2_schemaorg.Energy import Energy
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.Duration import Duration
