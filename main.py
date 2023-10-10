from user import user_db, check_user_type, register_user, login_user 
from transaction import add_new_product, start_delivery, confirm_receipt, raise_dispute, view_completed_deliveries, view_pending_deliveries
from block import Block, blockchain


if __name__ == "__main__":
    while True:

        print("\n")

        print("Welcome to Group 29's Supply Chain Management System")

        print("1. Register any New User i.e. Manufacturer/Distributor/Client")

        print("2. Place an Order for a New Product to Distributor from Manufacturer")

        print("3. Start the Dispactch of the Product from Distributor")

        print("4. Confirmation of the Product Received by Client")

        print("5. Raise a Dispute/Complaint by Client")

        print("6. View the Blockchain i.e. All the Blocks in the Blockchain")

        print("7. View Completed Deliveries of the Product")

        print("8. View Pending Deliveries of the Product")

        print("9. Exit Program")

        choice = input("Enter your choice number for the feature you would like to exercise: ")

        if choice == '1':
            user_type = input("Enter user type (Manufacturer/Distributor/Client): ")
            if not check_user_type(user_type):
                continue
            register_user(user_type)


        elif choice == '2':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            add_new_product(username, user_type)


        elif choice == '3':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            start_delivery(username, user_type)    


        elif choice == '4':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            confirm_receipt(username, user_type)


        elif choice == '5':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            raise_dispute(username, user_type)   


        elif choice == '6':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            if not blockchain:
                print("Blockchain currently empty")
            else:
                Block.view_blockchain(username)


        elif choice == '7':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            view_completed_deliveries(username)   


        elif choice == '8':
            user_type = input("Enter your user type: ")
            if not check_user_type(user_type):
                continue
            username = login_user(user_type)
            view_pending_deliveries(username)


        elif choice == '9':
            print("Exiting Program...")
            break
        else:
            print("Invalid choice. Please try again.")