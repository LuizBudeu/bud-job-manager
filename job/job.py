import sys
from datetime import datetime, timedelta
import asyncio
from typing import Callable, Any
import time
import logging

import settings
from job.job_status import JobStatus


class Job:
    def __init__(
        self,
        func_to_call: Callable,
        func_args: list[Any] | None = None,
        func_kwargs: dict[str, Any] | None = None,
        scheduled_time: datetime | None = None,
        is_async: bool = False,
        default_args: dict[str, Any] | None = None,
    ):
        self.func_to_call = func_to_call
        self.func_args = func_args if func_args else []
        self.func_kwargs = func_kwargs if func_kwargs else {}
        self.scheduled_time = scheduled_time
        self.result = None
        self.status = JobStatus.Scheduled  # Initial status is 'Scheduled'
        self.created_time = datetime.now()
        self.started_time = None
        self.completed_time = None
        self.is_async = is_async

        self.max_retries = 3  # Maximum number of retries for this job
        self.retry_count = 0   # Number of retries attempted
        # Default arguments for job-specific attributes
        default_job_args = {
            "max_retries": 3,
            "retry_count": 0,
            "retry_time": 5  # Default time (in seconds) to wait between retries
        }
        self.job_arguments = {**default_job_args, **(default_args or {})}

    async def execute_async(self):
        """
        Execute the job's function with the provided parameters asynchronously.
        """
        self.status = JobStatus.Running
        self.started_time = datetime.now()

        try:
            # Assuming func_to_call takes no arguments and is asynchronous
            self.result = await self.func_to_call(*self.func_args, **self.func_kwargs)
            self.status = JobStatus.Succeeded
            
            logging.info(f"Job {self} succeeded.")

        except KeyboardInterrupt:
            logging.error("Keyboard interrupt received. Stopping the job...")
            sys.exit()

        except Exception as e:
            # Handle any errors or exceptions during job execution
            self.status = JobStatus.Failed
            self.result = str(e)

            logging.error(f"Job failed with error: {e}")

            # Retry the job if the retry count is less than the maximum allowed retries
            if self.job_arguments["retry_count"] < self.job_arguments["max_retries"]:
                logging.info(f"Retrying job {self}..., attempt {self.job_arguments['retry_count'] + 1} / {self.job_arguments['max_retries']}")
                
                self.job_arguments["retry_count"] += 1
                await asyncio.sleep(self.job_arguments["retry_time"])  # Wait before retrying
                await self.execute_async()
        finally:
            self.completed_time = datetime.now()

    def execute_sync(self):
        """
        Execute the job's function with the provided parameters synchronously.
        """
        self.status = JobStatus.Running
        self.started_time = datetime.now()

        try:

            # Assuming func_to_call takes no arguments and is synchronous
            self.result = self.func_to_call(*self.func_args, **self.func_kwargs)
            self.status = JobStatus.Succeeded
            logging.info(f"Job {self} succeeded.")

        except Exception as e:
            # Handle any errors or exceptions during job execution
            self.status = JobStatus.Failed
            self.result = str(e)
            
            logging.error(f"Job failed with error: {e}")

            # Retry the job if the retry count is less than the maximum allowed retries
            if self.job_arguments["retry_count"] < self.job_arguments["max_retries"]:
                logging.info(f"Retrying job {self}...")
                
                self.job_arguments["retry_count"] += 1
                time.sleep(self.job_arguments["retry_time"])  # Wait before retrying
                self.execute_sync()

        finally:
            self.completed_time = datetime.now()

    def execute(self):
        """
        Execute the job based on its type (synchronous or asynchronous).
        """
        logging.info(f"Executing job {self} with params:\nargs={self.func_args} and kwargs={self.func_kwargs}")
        
        if self.is_async:
            return self.execute_async()
        else:
            return asyncio.to_thread(self.execute_sync)

    def to_dict(self):
        """
        Convert the Job instance to a dictionary for easy serialization and storage.
        """
        return {
            'func_to_call': self.func_to_call.__name__,
            'func_args': self.func_args,
            'func_kwargs': self.func_kwargs,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'result': self.result,
            'status': self.status,
            'created_time': self.created_time.isoformat(),
            'started_time': self.started_time.isoformat() if self.started_time else None,
            'completed_time': self.completed_time.isoformat() if self.completed_time else None,
            'max_retries': self.max_retries,
            'retry_count': self.retry_count,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Job instance from a dictionary representation.
        """
        job = cls(data['func_to_call'], data['func_args'], data['func_kwargs'])
        job.scheduled_time = datetime.fromisoformat(data['scheduled_time']) if data['scheduled_time'] else None
        job.result = data['result']
        job.status = data['status']
        job.created_time = datetime.fromisoformat(data['created_time'])
        job.started_time = datetime.fromisoformat(data['started_time']) if data['started_time'] else None
        job.completed_time = datetime.fromisoformat(data['completed_time']) if data['completed_time'] else None
        job.max_retries = data['max_retries']
        job.retry_count = data['retry_count']
        return job
    
    def __str__(self) -> str:
        return f"'{self.func_to_call.__name__}' with status '{self.status.value}'"
