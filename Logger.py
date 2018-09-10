"""
Name            :   Logger
Usage           :   Allows Logging functionality using python
Reusability     :   Completely Reusable
Author          :   AVM-Automation-SGO
Created on      :   06/06/2018
Compatibility   :   Python 3.5+
-----------------------------------------------------------------------------
Change Log: Recent Modification in TOP
------------------------------------------------------------------------------
Date        Moderator   Ver     Comments
------------------------------------------------------------------------------
09/10/2018  DomainBOTS  1.13    Added get_called_function_name
                                Added get_called_funciton_name_with_module
                                Modified InterProcessCommunicator
09/05/2018  DomainBOTS  1.12    Added __get_file_name__
                                Added Log_Constants Class
                                Modified log method's param name from
                                log_object to ipc_object
                                Modified all log methods to use
                                {InterProcessCommunicator.data}
08/13/2018  DomainBOTS  1.11    Modified Code as per PEP8 and pyLint standards
06/06/2018  DomainBOTS  1.10    Added a new function "write_default_log"
06/05/2018  DomainBOTS  1.01    Added docstrings to all functions
03/29/2018  DomainBOTS  1.00    Initial Code
"""

# python Library
import logging
import logging.config
import inspect
import os


class Log_Constants:
    INFO_PACKAGE_LOAD = "Package {ipc_object.data[package_name]} loaded"
    INFO_BOT_LOAD = "Bot loaded"
    INFO_BOT_COMPLETED = "Bot {ipc_object.data[bot_name]} completed"

    ERROR_STRING = "\nError: {ipc_object.data[error]}"
    ERROR_BOT_LOAD = "Error loading bot {ipc_object.data[bot_name]}"
    ERROR_PACKAGE_LOAD = str("Error loading package {ipc_object.data[package_name]}" +
        ERROR_STRING)
    ERROR_READ_ARGUMENT = str("Error reading argument" +
        ERROR_STRING)
    ERROR_READ_CONFIG_FILE = str("Error reading configuration at {ipc_object.data[file_name]}" +
        ERROR_STRING)
    ERROR_REPORT_GENERATION = str("Error when generating report {ipc_object.data[file_name]}")
    ERROR_IN_METHOD = str("Error in {ipc_object.data[method_name]}" + ERROR_STRING)
    ERROR_CONNECTING_DATABASE = str("Error while connecting database" +
        ERROR_STRING)
    ERROR_DATA_FETCH = str("Error while fetching data" +
        ERROR_STRING)
    ERROR_SENDING_MAIL = str("Error sending mail" + ERROR_STRING)
    ERROR_FILE_READ = str("Error when reading file" + ERROR_STRING)
    ERROR_FILE_WRITE = str("Error when writing file" + ERROR_STRING)
    ERROR_FILE_ATTACH = str("Error attaching file" + ERROR_STRING)

    DEBUG_FILE_READ_SUCCESS = "{ipc_object.data[file_name]} read operation success"
    DEBUG_FILE_WRITE_SUCCESS = "{ipc_object.data[file_name]} write operation success"
    DEBUG_CONFIG_FILE_READ_SUCCESS = "Config file - " + DEBUG_FILE_READ_SUCCESS
    DEBUG_CONFIG_FILE_WRITE_SUCCESS = "Config file - " + DEBUG_FILE_WRITE_SUCCESS
    DEBUG_REPORT_FILE_WRITE_SUCCESS = "Report file - " + DEBUG_FILE_WRITE_SUCCESS
    DEBUG_ARGUMENT_READ_SUCCESS = "Argument read successfully"
    DEBUG_METHOD_INITIATED = "{ipc_object.data[method_name]} initiated"
    DEBUG_METHOD_COMPLETE_SUCCESS = "{ipc_object.data[method_name]} completed successfully"
    DEBUG_FILE_ATTACHMENT_SUCCESS = "File attachment completed successfully"


class InterProcessCommunicator(object):
    """InterProcessCommunicator - A customised class which holds basic details
        for inter-process communication
    """
    data = None
    message = None
    status = None
    level = None
    success = None
    module = None
    
    def __init__(
            self, data=None, status=None, message=None,
            level=None, module=None, success=None
            ):

        self.data = data
        self.message = message
        self.status = status
        self.level = level
        self.success = success
        self.module = module
        return None

    def __str__(self):
        message = ""
        message = str(message + "InterProcessCommunicator" +
                    " - Used for communcation between process\n")
        message += str("Module : " + str(self.module) + "\n")
        message += str("Level : " + str(self.level) + "\n")
        return message


