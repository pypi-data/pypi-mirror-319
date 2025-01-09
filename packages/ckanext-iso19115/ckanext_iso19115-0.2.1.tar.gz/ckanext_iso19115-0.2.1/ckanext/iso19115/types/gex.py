from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import *


@dataclass
class EX_Extent:
    description: Optional[gco.CharacterString] = None
    geographicElement: list[AbstractEX_GeographicExtent] = field(default_factory=list)
    temporalElement: list[EX_TemporalExtent] = field(default_factory=list)
    verticalElement: list[EX_VerticalExtent] = field(default_factory=list)


@dataclass
class EX_VerticalExtent:
    minimumValue: str
    maximumValue: str
    verticalCRSId: Optional[mrs.MD_ReferenceSystem] = None
    verticalCRS: Optional[gml.AbstractCRS] = None


@dataclass
class EX_TemporalExtent:
    extent: gml.AbstractTimePrimitive


@dataclass
class AbstractEX_GeographicExtent:
    extentTypeCode: Optional[gco.Boolean] = None


@dataclass
class EX_GeographicDescription(AbstractEX_GeographicExtent):
    geographicIdentifier: Optional[mcc.MD_Identifier] = None


@dataclass
class EX_BoundingPolygon(AbstractEX_GeographicExtent):
    polygon: list[gml.AbstractGeometry] = field(default_factory=list)


@dataclass
class EX_GeographicBoundingBox(AbstractEX_GeographicExtent):
    westBoundLongitude: Optional[gco.Decimal] = None
    eastBoundLongitude: Optional[gco.Decimal] = None
    southBoundLatitude: Optional[gco.Decimal] = None
    northBoundLatitude: Optional[gco.Decimal] = None
