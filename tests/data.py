tasks = [
    {"name": "task1", "description": "desc1"},
    {"name": "task2", "description": "desc2"},
    {"name": "task3", "description": "desc3"},
]

invalid_tasks = [
    {"name": "", "description": "desc1"},
    {"name": "task1", "description": ""},
]

users = [
    {"name": "foobar", "password": "foobar123", "email": "foobar@example.com"},
    {
        "name": "deadbeef",
        "password": "deadbeef123",
        "email": "deadbeef@example.com",
    },
]

invalid_users = [
    {"name": "", "password": "foobar123", "email": "foobar@example.com"},
    {"name": "deadbeef", "password": "deadbeef123", "email": "deadbeef"},
]
