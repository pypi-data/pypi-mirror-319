from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.Intangible import Intangible


class ItemList(Intangible):
    """A list of items of any sort&#x2014;for example, Top 10 Movies About Weathermen, or Top 100 Party Songs. Not
     to be confused with HTML lists, which are often used only for formatting.

    See: https://schema.org/ItemList
    Model depth: 3
    """

    type_: str = Field(default="ItemList", alias="@type", const=True)
    itemListElement: Optional[
        Union[
            List[Union[str, "Text", "Thing", "ListItem"]],
            str,
            "Text",
            "Thing",
            "ListItem",
        ]
    ] = Field(
        default=None,
        description='For itemListElement values, you can use simple strings (e.g. "Peter", "Paul", "Mary"), existing entities, or use ListItem. Text values are best if the elements in the list are plain strings. Existing entities are best for a simple, unordered list of existing things in your data. ListItem is used with ordered lists when you want to provide additional context about the element in that list or when the same item might be in different places in different lists. Note: The order of elements in your mark-up is not sufficient for indicating the order or elements. Use ListItem with a \'position\' property in such cases.',
    )
    numberOfItems: Optional[
        Union[List[Union[int, "Integer", str]], int, "Integer", str]
    ] = Field(
        default=None,
        description="The number of items in an ItemList. Note that some descriptions might not fully describe all items in a list (e.g., multi-page pagination); in such cases, the numberOfItems would be for the entire list.",
    )
    itemListOrder: Optional[
        Union[
            List[Union[str, "Text", "ItemListOrderType"]],
            str,
            "Text",
            "ItemListOrderType",
        ]
    ] = Field(
        default=None,
        description="Type of ordering (e.g. Ascending, Descending, Unordered).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Thing import Thing
    from pydantic2_schemaorg.ListItem import ListItem
    from pydantic2_schemaorg.Integer import Integer
    from pydantic2_schemaorg.ItemListOrderType import ItemListOrderType
