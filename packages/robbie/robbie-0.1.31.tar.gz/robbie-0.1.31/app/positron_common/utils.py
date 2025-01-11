import sentry_sdk
import importlib.metadata
import sys
import os
import uuid
from positron_common.cli.logging_config import logger

def get_version():
    version = importlib.metadata.version('robbie')
    return version

def current_python_version():
    """Returns the current python version where program is running"""

    return f"{sys.version_info.major}.{sys.version_info.minor}".strip()

def get_default_workspace_dir():
    cwd = os.getcwd()
    return cwd

def is_notebook():
    """ Returns True if running in a notebook, False otherwise """
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if '__vsc_ipynb_file__' in ip.user_ns:
            logger.debug("Visual Studio Code detected!") 
            return True
        elif 'JPY_SESSION_NAME' in os.environ:
            logger.debug("Generic Jupyter Notebook detected!")
            return True
        elif 'google.colab' in str(ip):
            logger.debug("Google Colab detected!")
            return True
        else:
            logger.debug("No notebook detected")
            return False
    except AttributeError:
        logger.debug("ImportError, returning false")
        return False
    except ImportError:
        logger.debug("ImportError, returning false")
        return False
    except NameError:
        logger.debug("get_ipython() failed, not running in notebook")
        return False
    logger.debug("not running in notebook")
    return False
    
# singleton to check if we are running in a notebook
_nb = is_notebook()

#sys.exit() codes - only return if not running in a jupyter notebook
SUCCESS=0
FAILURE=1

def _exit_by_mode(val):
    """
    This function helps achieve two things:
    - If the code is not running in a notebook, it returns the value via sys.exit(). Users can write scripts with "robbie run" and check return values
    - If the code is running in a notebook, it returns None, since sys.exit() will kill the kernel in a notebook
    """
    if (val == FAILURE):
        logger.info(f"We are sorry that your job has run in to an issue. If you continue to have issues, please contact support@robbie.run and provide the following traceback.\nTrace ID: {sentry_sdk.get_current_span().trace_id}")
    logger.debug(f'Exiting...')
    sys.exit(val) if not _nb else None


# Sentinel object for undefined
undefined = object()



def is_valid_uuid(uuid_to_test, version=4):
    try:
        # check for validity of Uuid
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return True
