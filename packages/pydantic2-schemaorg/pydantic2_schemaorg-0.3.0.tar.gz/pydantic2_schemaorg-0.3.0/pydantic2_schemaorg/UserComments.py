from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union
from datetime import date, datetime
from pydantic.v1 import AnyUrl


from pydantic.v1 import Field
from pydantic2_schemaorg.UserInteraction import UserInteraction


class UserComments(UserInteraction):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally
     better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    See: https://schema.org/UserComments
    Model depth: 4
    """

    type_: str = Field(default="UserComments", alias="@type", const=True)
    creator: Optional[
        Union[List[Union["Person", "Organization", str]], "Person", "Organization", str]
    ] = Field(
        default=None,
        description="The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork.",
    )
    discusses: Optional[
        Union[List[Union["CreativeWork", str]], "CreativeWork", str]
    ] = Field(
        default=None,
        description="Specifies the CreativeWork associated with the UserComment.",
    )
    commentTime: Optional[
        Union[
            List[Union[datetime, "DateTime", date, "Date", str]],
            datetime,
            "DateTime",
            date,
            "Date",
            str,
        ]
    ] = Field(
        default=None,
        description="The time at which the UserComment was made.",
    )
    commentText: Optional[Union[List[Union[str, "Text"]], str, "Text"]] = Field(
        default=None,
        description="The text of the UserComment.",
    )
    replyToUrl: Optional[Union[List[Union[AnyUrl, "URL", str]], AnyUrl, "URL", str]] = (
        Field(
            default=None,
            description="The URL at which a reply may be posted to the specified UserComment.",
        )
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Person import Person
    from pydantic2_schemaorg.Organization import Organization
    from pydantic2_schemaorg.CreativeWork import CreativeWork
    from pydantic2_schemaorg.DateTime import DateTime
    from pydantic2_schemaorg.Date import Date
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.URL import URL
