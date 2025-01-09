from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.Product import Product


class ProductGroup(Product):
    """A ProductGroup represents a group of [[Product]]s that vary only in certain well-described ways, such as
     by [[size]], [[color]], [[material]] etc. While a ProductGroup itself is not directly offered for sale,
     the various varying products that it represents can be. The ProductGroup serves as a prototype or template,
     standing in for all of the products who have an [[isVariantOf]] relationship to it. As such, properties (including
     additional types) can be applied to the ProductGroup to represent characteristics shared by each of the (possibly
     very many) variants. Properties that reference a ProductGroup are not included in this mechanism; neither
     are the following specific properties [[variesBy]], [[hasVariant]], [[url]].

    See: https://schema.org/ProductGroup
    Model depth: 3
    """

    type_: str = Field(default="ProductGroup", alias="@type", const=True)
    hasVariant: Optional[Union[List[Union["Product", str]], "Product", str]] = Field(
        default=None,
        description="Indicates a [[Product]] that is a member of this [[ProductGroup]] (or [[ProductModel]]).",
    )
    variesBy: Optional[
        Union[List[Union[str, "Text", "DefinedTerm"]], str, "Text", "DefinedTerm"]
    ] = Field(
        default=None,
        description='Indicates the property or properties by which the variants in a [[ProductGroup]] vary, e.g. their size, color etc. Schema.org properties can be referenced by their short name e.g. "color"; terms defined elsewhere can be referenced with their URIs.',
    )
    productGroupID: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="Indicates a textual identifier for a ProductGroup.",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Product import Product
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.DefinedTerm import DefinedTerm
