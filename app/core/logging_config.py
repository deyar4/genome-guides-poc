import logging
import sys
from logging.config import dictConfig

def setup_logging():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(levelname)s:%(name)s:%(message)s"
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json", # Use json formatter for console
                "stream": "ext://sys.stdout"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "error.log",
                "maxBytes": 10485760, # 10 MB
                "backupCount": 5
            }
        },
        "loggers": {
            "root": {
                "handlers": ["console", "error_file"],
                "level": "INFO"
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False
            },
            "sqlalchemy": {
                "handlers": ["console"],
                "level": "WARNING", # Keep SQLAlchemy logs less verbose
                "propagate": False
            }
        }
    }

    dictConfig(log_config)

    # Optional: If you want to replace uvicorn's default logger with your configured one
    # This might require some deeper integration or setting up a custom server runner
    # For now, we rely on uvicorn.access and uvicorn loggers being configured
    # if you want to modify uvicorn's root logger, you might need to adjust uvicorn's code
    # or use their logging configuration options.

    # This gets the root logger and adds a basic handler if none exist (for scripts etc.)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
