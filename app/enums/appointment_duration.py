from enum import Enum 

class AppointmentDuration(Enum):
    ZERO_MINUTES = '0'        # Canceled appointments
    THIRTY_MINUTES = '30'
    SIXTY_MINUTES = '60'