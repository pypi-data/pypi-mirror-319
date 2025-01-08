# django-task

django-task is a library designed to assist you in tracking Celery tasks within your Django project. It provides a seamless integration with your current database and offers RESTful APIs for managing and monitoring your tasks.

## Features

- **Task Tracking:** With django-task, you can easily track the status, progress, and result of your Celery tasks. The library stores this information in your database, allowing you to retrieve and analyze task data at any time.

- **RESTful APIs:** django-task exposes a set of RESTful APIs that enable you to interact with your Celery tasks programmatically. You can create, update, delete, and retrieve tasks using these APIs, providing flexibility in managing your task workflow.

- **Integration with Celery:** This library seamlessly integrates with Celery, a widely-used distributed task queue framework. You can use all the powerful features of Celery, such as task scheduling, distributed processing, and task retries, while leveraging django-task for task tracking and management.

## Installation

You can install django-task using pip:

```
pip install django-task
```

Make sure you have Celery and Django installed as well.

## Usage

Once installed and configured, you can start tracking your Celery tasks using django-task. Here's a basic example of how to use the library:

```python
from django_task.handlers import TaskHandler

# Create a new task
@celery_app.task(
    name="some_task", queue="default_queue", base=TaskHandler
)
def some_task(bulk_account_data, *args, **kwargs):
    pass
```

Using this annotation, you can track the task status in your db.

For detailed usage instructions and available APIs, please refer to the [documentation](https://github.com/abhishm20/django-task).

## Contributing

Contributions to django-task are welcome! If you encounter any issues, have suggestions, or would like to contribute new features, please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/abhishm20/django-task).

When contributing, please ensure that you follow the existing coding style, write tests for new functionality, and update the documentation accordingly.

## License

This project is licensed under the [MIT License](LICENSE).
