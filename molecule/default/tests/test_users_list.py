# molecule/default/tests/test_users_list.py
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

users_list = vars["users_list"]
users_home = vars["users_home"]
users_groups = vars["users_groups"]
users_shell = vars["users_shell"]


def test_user_exists_and_configured(host):
    for user in users_list:
        username = user["username"]
        u = host.user(username)

        assert u.exists
        assert u.name == username

        assert u.group == username

        expected_home = user.get("home", f"{users_home}/{username}")
        assert u.home == expected_home

        expected_groups = user.get("groups", users_groups)
        for group in expected_groups:
            assert group in u.groups

        expected_shell = user.get("shell", users_shell)
        assert u.shell == expected_shell
