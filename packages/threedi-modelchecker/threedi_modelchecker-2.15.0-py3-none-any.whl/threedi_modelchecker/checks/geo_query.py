from geoalchemy2 import functions as geo_func
from sqlalchemy import func
from sqlalchemy.orm import Query
from sqlalchemy.sql import literal
from threedi_schema import models

DEFAULT_EPSG = 28992


def epsg_code_query():
    epsg_code = Query(models.ModelSettings.epsg_code).limit(1).scalar_subquery()
    return func.coalesce(epsg_code, literal(DEFAULT_EPSG)).label("epsg_code")


def transform(col):
    return geo_func.ST_Transform(col, epsg_code_query())


def distance(col_1, col_2):
    return geo_func.ST_Distance(transform(col_1), transform(col_2))


def length(col):
    return geo_func.ST_Length(transform(col))
