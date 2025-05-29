# molecule/default/tests/test_default.py
import pytest

users_list = [
    {
        "username": "deploy",
        "ssh_keys": [
            "ssh-ed25519 AAAAC3NzaC1 user1@email.com",
            "ssh-ed25519 AAAAC3NzaC2 user2@email.com",
            "ssh-ed25519 AAAAC3NzaC3 user3@email.com",
        ],
    },
    {
        "username": "devops",
        "groups": ["sudo"],
        "ssh_keys": ["ssh-ed25519 AAAAC3NzaC1 user1@email.com"],
    },
]

# Filter only users who have ssh_keys defined
users_with_ssh_keys = [user for user in users_list if "ssh_keys" in user]


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


@pytest.mark.parametrize("user", users_with_ssh_keys)
def test_ssh_directory_exists(host, user):
    ssh_dir = host.file(f"/home/{user['username']}/.ssh")

    assert ssh_dir.exists
    assert ssh_dir.is_directory
    assert ssh_dir.user == user["username"]
    assert ssh_dir.group == user["username"]
    assert ssh_dir.mode == 0o700


@pytest.mark.parametrize("user", users_with_ssh_keys)
def test_authorized_keys_file_exists_and_contents(host, user):
    path = f"/home/{user['username']}/.ssh/authorized_keys"

    f = host.file(path)

    assert f.exists
    assert f.user == user["username"]
    assert f.group == user["username"]
    assert f.mode == 0o600

    content = f.content_string.strip().splitlines()
    for key in user["ssh_keys"]:
        assert key in content
