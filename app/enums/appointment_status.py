from enum import Enum

class AppointmentStatus(Enum):
    SCHEDULED = 'Scheduled'
    RESCHEDULED = 'Rescheduled'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
