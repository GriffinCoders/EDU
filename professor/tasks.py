from celery import Celery
from celery import shared_task

@shared_task
def add(x, y):
    return x + y

"""Test Celery With a Custom add Function"""

# Create your tests here.
from concurrent.futures import ThreadPoolExecutor, as_completed
from professor.tasks import add

# Number of tasks to run concurrently
num_tasks = 5

# Arguments to pass to each task
task_arguments = [(i, i) for i in range(num_tasks)]

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_tasks) as executor:
    # Submit each task to the executor
    futures = [executor.submit(add.delay, *args) for args in task_arguments]

    # Wait for all tasks to complete
    for future in as_completed(futures):
        result = future.result()
        print(f"Result: {result}")
