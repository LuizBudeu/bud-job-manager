import asyncio

from job.job import Job


def job(default_args=None, scheduled_time=None, is_async=False):
    def decorator(func_to_decorate):
        def wrapper(*args, **kwargs):
            job_instance = Job(
                func_to_call=func_to_decorate,
                func_args=args,  # type: ignore
                func_kwargs=kwargs,
                scheduled_time=scheduled_time,
                is_async=is_async,
                default_args=default_args
            )
            if job_instance.is_async:
                return job_instance.execute_async()
            else:
                return asyncio.to_thread(job_instance.execute_sync)

        return wrapper

    return decorator
