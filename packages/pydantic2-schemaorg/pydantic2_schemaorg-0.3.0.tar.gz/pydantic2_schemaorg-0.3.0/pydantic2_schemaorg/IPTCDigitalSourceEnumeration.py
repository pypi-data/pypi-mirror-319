from __future__ import annotations


from pydantic.v1 import Field
from pydantic2_schemaorg.MediaEnumeration import MediaEnumeration


class IPTCDigitalSourceEnumeration(MediaEnumeration):
    """<a href=\"https://www.iptc.org/\">IPTC</a> \"Digital Source\" codes for use with the [[digitalSourceType]]
     property, providing information about the source for a digital media object. In general these codes are not
     declared here to be mutually exclusive, although some combinations would be contradictory if applied simultaneously,
     or might be considered mutually incompatible by upstream maintainers of the definitions. See the IPTC <a
     href=\"https://www.iptc.org/std/photometadata/documentation/userguide/\">documentation</a>
     for <a href=\"https://cv.iptc.org/newscodes/digitalsourcetype/\">detailed definitions</a> of all
     terms.

    See: https://schema.org/IPTCDigitalSourceEnumeration
    Model depth: 5
    """

    type_: str = Field(
        default="IPTCDigitalSourceEnumeration", alias="@type", const=True
    )
