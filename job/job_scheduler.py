import threading
from datetime import datetime, timedelta
import asyncio
import logging

from job.job import Job
import settings as settings
from job.job_status import JobStatus



class JobScheduler:
    def __init__(self):
        self.jobs: list[Job] = []
        self.lock = threading.Lock()
        self.stop_flag = False

    def add_job(self, job: Job):
        """
        Add a job to the scheduler.
        """
        with self.lock:
            self.jobs.append(job)
            logging.info(f"Added job {job} to the scheduler.")

    def remove_job(self, job: Job):
        """
        Remove a job from the scheduler.
        """
        with self.lock:
            self.jobs.remove(job)
            logging.info(f"Removed job {job} from the scheduler.")

    async def _execute_job(self, job: Job):
        """
        Execute a job and update its status asynchronously.
        """
        await job.execute()

    async def run(self):
        """
        Start the job scheduler and execute jobs as per their schedules asynchronously.
        """
        while not self.stop_flag:
            with self.lock:
                now = datetime.now()

                for job in self.jobs:

                    if job.status == JobStatus.Scheduled:
                        if job.scheduled_time is None:
                            # Execute the job asynchronously immediately
                            asyncio.create_task(self._execute_job(job))

                        elif job.scheduled_time <= now:
                            # Execute the job asynchronously
                            asyncio.create_task(self._execute_job(job))

            await asyncio.sleep(1)  # Sleep asynchronously for 1 second before checking again

    def start_scheduler(self):
        """
        Start the job scheduler in a background thread.
        """
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.start()
        logging.info("Job scheduler started.")

    def _run_scheduler(self):
        """
        Internal method to run the job scheduler in a loop.
        """
        asyncio.run(self.run())

    def stop(self):
        """
        Stop the job scheduler.
        """
        self.stop_flag = True
        self.scheduler_thread.join()
        logging.info("Job scheduler stopped.")
