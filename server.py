import socket

HOST = '127.0.0.1'
PORT = 65432

employees = {
    'E00123': ('Aadya Khan', 38566, 25),
    'W01033': ('Invalid Employee', 0, 0),
    'E01033': ('John Smith', 29400, 25),
    'E12345': ('Alice Johnson', 45000, 22),
    'E23456': ('Bob Miller', 38000, 23),
    'E34567': ('Charlie Davis', 42000, 24),
    'E45678': ('David Brown', 50000, 21),
    'E56789': ('Eva White', 41000, 26),
    'E67890': ('Frank Wilson', 48000, 20),
    'E78901': ('Grace Anderson', 39000, 28),
    'E89012': ('Henry Lee', 46000, 25),
    'E90123': ('Ivy Martinez', 43000, 27),
    'E01234': ('Jack Taylor', 47000, 23),
}

def employee_validation(employee_id):
    return employee_id in employees

def get_current_salary(employee):
    employee_name = employee[0]
    result_message = f"Employee {employee_name}\n Current basic salary: {employee[1]}"
    return result_message

def get_total_salary(employee, year):
    overtime = employee[2] if len(employee) > 2 else 0
    employee_name = employee[0]
    basic_pay = employee[1]
    total_salary = basic_pay
    result_message = f"Employee {employee_name}\nTotal Salary for {year}: Basic pay, {total_salary}, Overtime, {overtime}" 
    return result_message


def get_leave_details(employee, year):
    employee_name = employee[0]
    leave_days = employee[2]
    result_message = f"Employee {employee_name}\nLeave taken in {year}: {leave_days} days"
    return result_message

def get_annual_leave_entitlement(employee):
    annual_leave_entitlement = employee[2]
    result_message = f"Current annual leave entitlement: {annual_leave_entitlement} days"
    return result_message

def handle_request(data):
 # Parse the received data
    employee_id, query_type, query_subtype, year = data.split()

    # Validation
    if not employee_validation(employee_id):
        return "Invalid employee ID"

    # Retrieve employee details 
    employee = employees[employee_id]
    if query_type == 'S':
        if query_subtype == 'C':
            return get_current_salary(employee)
        elif query_subtype == 'T':
            return get_total_salary(employee, year)
    elif query_type == 'L': 
        if query_subtype == 'Y':
            return get_leave_details(employee, year)
        elif query_subtype == 'C':
            return get_annual_leave_entitlement(employee)

    return "Not recognized command or option"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("HR System 1.0 - Server is listening...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                response = handle_request(data)
                conn.sendall(response.encode())

if __name__ == "__main__":
    main()
