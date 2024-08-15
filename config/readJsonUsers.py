import json

def read_json_users_file():
    data = any
    with open('/etc/secrets/USER_TEST', 'r') as file:
        data = json.load(file)
        new_data = data['users']
        first_user = new_data[0]['email']
        data = first_user
    return data