import string
import time
import qrcode
import random
from user import user_db
from block import blockchain,Block

ongoing_deliveries = []
completed_transactions = []
production = []
products = {}


def generate_product_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def generate_qr_code(transaction):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr_data = f"Product: {transaction['product']}\n"
    qr_data += f"Produced: {time.ctime(transaction['production_timestamp'])}\n"
    qr_data += f"Shipped: {time.ctime(transaction['ship_timestamp']) if transaction['ship_timestamp'] else 'Not yet shipped'}\n"
    qr_data += f"Received: {time.ctime(transaction['receive_timestamp']) if transaction['receive_timestamp'] else 'Not yet received'}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{transaction['product']}_status_qr.png")
    print(f"QR code saved as {transaction['product']}_status_qr.png")


def add_new_product(username, user_type):
    if username:
        if user_type == 'Manufacturer':
            product = input("Enter product name to add to the product list: ")
            amount = float(input("Enter product price: "))
            if product not in products:
                product_id = generate_product_id()  
                production_timestamp = time.time()  
                products[product] = {'product_id': product_id, 'production_timestamp': production_timestamp, 'amount': amount}
                transaction = {
                    'transaction_type': 'Manufacturer to Distributor',
                    'product_id': product_id,  
                    'product': product,
                    'amount': amount,
                    'production_timestamp': production_timestamp,   
                    'ship_timestamp': None,
                    'receive_timestamp': None
                }
                production.append(transaction)
                generate_qr_code(transaction)
                print(f"Product '{product}' (ID: {product_id}) added to the product list.")
            else:
                print(f"Product '{product}' is already in the product list.")
        else:
            print(f"{user_type} does not have production ability.")        
    else:
        print("You must be logged in as a Manufacturer to add products to the product list.")


def transaction_possible(username):
    transaction_present = False
    for delivery in ongoing_deliveries:
        if delivery['distributor'] == username:
            transaction_present = True

    return False if transaction_present else True

    
def start_delivery(username, user_type):
    if username:
        if user_type == 'Distributor':

            if not transaction_possible(username):
                print(f"The distributor {username} already has a pending delivery.")
                return
            
            client = input("Enter client username: ")

            
            if client not in user_db['Client']:
                print(f"Client {client} is not registered.")
                return

            product = input("Enter product name: ")
            amount = float(input("Enter transaction amount: "))  
            if product in products:
                product_id = products[product]['product_id']  
                production_timestamp = products[product]['production_timestamp']  
                transaction = {
                    'transaction_type': 'Distributor to Client',
                    'distributor': username,
                    'client': client,
                    'product_id': product_id,  
                    'product': product,
                    'amount': amount,
                    'production_timestamp': production_timestamp,  
                    'ship_timestamp': time.time(),
                    'receive_timestamp': None
                }
                products.pop(product)
                ongoing_deliveries.append(transaction)
                generate_qr_code(transaction)
                print(f"Product shipped: {transaction}")
            else:
                print(f"'{product}' is not available for delivery .")
        else:
            print(f"{user_type} role does not have transaction capabilities.")
            return
    else:
        print("You must be logged in as a distributor to start a transaction.")
    
  
def confirm_receipt(username, user_type):
    count = 0
    if username:
        if user_type == 'Client':
            print("Ongoing Deliveries:")
            for index, delivery in enumerate(ongoing_deliveries):
                if delivery['client'] == username:
                    count+=1
                    print(f"{index + 1}. Product: {delivery['product']}, Distributor: {delivery['distributor']}, Client: {delivery['client']} \n")

            if count == 0:
                print(f"No pending deliveries for Client {username}")
                return
            
            delivery_choice = input("Enter the number of the delivered product (e.g., 1, 2, ...): ")
            try:
                delivery_choice = int(delivery_choice) - 1  
                if 0 <= delivery_choice < len(ongoing_deliveries):
                    delivered_product = ongoing_deliveries[delivery_choice]
                    delivered_product['receive_timestamp'] = time.time()
                    if verify_transaction(delivered_product):
                        print(f"Product received: {delivered_product}")
                        generate_qr_code(delivered_product)
                        process_transaction(delivered_product)
                        ongoing_deliveries.pop(delivery_choice)
                    else:
                        print("Invalid Transaction") 
                        return   
                else:
                    print("Invalid choice. Please enter a valid product number.")
            except ValueError:
                print("Invalid input. Please enter a valid product number.")
        else:
            print(f"{user_type} does not have confirmation ability.")        
    else:
        print("You must be logged in as client to confirm receipt.")    

