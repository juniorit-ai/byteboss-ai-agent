class User:
    @staticmethod
    def get_user_response(prompt):
        return input(prompt)
    
    @staticmethod
    def confirm_action(prompt, commands):
        print(prompt)
        for command in commands:
            print(command)
        
        user_response = input("Do you want to proceed with these commands? (yes/No): ")
        if user_response.lower() not in ('yes', 'y'):
            print("Skipping commands.")
            return False
        return True
