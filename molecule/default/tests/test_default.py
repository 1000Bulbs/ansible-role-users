# molecule/default/tests/test_default.py
import pytest

users_list = [{"username": "deploy"}, {"username": "devops", "groups": ["sudo"]}]


@pytest.mark.parametrize("user", users_list)
def test_user_exists_and_configured(host, user):
    username = user["username"]
    u = host.user(username)

    assert u.exists
    assert u.name == username

    expected_group = user.get("group", username)
    assert u.group == expected_group

    expected_home = user.get("home", f"/home/{username}")
    assert u.home == expected_home

    expected_groups = user.get("groups", [])
    for group in expected_groups:
        assert group in u.groups

    expected_shell = user.get("shell", "/bin/bash")
    assert u.shell == expected_shell
