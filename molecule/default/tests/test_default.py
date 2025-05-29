# molecule/default/tests/test_default.py


def test_host_is_reachable(host):
    """Ensure etc directory exists"""
    etc = host.file("/etc")
    assert etc.exists
    assert etc.is_directory
