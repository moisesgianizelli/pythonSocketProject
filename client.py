import socket

class InvalidInputError(Exception):
    pass

HOST = '127.0.0.1'
PORT = 65432

def get_user_input(prompt):
    return input(prompt).strip()

def validate_employee_id(employee_id):
    if not (employee_id.startswith('E') and len(employee_id) == 6 and employee_id[1:].isdigit()):
        raise InvalidInputError("Invalid employee ID. Please enter a valid employee ID.")

def validate_query_type(query_type):
    if query_type not in ['S', 'L']:
        raise InvalidInputError("Invalid query type. Please enter 'S' for Salary or 'L' for Annual Leave.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("HR System 1.0")
        print("---------------")

        while True:
            try:
                employee_id = get_user_input("What is the employee id? ").upper()
                validate_employee_id(employee_id)

                query_type = get_user_input("Salary (S) or Annual Leave (L) Query? ").upper()
                validate_query_type(query_type)

                query_subtype = get_user_input("Current (C) or Total (T) for year? ").upper()

                if query_subtype == 'T' or query_subtype == 'Y':
                    year = get_user_input("What year? ")
                else:
                    year = ""

                command = f"{employee_id} {query_type} {query_subtype} {year}"
                s.sendall(command.encode())

                data = s.recv(1024).decode()
                print(data)

                continue_exit = get_user_input("Would you like to continue (C) or exit (X)? ").upper()
                if continue_exit == 'X':
                    print("Goodbye")
                    break

            except InvalidInputError as e:
                print(e)
                continue

if __name__ == "__main__":
    main()
