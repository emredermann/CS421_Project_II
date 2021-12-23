"""
Authors:
Emre Derman
-----------------
Bilkent University
CS 421 - Network Course
Programming Assignment 2
Subject : Parallel File Downloader
"""

import socket
import sys
import threading



def get_size_of_file(url):
    try:
        internal_socket_get_size_of_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostIP_get_size_of_file = socket.gethostbyname(url[:url.find("/")])
        internal_socket_get_size_of_file.connect((hostIP_get_size_of_file, server_port))
    except:
        print("Connection error in file {}".format(url))
        return
    connection_message = get_request_msg(url, request_type="HEAD")
    internal_socket_get_size_of_file.sendall(connection_message.encode())
    response_internal_get_size_of_file = internal_socket_get_size_of_file.recv(BUFFER_SIZE)
    response_internal_get_size_of_file = response_internal_get_size_of_file.decode()
    splitted = response_internal_get_size_of_file.split("\r")
    if splitted[0] == ('HTTP/1.1 404 Not Found'):
        print(f"{url}  not found...")
        internal_socket_get_size_of_file.close()
    else:
        # File exist in server.
        # In order to get content length.
        content_length = -1
        for i in range(0, len(splitted)):
            temp = (splitted[i].split(" "))
            if temp[0].find('\nContent-Length:') != -1:
                content_length = int(temp[1])
                internal_socket_get_size_of_file.close()
                break
            if splitted[0] == ('HTTP/1.1 404 Not Found'):
                print(f"{url}  not found...")
            else:
                # File exist in server.
                # In order to get content length.
                if len(splitted) > 4:
                    for i in range(0, len(splitted)):
                        temp = (splitted[i].split(" "))
                        if temp[0].find('\nContent-Length:') != -1:
                            content_length = int(temp[1])

                            internal_socket_get_size_of_file.close()
                            return content_length
                    # if content_length % thread_counter == 0:
                    #     internal_socket_get_size_of_file.close()
                    #     return content_length
        internal_socket_get_size_of_file.close()
        return -1


def create_connection(url,data_capacity_of_each_thread,last_read_byte,upper_limit):
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_hostIP = socket.gethostbyname(url[:url.find("/")])
    internal_socket.connect((server_hostIP, server_port))
    # In order to decide the bounds of the connection.
    range_header = f"Range: bytes = {last_read_byte}-{upper_limit}"
    msg = get_request_msg(url, request_type="GET", custom_header=range_header)
    internal_socket.sendall(msg.encode())
    resp = internal_socket.recv(BUFFER_SIZE)
    with open(url[url.rfind('/') + 1:], 'wb') as file:
        file.write(resp)
    last_read_byte += data_capacity_of_each_thread
    internal_socket.close()

def get_request_msg(target_download_url: str, request_type="GET", custom_header=""):
    msg = f'{request_type} /{target_download_url[target_download_url.find("/"):]} HTTP/1.1\r\nHost:%s\r\n\r\n' % target_download_url[
                                                                                                                 :target_download_url.find(
                                                                                                                     "/")]
    if custom_header != "":
        msg += custom_header + '\r\n'
        msg += '\r\n'
    return msg

def createNewDownloadThread(link, data_capacity_of_each_thread,last_read_byte):
    global upper_limit
    upper_limit = last_read_byte + data_capacity_of_each_thread
    download_thread = threading.Thread(target=create_connection, args=(link,data_capacity_of_each_thread,last_read_byte,upper_limit))
    download_thread.start()

print('Program has been started ...')

arguments = sys.argv
arguments = arguments[1:]
range_is_given = False

target_url = arguments[0]
thread_counter = int(arguments[1])

print(f"URL of the index file: {target_url}")
file_name = target_url[target_url.rfind("/") + 1:]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_hostIP = socket.gethostbyname(target_url[:target_url.find("/")])

server_port = 80
BUFFER_SIZE = 100000

# Connect to the server
s.connect((server_hostIP, server_port))

print(f'Connected to {server_hostIP} on {server_port} port.')

# Make a GET request
# Get  and save it to

msg = get_request_msg(target_url, request_type="GET")
print('Sending request...')
try:
    s.sendall(msg.encode())
    response = s.recv(BUFFER_SIZE)
    response1 = response.decode()
    url_list = response1.split("\n")
    for r in range(1, len(url_list)):
        if url_list[r] == 'HTTP/1.1 400 Bad Request\r':
            end = r

    url_list = url_list[url_list.index('\r') + 1:url_list.index('')]
except:
    print(f"{target_url} could not founded ...")
    print("Program will exit.")
    sys.exit(1)

print(f"There are {len(url_list)} files in the index. ")

"""
 n :  the number of bytes in the file.
 k :  the number of connections. 
 
if n is divisible by k, 
    The number of bytes downloaded through each connection is  n/k
Otherwise, ((n/k)+1) bytes should be downloaded through the first (n−(n/k)*k) connections 
    and ⌊n/k⌋ bytes should be downloaded through the remaining connections.
"""
counter = 1
for x in url_list:
    # Head request in order to check file existence.
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostIP = socket.gethostbyname(x[:x.find("/")])
    internal_socket.connect((hostIP, server_port))
    connection_message = get_request_msg(x, request_type="HEAD")
    internal_socket.sendall(connection_message.encode())
    response_internal = internal_socket.recv(BUFFER_SIZE)
    response_internal = response_internal.decode()
    splitted = response_internal.split("\r")
    if splitted[0] == ('HTTP/1.1 404 Not Found'):
        print(f"{str(counter)}. {x} not found. ")
    else:
        last_read_byte = 0
        upper_limit = 0
        file_size = get_size_of_file(x)
        global result
        result = f"{str(counter)}. {x} (size = {file_size}) is downloaded \n File parts: "
        if file_size % thread_counter == 0:
            data_capacity_of_each_thread = file_size / thread_counter
            for y in range(thread_counter):
                last_read_byte += int(data_capacity_of_each_thread)
                createNewDownloadThread(x, data_capacity_of_each_thread,last_read_byte)
                result += f"{int(last_read_byte - data_capacity_of_each_thread)}:{int(last_read_byte)}({int(data_capacity_of_each_thread)})  "
                # create_connection(x,last_read_byte,data_capacity_of_each_thread)
        else:
            # As default downloader for each thread
            data_capacity_of_each_thread = 1
            for y in range(thread_counter):
                if y < thread_counter - 1:
                    data_capacity_of_each_thread = file_size / thread_counter + 1
                else:
                    data_capacity_of_each_thread = file_size / thread_counter
                last_read_byte += int(data_capacity_of_each_thread)
                createNewDownloadThread(x, int(data_capacity_of_each_thread),last_read_byte)
                result += f"{int(last_read_byte-data_capacity_of_each_thread)}:{int(last_read_byte)}({int(data_capacity_of_each_thread)})  "
        print(result)
    counter += 1
s.close()
print('Connection was closed.')
