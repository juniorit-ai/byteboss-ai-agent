import os

class User:
    @staticmethod
    def get_user_response(prompt):
        return input(prompt)
    
    @staticmethod
    def confirm_action(description, commands):
        print(description)
        for command in commands:
            print(command)
            
        if os.getenv('JUNIORIT_CONTAINER_TOKEN') is not None:
            print("Please execute the commands above manually.")
            return False
        
        user_response = input("Do you want to proceed with these commands? (yes/No): ")
        if user_response.lower() not in ('yes', 'y'):
            print("Skipping commands.")
            return False
        return True
