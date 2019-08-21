from api.models import Flight
from api.schemas import FlightSchema

from .base import BaseListResource


class FlightList(BaseListResource):
    model = Flight
    schema_class = FlightSchema
