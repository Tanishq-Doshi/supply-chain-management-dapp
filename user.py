user_db = {'Manufacturer': {}, 'Distributor': {}, 'Client': {}}

def check_user_type(user_type):
    if user_type != 'Manufacturer' and user_type != 'Distributor' and user_type != 'Client':
        print("Please enter valid user type")
        return False
    else:
        return True

def register_user(user_type):
    if user_type == 'Manufacturer' and user_db['Manufacturer']:
        print("A manufacturer is already registered.")
        return
    
    username = input("Enter username: ")
    id = int(input("Enter ID number: "))
    security_deposit = 0
    if user_type != 'Manufacturer':
        security_deposit = float(input("Enter security deposit amount: "))  # Prompt for security deposit
    
    id_exists = any(id == user_data['id'] for user_data in user_db['Manufacturer'].values()) or \
                any(id == user_data['id'] for user_data in user_db['Distributor'].values()) or \
                any(id == user_data['id'] for user_data in user_db['Client'].values())

    if not id_exists:
        user_db[user_type][username] = {'id': id, 'security_deposit': security_deposit}
        print(f"{user_type} {username} registered successfully with a security deposit of ₹{security_deposit}.")
    else:
        print("ID already exists.")

def login_user(user_type):
    username = input("Enter username: ")
    if username in user_db[user_type]:
        print(f"{user_type} {username} logged in successfully.")
        return username
    else:
        print("Invalid credentials.")
        return None