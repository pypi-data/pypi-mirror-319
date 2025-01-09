from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List, Optional, Union
from pydantic.v1 import AnyUrl


from pydantic.v1 import Field
from pydantic2_schemaorg.Review import Review


class MediaReview(Review):
    """A [[MediaReview]] is a more specialized form of Review dedicated to the evaluation of media content online,
     typically in the context of fact-checking and misinformation. For more general reviews of media in the broader
     sense, use [[UserReview]], [[CriticReview]] or other [[Review]] types. This definition is a work in progress.
     While the [[MediaManipulationRatingEnumeration]] list reflects significant community review amongst
     fact-checkers and others working to combat misinformation, the specific structures for representing media
     objects, their versions and publication context, are still evolving. Similarly, best practices for the
     relationship between [[MediaReview]] and [[ClaimReview]] markup have not yet been finalized.

    See: https://schema.org/MediaReview
    Model depth: 4
    """

    type_: str = Field(default="MediaReview", alias="@type", const=True)
    originalMediaContextDescription: Optional[
        Union[List[Union[str, "Text"]], str, "Text"]
    ] = Field(
        default=None,
        description="Describes, in a [[MediaReview]] when dealing with [[DecontextualizedContent]], background information that can contribute to better interpretation of the [[MediaObject]].",
    )
    originalMediaLink: Optional[
        Union[
            List[Union[AnyUrl, "URL", "MediaObject", "WebPage", str]],
            AnyUrl,
            "URL",
            "MediaObject",
            "WebPage",
            str,
        ]
    ] = Field(
        default=None,
        description="Link to the page containing an original version of the content, or directly to an online copy of the original [[MediaObject]] content, e.g. video file.",
    )
    mediaAuthenticityCategory: Optional[
        Union[
            List[Union["MediaManipulationRatingEnumeration", str]],
            "MediaManipulationRatingEnumeration",
            str,
        ]
    ] = Field(
        default=None,
        description="Indicates a MediaManipulationRatingEnumeration classification of a media object (in the context of how it was published or shared).",
    )


if TYPE_CHECKING:
    from pydantic2_schemaorg.Text import Text
    from pydantic2_schemaorg.URL import URL
    from pydantic2_schemaorg.MediaObject import MediaObject
    from pydantic2_schemaorg.WebPage import WebPage
    from pydantic2_schemaorg.MediaManipulationRatingEnumeration import (
        MediaManipulationRatingEnumeration,
    )
