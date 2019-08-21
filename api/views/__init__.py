from .auth import Register, Login
from .photos import PhotoUpload
from .flight import FlightList

URLS = (
    (Register, '/auth/register'),
    (Login, '/auth/login'),
    (PhotoUpload, '/user/photo'),
    (FlightList, '/flights')
)
