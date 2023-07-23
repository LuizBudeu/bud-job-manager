from enum import Enum


class JobStatus(Enum):
    Scheduled = "Scheduled"
    Running = "Running"
    Succeeded = "Succeeded"
    Failed = "Failed"
    Cancelled = "Cancelled"
    Unknown = "Unknown"