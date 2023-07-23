from datetime import datetime, timedelta
import time
import asyncio
import logging

from job.job_scheduler import JobScheduler
from job.job import Job
from job.decorators.job import job
from job.funcs import synchronous_function, asynchronous_function


if __name__ == "__main__":
   # Create the job scheduler
    job_scheduler = JobScheduler()

    # Create and add jobs to the scheduler
    sync_job = Job(
        func_to_call=synchronous_function, func_args=["Hello, World!"],
        scheduled_time=datetime.now() + timedelta(minutes=1),
        is_async=False)

    async_job = Job(
        func_to_call=asynchronous_function, func_args=["Hello, Async!"],
        is_async=True,
        default_args={
            "max_retries": 5,
            "retry_time": 10
        })

    job_scheduler.add_job(sync_job)
    job_scheduler.add_job(async_job)
    
    try:
        # Start the job scheduler in the background
        job_scheduler.start_scheduler()
        
        time.sleep(300)

    except KeyboardInterrupt:
        logging.error("Keyboard interrupt received. Stopping the program...")

    # Stop the job scheduler and quit the program when needed
    job_scheduler.stop()
