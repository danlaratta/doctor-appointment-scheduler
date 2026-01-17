from enum import Enum

class AppointmentStatus(Enum):
    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