def verify_transaction(transaction):
    required_fields = ['transaction_type', 'product_id', 'product', 'amount', 'production_timestamp', 'ship_timestamp', 'receive_timestamp', 'client', 'distributor']
    for field in required_fields:
        if field not in transaction:
            print(f"Transaction is missing the '{field}' field.")
            return False

    production_timestamp = transaction['production_timestamp']
    ship_timestamp = transaction['ship_timestamp']
    receive_timestamp = transaction['receive_timestamp']

    if ship_timestamp and production_timestamp > ship_timestamp:
        print("Invalid transaction: Production timestamp is after ship timestamp.")
        return False

    if receive_timestamp and ship_timestamp > receive_timestamp:
        print("Invalid transaction: Ship timestamp is after receive timestamp.")
        return False

    return True

def process_transaction(transaction):
    if transaction not in completed_transactions:
        completed_transactions.append(transaction)
        print("Transaction verified and added to the list.")

    if len(completed_transactions) % 3 == 0: 
        if not blockchain:
            previous_hash = '0x4cd1e910c3d74780000000000000000000000000000000000000000000000000'  # Genesis block
        else:
            previous_hash = blockchain[-1].hash
        Block.mine_block(completed_transactions[-3:], previous_hash) 

def raise_dispute(username, user_type):
    if username and user_type == 'Client':
        distributor_name = input("Enter distributor name: ")

        if distributor_name not in user_db['Distributor']:
                print(f"Distributor {distributor_name} is not registered.")
                return
        
        product_name = input("Enter the product name for which you want to raise a dispute: ")
        product_exists = False

        for transaction in completed_transactions:
            if transaction['product'] == product_name and transaction['client'] == username and transaction['distributor'] == distributor_name:
                product_exists = True
                if 'amount' in transaction:
                    dispute_amount = transaction['amount']
                    if user_db[user_type][username]['security_deposit'] >= dispute_amount:
                        user_db[user_type][username]['security_deposit'] -= dispute_amount
                        print(f"You have tried to raise a dispute for product '{product_name}' which has already been delivered to you. As a consequence, ₹{dispute_amount} will be deducted from your security deposit.")
                        print(f"Your security deposit now stands at ₹{user_db['Client'][username]['security_deposit']}")
                        break
                    else:
                        print(f"Insufficient security deposit to raise a dispute for product '{product_name}'.")

        for delivery in ongoing_deliveries:
            if delivery['product'] == product_name and delivery['client'] == username and delivery['distributor'] == distributor_name:
                product_exists = True
                print(f"The delivery for product '{product_name}' is still pending. Please be patient.")
                return

        if not product_exists:
            product_exists_in_products = product_name in products
            if product_exists_in_products:
                dispute_amount = products[product_name]['amount']
                if user_db['Distributor'][distributor_name]['security_deposit'] >= dispute_amount:
                    user_db['Distributor'][distributor_name]['security_deposit'] -= dispute_amount
                    print(f"{distributor_name} has wrongly marked '{product_name}' as shipped. As a consequence, ₹{dispute_amount} will be deducted from his security deposit.")
                else:
                    print(f"Insufficient security deposit to raise a dispute for product '{product_name}'.")
            else:
                print("No such product exists")
    else:
        print("You must be logged in as a client to raise a dispute.")

def view_completed_deliveries(username):
    if username: 
        if len(completed_transactions) == 0:
            print("No deliveries completed yet")
        else:
            print("Completed Deliveries:")
            for index, delivery in enumerate(completed_transactions):
                        print(f"{index + 1}. Product: {delivery['product']}")
                        print(f"   Distributor: {delivery['distributor']}")
                        print(f"   Client: {delivery['client']}")
                        print(f"   Amount: {delivery['amount']}")
                        print(f"   Produced At: {time.ctime(delivery['production_timestamp'])}")
                        print(f"   Shipped At: {time.ctime(delivery['ship_timestamp'])}")
                        print(f"   Received At: {time.ctime(delivery['receive_timestamp'])}")
    else:
        print("You must be logged in to view completed deliveries.")                    

def view_pending_deliveries(username):
    if username:
        if len(ongoing_deliveries) == 0:
            print("No pending deliveries")
        else:     
            print("Ongoing Deliveries:")
            for index, delivery in enumerate(ongoing_deliveries):
                        print(f"{index + 1}. Product: {delivery['product']}, Distributor: {delivery['distributor']}, Client: {delivery['client']}, Amount: {delivery['amount']} \n")
    else:
         print("You must be logged in to view pending deliveries.")                   