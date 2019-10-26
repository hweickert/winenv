"""
    Provides functionality to query environments
"""
import os
import ctypes
import ctypes.wintypes

__all__ = ['get_desktopenv', 'get_sysenv', 'get_userenv']

def errcheck_bool(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

ctypes.windll.userenv.CreateEnvironmentBlock.argtypes =  [ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p, ctypes.c_int]
ctypes.windll.userenv.CreateEnvironmentBlock.errcheck =  errcheck_bool
ctypes.windll.userenv.DestroyEnvironmentBlock.argtypes = [ctypes.c_void_p]
ctypes.windll.userenv.DestroyEnvironmentBlock.errcheck = errcheck_bool


class Handle(ctypes.wintypes.HANDLE):
    """ Handle wrapper that gets closed when garbage collected. """

    def __del__(self):
        ctypes.windll.kernel32.CloseHandle(self)


def get_desktopenv():
    """ Returns the merged system and user environment. """

    result = get_sysenv()
    user_environ = get_userenv()
    result.update(user_environ)
    return result


def get_sysenv():
    """ Returns the system environment. """

    return _get_env()


def get_userenv():
    """ Returns the user environment. """

    return _get_env(_get_new_process_token())


def _get_env(token=None):
    result = {}

    lpEnvironment = ctypes.c_void_p()
    ctypes.windll.userenv.CreateEnvironmentBlock(ctypes.byref(lpEnvironment), token, 0)

    environment_variable_address = lpEnvironment.value
    try:
        while True:
            value_string = ctypes.c_wchar_p(environment_variable_address).value
            if not value_string:
                break
            i = value_string.find('=', 1)
            if i != -1:
                key = str(value_string[:i])
                value = str(value_string[i+1:])
                result[key] = value
            environment_variable_address += (len(value_string) + 1) * ctypes.sizeof(ctypes.c_wchar)
    finally:
        ctypes.windll.userenv.DestroyEnvironmentBlock(lpEnvironment)
    return result



def _get_new_process_token():
    result = _get_duplicated_token(_get_current_process_token())
    TokenUIAccess = 26
    ctypes.windll.advapi32.SetTokenInformation(
        result, TokenUIAccess,
        ctypes.byref(ctypes.c_ulong(1)),
        ctypes.sizeof(ctypes.c_ulong)
    )
    return result

def _get_duplicated_token(token):
    MAXIMUM_ALLOWED = 0x2000000
    TokenPrimary = 1
    SecurityIdentification = 2

    result = Handle()
    ctypes.windll.advapi32.DuplicateTokenEx(token, MAXIMUM_ALLOWED, None, SecurityIdentification, TokenPrimary, ctypes.byref(result))
    return result

def _get_current_process_token():
    PROCESS_QUERY_INFORMATION = 0x0400
    MAXIMUM_ALLOWED = 0x2000000
    process = Handle(ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, os.getpid()))
    result = Handle()
    ctypes.windll.advapi32.OpenProcessToken(process, MAXIMUM_ALLOWED, ctypes.byref(result))
    return result

