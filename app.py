from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from db import init_db, get_session

from models import (
    Property,
    PropertyCreate,
    PropertyPublic,
    PropertyUpdate,
    Unit,
    UnitPublic,
    UnitUpdate,
    UnitCreate,
    Meter,
    MeterPublic,
    MeterUpdate,
    MeterCreate,
    Reading,
    ReadingPublic,
    ReadingUpdate,
    ReadingCreate

)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Property Endpoints
@app.post("/properties", response_model=PropertyPublic, status_code=201)
async def create_property(*,session:Session =Depends(get_session),
                          property:PropertyCreate):
    db_property = Property.model_validate(property)
    session.add(db_property)
    session.commit()
    session.refresh(db_property)
    return db_property

@app.get("/properties", response_model=list[PropertyPublic])
async def read_properties(*, session:Session = Depends(get_session)):
    properties = session.exec(select(Property)).all()
    return properties

@app.get("/properties/{property_id}", response_model=PropertyPublic)
async def read_single_property(*, session:Session=Depends(get_session), 
                               property_id:int):
    db_property = session.get(Property, property_id)
    if not db_property:
        return HTTPException(status_code=404, detail="Property Not Found")
    return db_property

@app.patch("/properties/{property_id}", response_model=PropertyPublic)
async def update_property(*, session:Session=Depends(get_session),
                          property_id:int, property:PropertyUpdate):
    db_property = session.get(Property, property_id)
    if not db_property:
        return HTTPException(status_code=404, detail="Property Not Found")
    new_db_property_data = property.model_dump(exclude_unset=True)
    db_property.sqlmodel_update(new_db_property_data)
    session.add(db_property)
    session.commit()
    session.refresh(db_property)
    return db_property

@app.delete("/properties/{property_id}")
async def delete_property(*, session:Session=Depends(get_session),
                          property_id:int):
    db_property = session.get(Property, property_id)
    if not db_property:
        return HTTPException(status_code=404, detail="Property Not Found")
    session.delete(db_property)
    session.commit()
    return {"message": "Property Deleted Successfully"}

# Unit Endpoints

@app.post("/properties/{property_id}/units", response_model=UnitPublic, status_code=201)
async def create_unit(*, session:Session=Depends(get_session), property_id: int, unit:UnitCreate):
    db_property = session.get(Property, property_id)
    if not db_property:
        raise HTTPException(status_code=404, detail="Property Not Found")
    db_unit = Unit(unit_number=unit.unit_number)
    db_unit.property = db_property
    session.add(db_unit)
    session.commit()
    session.refresh(db_unit)
    return db_unit

@app.get("/properties/{property_id}/units", response_model=list[UnitPublic])
async def read_units(*, session:Session=Depends(get_session), property_id:int):
    db_units = session.exec(select(Unit).where(Unit.property_id == property_id)).all()
    return db_units

@app.get("/properties/{property_id}/units/{unit_id}", response_model=UnitPublic)
async def read_single_unit(*, session:Session=Depends(get_session), property_id:int, unit_id:int):
    db_unit = session.exec(select(Unit).where(Unit.property_id == property_id).where(Unit.id == unit_id)).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit Not Found")
    return db_unit

@app.delete("/properties/{property_id}/units/{unit_id}", response_model=UnitPublic)
async def delete_unit(*, session:Session=Depends(get_session), property_id:int, unit_id:int):
    db_unit = session.exec(select(Unit).where(Unit.property_id == property_id).where(Unit.id == unit_id)).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit Not Found")
    session.delete(db_unit)
    session.commit()
    return {"message": "Unit deleted successfully"}

    
# Meter Endpoints

@app.post("/properties/{property_id}/units/{unit_id}/meters", response_model=MeterPublic)
async def create_meter(*, session:Session=Depends(get_session), property_id:int, unit_id:int, meter:MeterCreate):
    db_unit = session.exec(select(Unit).where(Unit.property_id == property_id).where(Unit.id == unit_id)).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit Not Found")
    db_meter = Meter(meter_number=meter.meter_number, type=meter.type)
    db_meter.unit = db_unit
    session.add(db_meter)
    session.commit()
    session.refresh(db_meter)
    return db_meter

@app.get("/properties/{property_id}/units/{unit_id}/meters", response_model=list[MeterPublic])
async def get_meters(*, session:Session=Depends(get_session), property_id:int, unit_id:int):
    db_unit = session.exec(select(Unit).where(Unit.property_id == property_id).where(Unit.id == unit_id)).first()
    meters = session.exec(select(Meter).where(Meter.unit == db_unit)).all()
    if not meters:
        raise HTTPException(status_code=404, detail="Meters Not Found")
    return meters

# Reading End points

@app.post("/meters/{meter_id}/readings", response_model=ReadingPublic)
async def create_reading(*, session:Session=Depends(get_session),
                         meter_id:int, reading:ReadingCreate):
    meter = session.exec(select(Meter).where(Meter.id == meter_id)).first()
    if not meter:
        raise HTTPException(status_code=404, detail="Meter Not Found")
    db_reading = Reading(reading=reading.reading)
    db_reading.meter = meter
    session.add(db_reading)
    session.commit()
    session.refresh(db_reading)
    return db_reading

