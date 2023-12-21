import socket
import threading
import pika
import queue

HOST = '0.0.0.0'
PORT = 65432
RABBITMQ_HOST = 'host.docker.internal' 

parameters = pika.ConnectionParameters(
    host='host.docker.internal',            
    port=5672,                    
    virtual_host='hr_system',     
    credentials=pika.PlainCredentials('hr_user', '1234')
)

# Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters('host.docker.internal'))
channel = connection.channel()


employees = {
    'E00123': ('Aadya Khan', 38566, 25),
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

user_input_queue = queue.Queue()

def log_activity(employee_id, command, options, client_ip):
    # Create a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='activity_log')
    log_message = f"Employee ID: {employee_id}, Command: {command}, Options: {options}, Client IP: {client_ip}"
    channel.basic_publish(exchange='', routing_key='activity_log', body=log_message)
    connection.close()

def employee_validation(employee_id):
    return employee_id in employees

def get_current_salary(employee):
    print(employee)
    if len(employee) >= 2:
        employee_name = employee[0]
        result_message = f"Employee {employee_name}\n Current basic salary: {employee[1]}"
    else:
        result_message = "Invalid employee data format"
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

def get_user_input(prompt):
    user_input = input(prompt).strip()
    user_input_queue.put(user_input) 
    return user_input

def publish_to_queue(employee_id, query_type, query_subtype, year, client_ip):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='activity_log')

    message = f"{employee_id} {query_type} {query_subtype} {year} {client_ip}"
    channel.basic_publish(exchange='', routing_key='activity_log', body=message)

    connection.close() 

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    response = None 

    while True:
        try:
            user_input = user_input_queue.get_nowait()
            print(f"Received user input from {addr}: {user_input}")

        except queue.Empty:
            pass

        data = conn.recv(1024).decode()
        if not data:
            break
        print(data)
        print(str(data))

        # Parse the received data
        year = None
        try:
            employee_id, query_type, query_subtype, year = str(data).split()
        except ValueError:
            print(f"Error: Received unexpected data format: {data}")
            try:
                employee_id, query_type, query_subtype = str(data).split()
            except ValueError:
                print(f"Error: Received unexpected data format: {data}")
                continue
        print(employee_id)

        # Validation
        if not employee_validation(employee_id):
            response = "Invalid employee ID"
        else:
            # Retrieve employee details
            print("entrei no else")
            employee = employees.get(employee_id)
            if not employee:
                response = "Employee not found"
            else:
                print(employee)
                if query_type == 'S':
                    if query_subtype == 'C':
                        response = get_current_salary(employee)
                    elif query_subtype == 'T':
                        response = get_total_salary(employee, year)
                elif query_type == 'L':
                    if query_subtype == 'Y':
                        response = get_leave_details(employee, year)
                    elif query_subtype == 'C':
                        response = get_annual_leave_entitlement(employee)
                else:
                    response = "Not recognized command or option"

                command = f"{employee_id} {query_type} {query_subtype} {year}"

                log_message = f'Employee Activity: {command} from IP: {addr[0]}'
                channel.basic_publish(exchange='',
                                      routing_key='activity_log',
                                      body=log_message)

        if response is None:
            response = "Error processing request"

        conn.sendall(response.encode())

    print(f"Connection closed by {addr}")
    conn.close()

def main():
    print("testmain")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("HR System 1.0 - Server is listening...")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
