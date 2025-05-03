from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
import enum

class ClimateCategory(str, enum.Enum):
    VERY_LOW  = "Very Low"
    LOW       = "Low"
    MODERATE  = "Moderate"
    HIGH      = "High"
    EXTREME   = "Extreme"

class PlantType(str, enum.Enum):
    TREE                 = "Tree"
    SHRUB                = "Shrub"
    SUCCULENT            = "Succulent Plant"
    SUCCULENT_SHRUB      = "Succulent Shrub"
    HERBACEOUS_PERENNIAL = "Herbaceous perennial"
    ELEGANT_PLANT        = "Elegant Plant"


class SoilType(str, enum.Enum):
    SANDY        = "Sandy"
    SANDY_LOAM   = "Sandy-Loam"
    CALCAREOUS   = "Calcareous"
    GYPSIFEROUS  = "Gypsiferous"
    SALINE       = "Saline"
    CLAY_LOAM    = "Clay-Loam"
    SILT_LOAM    = "Silt-Loam"

class Plant(BaseModel):
    name:        str                      = Field(..., description="Common English name")
    type:        PlantType                = Field(..., description="Growth form of the plant")
    temperature: List[ClimateCategory]    = Field(..., description="Temperature tolerance categories")
    humidity:    List[ClimateCategory]    = Field(..., description="Humidity tolerance categories")
    # precip:      List[ClimateCategory]    = Field(..., description="Precipitation tolerance categories")
    soil:        List[SoilType]           = Field(..., description="Preferred soil types")

class Weather(BaseModel):
    temp: float = Field(...,description="Temperature in Celsius")
    humidity: float = Field(...,description="Humidity percentage (0-100)")
    region: str = Field(..., description="Name of the region/location")
    soil: SoilType = Field(..., description="Predominant soil type")
    

class RecommendationRequest(BaseModel):
    lat:   Annotated[float, Field(ge=-90,  le=90,  description="Latitude in degrees")]
    lon:   Annotated[float, Field(ge=-180, le=180, description="Longitude in degrees")]
    month: Annotated[Optional[int], Field(ge=1, le=12,
            description="Month number 1-12; if omitted, the current month is used.")] = None
    limit: Annotated[int, Field(ge=1, le=100,
            description="Maximum number of plants to return")] = 10


class RecommendationResponse(BaseModel):
    recommendations: List[Plant]
    weather: Weather