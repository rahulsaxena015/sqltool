import ldap3

attr = ['*']


def authenticate(server_uri, domain, username, password):
    search_base = "ou=Users,o=adbe"
    search_filter = F"(cn={username})"
    print(F"My serch filter is: {search_filter}")
    user_dc = F"cn={username},ou=Users,o=adbe"
    server = ldap3.Server(server_uri, get_info=ldap3.ALL)
    connection = ldap3.Connection(
        server, user=user_dc, password=password, auto_bind=True)
    connection.search(search_base, search_filter, attributes=attr)
    for entry in connection.entries:
        if (len(entry['displayName']) > 0):
            display_name = str(entry['displayName'])
            print(F"My name is: {display_name}")

    if not connection.bind():
        raise ValueError("Invalid credentials")
    return display_name
