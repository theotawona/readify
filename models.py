import datetime
from enum import StrEnum

from sqlmodel import SQLModel, Field, Relationship, create_engine

# Property Models

class PropertyType(StrEnum):
    residential = "Residential"
    commercial = "Commercial"

class PropertyBase(SQLModel):
    Name: str = Field(index=True)
    type: PropertyType = PropertyType.residential

class Property(PropertyBase,table=True):
    id: int|None = Field(default=None, primary_key=True)
    
    units: list["Unit"] = Relationship(back_populates="property")

class PropertyCreate(PropertyBase):
    pass 

class PropertyPublic(PropertyBase):
    id: int

class PropertyUpdate(SQLModel):
    Name:str|None = None

# Unit Models

class UnitBase(SQLModel):
    unit_number : str
    property_id : int = Field(foreign_key="property.id", index=True)

class Unit(UnitBase, table=True):
    id:int|None = Field(default=None, primary_key=True)

    property: Property = Relationship(back_populates="units")
    meters: list["Meter"]| None = Relationship(back_populates="unit")

class UnitCreate(UnitBase):
    pass 

class UnitPublic(UnitBase):
    id: int

class UnitUpdate(SQLModel):
    unit_number: str|None =None
    property_id: int|None = None

# Meter Models

class MeterType(StrEnum):
    cold_water = "Cold Water"
    hot_water = "Hot Water"

class MeterBase(SQLModel):
    meter_number: str
    type: MeterType
    unit_id: int = Field(foreign_key="unit.id", index=True)

class Meter(MeterBase, table=True):
    id: int|None = Field(default=None, primary_key=True)

    unit: Unit = Relationship(back_populates="meters")
    readings: list["Reading"]|None = Relationship(back_populates="meter") 

class MeterCreate(MeterBase):
    pass

class MeterPublic(MeterBase):
    id: int

class MeterUpdate(SQLModel):
    meter_number: str|None = None
    unit_id: int|None = None

#Reading Models

class ReadingBase(SQLModel):
    reading: float 
    Date : datetime.datetime|None = Field(default=None, nullable=True)
    meter_id : int = Field(foreign_key="meter.id", index=True)

class Reading(ReadingBase, table=True):
    id: int|None = Field(default=None, primary_key=True)

    meter: Meter = Relationship(back_populates="readings")

class ReadingCreate(ReadingBase):
    pass 

class ReadingPublic(ReadingBase):
    pass 

class ReadingUpdate(SQLModel):
    reading: float|None = None

