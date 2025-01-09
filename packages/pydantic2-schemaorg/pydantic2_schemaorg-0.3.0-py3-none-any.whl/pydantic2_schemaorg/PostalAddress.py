from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union


from pydantic.v1 import Field
from pydantic2_schemaorg.ContactPoint import ContactPoint


class PostalAddress(ContactPoint):
    """The mailing address.

    See: https://schema.org/PostalAddress
    Model depth: 5
    """

    type_: str = Field(default="PostalAddress", alias="@type", const=True)
    addressCountry: Optional[
        Union[List[Union[str, "Text", "Country"]], str, "Text", "Country"]
    ] = Field(
        default=None,
        description="The country. For example, USA. You can also provide the two-letter [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1).",
    )
    postalCode: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The postal code. For example, 94043.",
    )
    streetAddress: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The street address. For example, 1600 Amphitheatre Pkwy.",
    )
    addressLocality: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The locality in which the street address is, and which is in the region. For example, Mountain View.",
    )
    postOfficeBoxNumber: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The post office box number for PO box addresses.",
    )
    addressRegion: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The region in which the locality is, and which is in the country. For example, California or another appropriate first-level [Administrative division](https://en.wikipedia.org/wiki/List_of_administrative_divisions_by_country).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.Country import Country
