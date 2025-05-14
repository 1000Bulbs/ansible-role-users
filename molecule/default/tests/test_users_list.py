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


def test_ssh_directory_exists(host):
    for user in users_list:
        if "ssh_keys" not in user:
            continue

        f = host.file(f"/home/{user['username']}/.ssh")

        assert f.exists
        assert f.is_directory
        assert f.user == user["username"]
        assert f.group == user["username"]
        assert f.mode == 0o700


def test_authorized_keys_file_exists_and_contents(host):
    for user in users_list:
        if "ssh_keys" not in user:
            continue

        path = f"/home/{user['username']}/.ssh/authorized_keys"

        f = host.file(path)

        assert f.exists
        assert f.user == user["username"]
        assert f.group == user["username"]
        assert f.mode == 0o600

        content = f.content_string.strip().splitlines()
        for key in user["ssh_keys"]:
            assert key in content
