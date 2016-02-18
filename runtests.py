import sys

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "djangorestlogger",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        LOGGING={
            "version": 1,
            "disable_existing_loggers": True,
            "root": {
                "level": "WARNING",
                "handlers": ["rest_logger_handler"],
            },
            "formatters": {
                "verbose": {
                    "format": "%(levelname)s %(asctime)s %(module)s "
                              "%(process)d %(thread)d %(message)s"
                },
            },
            "handlers": {
                "rest_logger_handler": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "verbose"
                },
            },
            "loggers": {
                "django.db.backends": {
                    "level": "ERROR",
                    "handlers": ["rest_logger_handler"],
                    "propagate": False,
                },
                "django_rest_logger": {
                    "level": "DEBUG",
                    "handlers": ['rest_logger_handler'],
                    'propagate': False,
                },
            },
        },
        DEFAULT_LOGGER="django_rest_logger",
        LOGGER_EXCEPTION="django_rest_logger",
        LOGGER_ERROR="django_rest_logger",
        LOGGER_WARNING="django_rest_logger"
    )

    try:
        import django

        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback

    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests

    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
