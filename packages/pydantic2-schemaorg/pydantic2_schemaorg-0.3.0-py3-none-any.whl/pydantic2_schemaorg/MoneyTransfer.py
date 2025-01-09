from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic.v1 import StrictInt, StrictFloat
from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.TransferAction import TransferAction


class MoneyTransfer(TransferAction):
    """The act of transferring money from one place to another place. This may occur electronically or physically.

    See: https://schema.org/MoneyTransfer
    Model depth: 4
    """

    type_: str = Field(default="MoneyTransfer", alias="@type", const=True)
    amount: Optional[
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
        description="The amount of money.",
    )
    beneficiaryBank: Optional[
        Union[
            List[Union[str, "Text", "BankOrCreditUnion"]],
            str,
            "Text",
            "BankOrCreditUnion",
        ]
    ] = Field(
        default=None,
        description="A bank or bank’s branch, financial institution or international financial institution operating the beneficiary’s bank account or releasing funds for the beneficiary.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Number import Number
    from pydantic2_schemaorg.MonetaryAmount import MonetaryAmount
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.BankOrCreditUnion import BankOrCreditUnion
