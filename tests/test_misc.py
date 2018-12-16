import sys
import pytest


@pytest.mark.skipif(sys.platform != 'win32', reason='only runs on windows')
def test_import():
    import winenv


class Test_main_functions_start:
    def test_get_desktopenv(self):
        import winenv
        winenv.get_desktopenv()

    def test_get_sysenv(self):
        import winenv
        winenv.get_sysenv()

    def test_get_userenv(self):
        import winenv
        winenv.get_userenv()