@DeprecationWarning
# Create own contextual information
class ContextFilter(logging.Filter):
    def filter(self, record):
        pass
        # record.module = module
        return True


@DeprecationWarning
def __initiate_logger(ipc_object):
    """Initiate Logger will creates context filter and other initiation for logger

    Arguments:
        ipc_object {InterProcessCommunicator}
            -- ipc_object is an IPC object which holds basic details for
                interprocess communication

    Returns:
        Logger -- python logger object
    """

    # create logger
    logger = logging.getLogger()
    global module
    module = ipc_object.module
    ipc_object.success = True
    # Create contextual filter to add module to the handler
    filter_set = ContextFilter()
    logger.addFilter(filter_set)
    return logger


def write_debug_log(ipc_object=None, can_log=True):
    """write_debug_log - Writes a debug message into log file

    Keyword Arguments:
        ipc_object {InterProcessCommunicator}
            -- IPC Object which holds basic communication data
                (default: {None})
        can_log {bool}
            -- Manually set whether to log the message (default: {True})

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """

    if(can_log):
        try:
            if ipc_object.data:
                ipc_object.data['method_name'] = get_called_function_name()
                ipc_object.message = "{ipc_object.module} | " + ipc_object.message
                ipc_object.message = ipc_object.message.format(ipc_object=ipc_object)
            logger = logging.getLogger()
            logger.debug(str(ipc_object.message))
        except Exception as ex:
            print("Exception : " + str(ex))
            # print(ipc_object.message)
            ipc_object.success = False
            __write_log_exception()

        finally:
            logging.shutdown()
    else:
        print('Manual log prevention - Activated')
    return ipc_object


def write_info_log(ipc_object=None, can_log=True):
    """write_info_log - Writes a info message into log file

    Keyword Arguments:
        ipc_object {InterProcessCommunicator}
            -- IPC Object which holds basic communication data
                (default: {None})
        can_log {bool}
            -- Manually set whether to log the message (default: {True})

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """

    if(can_log):
        try:
            if ipc_object.data:
                ipc_object.data['method_name'] = get_called_function_name()
                ipc_object.message = "{ipc_object.module} | " + ipc_object.message
                ipc_object.message = ipc_object.message.format(ipc_object=ipc_object)
            logger = logging.getLogger()
            logger.info(str(ipc_object.message))
        except:
            ipc_object.success = False
            __write_log_exception()

        finally:
            logging.shutdown()
    else:
        print('Manual log prevention - Activated')
    return ipc_object


def write_error_log(ipc_object=None, can_log=True):
    """write_error_log - Writes a error message into log file

    Keyword Arguments:
        ipc_object {InterProcessCommunicator}
            -- IPC Object which holds basic communication data
                (default: {None})
        can_log {bool}
            -- Manually set whether to log the message (default: {True})

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """
    if(can_log):
        try:
            if ipc_object.data:
                ipc_object.data['method_name'] = get_called_function_name()
                ipc_object.message = "{ipc_object.module} | " + ipc_object.message
                ipc_object.message = ipc_object.message.format(ipc_object=ipc_object)
            logger = logging.getLogger()
            logger.error(str(ipc_object.message))
        except Exception as ex:
            print(ex)
            ipc_object.success = False
            __write_log_exception()
        finally:
            logging.shutdown()
    else:
        print('Manual log prevention - Activated')
    return ipc_object


def write_warning_log(ipc_object=None, can_log=True):
    """write_warning_log - Writes a warning message into log file

    Keyword Arguments:
        ipc_object {InterProcessCommunicator}
            -- IPC Object which holds basic communication data
                (default: {None})
        can_log {bool}
            -- Manually set whether to log the message (default: {True})

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """
    if(can_log):
        try:
            if ipc_object.data:
                ipc_object.data['method_name'] = get_called_function_name()
                ipc_object.message = "{ipc_object.module} | " + ipc_object.message
                ipc_object.message = ipc_object.message.format(ipc_object=ipc_object)
            logger = logging.getLogger()
            logger.warning(str(ipc_object.message))
        except:
            ipc_object.success = False
            __write_log_exception()

        finally:
            logging.shutdown()
    else:
        print('Manual log prevention - Activated')
    return ipc_object


