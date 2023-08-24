import functools
import time
import schedule
import threading


# This decorator can be applied to any job function to log the elapsed time of each job
def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed in %d seconds' % (func.__name__, time.time() - start_timestamp))
        return result

    return wrapper

# this decorator can be applied to any job function to catch any exceptions that may be raised during the job
def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@print_elapsed_time
@catch_exceptions(cancel_on_failure=True)
def job(argument1, argument2):
    print(f"argument1: {argument1}, argument2: {argument2}")

@print_elapsed_time
@catch_exceptions(cancel_on_failure=True)
def job_that_executes_once():
    
    with open("test.txt", "a+") as f:
        f.write(f"{time.time()}\n")
    
    return schedule.CancelJob

@print_elapsed_time
@catch_exceptions(cancel_on_failure=True)
def error_job():
    print(1/0)

@print_elapsed_time
@catch_exceptions(cancel_on_failure=True)
def background_job():
    print('Hello from the background thread')

def run_continuously(interval=1):

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


if __name__ == '__main__':
    # Run the job every 3 seconds
    # schedule.every(3).seconds.do(job, argument1='hello', argument2='world')
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    
    # Run the job once
    # schedule.every().second.do(error_job)
    # schedule.run_all()
    # schedule.clear()
    
    # get the number of seconds until the next job is scheduled to run
    # schedule.every().seconds.do(error_job)
    # while 1:
    #     n = schedule.idle_seconds()
    #     print(f"n: {n}")
    #     if n is None:
    #         # no more jobs
    #         break
    #     elif n > 0:
    #         # sleep exactly the right amount of time
    #         time.sleep(n)
    #     schedule.run_pending()
    

    schedule.every().second.do(background_job)

    # Start the background thread
    stop_run_continuously = run_continuously()
    
    # task main thread do here
    print("task main thread do here")
    time.sleep(5)
    
    # Stop the background thread
    stop_run_continuously.set()
    