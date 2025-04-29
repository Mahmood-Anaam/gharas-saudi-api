# =======================
# ## Plant Pydantic
# =======================
from typing import List
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
    precip:      List[ClimateCategory]    = Field(..., description="Precipitation tolerance categories")
    soil:        List[SoilType]           = Field(..., description="Preferred soil types")