def write_critical_log(ipc_object=None, can_log=True):
    """write_critical_log - Writes a critical message into log file

    Keyword Arguments:
        ipc_object {InterProcessCommunicator}
            -- IPC Object which holds basic communication data
                (default: {None})
        can_log {bool}
            -- Manually set whether to log the message (default: {True})

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """
    if(can_log):
        try:
            if ipc_object.data:
                ipc_object.data['method_name'] = get_called_function_name()
                ipc_object.message = "{ipc_object.module} | " + ipc_object.message
                ipc_object.message = ipc_object.message.format(ipc_object=ipc_object)
            logger = logging.getLogger()
            logger.critical(str(ipc_object.message))
        except:
            ipc_object.success = False
            __write_log_exception()
        finally:
            logging.shutdown()
    else:
        print('Manual log prevention - Activated')
    return ipc_object


def write_default_log(ipc_object=None, can_log=True):
    """write_default_log - Writes a message into log file, based on given
                            log level

    Keyword Arguments:
        ipc_object {InterProcessCommunicator}
            -- IPC Object which holds basic communication data
                (default: {None})
        can_log {bool}
            -- Manually set whether to log the message (default: {True})

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """
    if(can_log):
        try:
            logger = __initiate_logger(ipc_object)
            error_level = ipc_object.level.lower()
            message = ipc_object.message

            if error_level == 'debug':
                logger.debug(str(message))
            elif error_level == 'info':
                logger.info(str(message))
            elif error_level == 'warn':
                logger.warning(str(message))
            elif error_level == 'error':
                logger.error(str(message))
            elif error_level == 'critical':
                logger.critical(str(message))
            else:
                logger.critical('Unable to find the error level described')

        except:
            ipc_object.success = False
            __write_log_exception()
        finally:
            logging.shutdown()
    else:
        print('Manual log prevention - Activated')
    return ipc_object


def __write_log_exception():
    """__write_log_exception - Writes exception log for Logger occurs

    Returns:
        [InterProcessCommunicator]
            -- IPC Object which holds basic communication data
    """

    called_function_name = get_called_function_name()
    ipc_object = InterProcessCommunicator()
    ipc_object.module = 'LogProvider'
    ipc_object.message = 'Unable to load Logger/ Logger not available in '
    ipc_object.message = ipc_object.message + called_function_name
    write_critical_log(ipc_object)

    return ipc_object


def get_called_funciton_name_with_module():
    innerframe = inspect.currentframe()
    outerframes = inspect.getouterframes(innerframe)

    for index, frame in enumerate(outerframes):
        if(frame.function == "get_called_funciton_name_with_module"):
            index += 2
            break

    called_function_name = (outerframes[index].function)
    if(called_function_name != "<module>"):
        called_function_name += "()"
    module_name = __get_bot_name__(outerframes[index].filename)
    called_function_name = str(module_name + '.' + function_name)

    return called_function_name


def get_called_function_name():
    innerframe = inspect.currentframe()
    outerframes = inspect.getouterframes(innerframe)

    for index, frame in enumerate(outerframes):
        if(frame.function == "get_called_function_name"):
            index += 2
            break

    called_function_name = (outerframes[index].function)
    if(called_function_name != "<module>"):
        called_function_name += "()"

    return called_function_name


def __get_parent_directory(file_name):
    expanded_dir = os.path.expanduser(file_name)
    realpath_dir = os.path.realpath(expanded_dir)
    directory = os.path.dirname(realpath_dir)
    return directory


def __CONFIG_FILE_NAME():
    log_path = __get_parent_directory(__file__)
    if(os.path.exists(log_path)):
        return os.path.join(log_path, 'logger.ini')
    else:
        return os.path.join(os.getcwd(), 'logger.ini')


def __get_bot_name__(file_name):
    return os.path.splitext(__get_file_name__(file_name))[0]


def __get_file_name__(file_name):
    return os.path.basename(file_name)


# Load the configuration file
_CONFIG_FILE_NAME = __CONFIG_FILE_NAME()
logging.config.fileConfig(_CONFIG_FILE_NAME)
module = ''
