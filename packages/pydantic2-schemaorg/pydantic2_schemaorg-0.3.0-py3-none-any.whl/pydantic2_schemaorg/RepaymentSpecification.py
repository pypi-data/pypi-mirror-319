from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union
from pydantic.v1 import StrictInt, StrictFloat


from pydantic.v1 import Field
from pydantic2_schemaorg.StructuredValue import StructuredValue


class RepaymentSpecification(StructuredValue):
    """A structured value representing repayment.

    See: https://schema.org/RepaymentSpecification
    Model depth: 4
    """

    type_: str = Field(default="RepaymentSpecification", alias="@type", const=True)
    loanPaymentAmount: Optional[
        Union[List[Union["MonetaryAmount", str]], "MonetaryAmount", str]
    ] = Field(
        default=None,
        description="The amount of money to pay in a single payment.",
    )
    downPayment: Optional[
        Union[
            List[Union[StrictInt, StrictFloat, "Number", "MonetaryAmount", str]],
            StrictInt,
            StrictFloat,
            "Number",
            "MonetaryAmount",
            str,
        ]
    ] = Field(
        default=None,
        description="a type of payment made in cash during the onset of the purchase of an expensive good/service. The payment typically represents only a percentage of the full purchase price.",
    )
    numberOfLoanPayments: Optional[
        Union[
            List[Union[StrictInt, StrictFloat, "Number", str]],
            StrictInt,
            StrictFloat,
            "Number",
            str,
        ]
    ] = Field(
        default=None,
        description="The number of payments contractually required at origination to repay the loan. For monthly paying loans this is the number of months from the contractual first payment date to the maturity date.",
    )
    loanPaymentFrequency: Optional[
        Union[
            List[Union[StrictInt, StrictFloat, "Number", str]],
            StrictInt,
            StrictFloat,
            "Number",
            str,
        ]
    ] = Field(
        default=None,
        description="Frequency of payments due, i.e. number of months between payments. This is defined as a frequency, i.e. the reciprocal of a period of time.",
    )
    earlyPrepaymentPenalty: Optional[
        Union[List[Union["MonetaryAmount", str]], "MonetaryAmount", str]
    ] = Field(
        default=None,
        description="The amount to be paid as a penalty in the event of early payment of the loan.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
    from pydantic2_schemaorg.Number import Number
