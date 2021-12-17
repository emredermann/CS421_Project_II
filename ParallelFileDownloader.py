"""
Authors:
Emre Derman
Idil Yılmaz
-----------------
Bilkent University
CS 421 - Network Course
Programming Assignment 1
Subject : Socket Programming
"""

import socket
import sys
import os


def get_request_msg(target_download_url: str, request_type="GET", custom_header=""):

    msg = f'{request_type} /{target_download_url[target_download_url.find("/"):]} HTTP/1.1\r\nHost:%s\r\n\r\n' % target_download_url[
                                                                                                                 :target_download_url.find(
                                                                                                                     "/")]
    if custom_header != "":
        msg += custom_header + '\r\n'
        msg += '\r\n'
    return msg


print('Program has been started ...')

arguments = sys.argv
arguments = arguments[1:]
range_is_given = False

target_url = arguments[0]
connection_counter = arguments[1]

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
msg = get_request_msg(target_url, request_type="GET")
print('Sending request...')
try:
    s.sendall(msg.encode())
    response = s.recv(BUFFER_SIZE)
    response1 = response.decode()
    url_list = response1.split("\n")
    # Must be dynamic in order to sustanibility.
    for r in range(1, len(url_list)):
        if url_list[r] == 'HTTP/1.1 400 Bad Request\r':
            end = r

    url_list = url_list[url_list.index('\r') + 1:url_list.index('')]
except:
    print(f"{target_url} could not founded ...")
    print("Program will exit.")
    sys.exit(1)

print(f"There are {len(url_list)} files in the index. ")
counter = 0


def get_size_of_file(url):
    try:
        internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_hostIP = socket.gethostbyname(url[:url.find("/")])
        internal_socket.connect((server_hostIP, server_port))
    except:
        print("Connection error in file {}".format(url))
        return
    connection_message = get_request_msg(url, request_type="HEAD")
    internal_socket.sendall(connection_message.encode())
    response_internal = internal_socket.recv(BUFFER_SIZE)
    response_internal = response_internal.decode()
    splitted = response_internal.split("\r")
    if splitted[0] == ('HTTP/1.1 404 Not Found'):
        print(str(counter) + " " + f"{url}  not found...")
    else:
        # File exist in server.
        # In order to get content length.
        content_length = -1
        for i in range(0, len(splitted)):
            temp = (splitted[i].split(" "))
            if temp[0].find('\nContent-Length:') != -1:
                content_length = int(temp[1])
                break
            if splitted[0] == ('HTTP/1.1 404 Not Found'):
                print(str(counter) + " " + f"{url}  not found...")
            else:
                # File exist in server.
                # In order to get content length.
                if len(splitted) > 4:
                    content_length = -1
                    for i in range(0, len(splitted)):
                        temp = (splitted[i].split(" "))
                        if temp[0].find('\nContent-Length:') != -1:
                            content_length = int(temp[1])
                            break
                    if (content_length % connection_counter == 0):
                        return content_length
    internal_socket.close()


def create_connection(url, data_size, counter):
    counter += 1
    # GETS content_length
    # No range usage.

    # if not range_is_given:
    #     internal_socket.close()
    #     internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     server_hostIP = socket.gethostbyname(url[:url.find("/")])
    #     internal_socket.connect((server_hostIP, server_port))
    #     range_header = f"Range: bytes = 0-{content_length}"
    #     msg = get_request_msg(url, request_type="GET", custom_header=range_header)
    #     internal_socket.sendall(msg.encode())
    #     resp = internal_socket.recv(BUFFER_SIZE)
    #     data = resp.decode()
    #     response1 = data.split("\n")
    #
    #     for i in range(0, len(response1)):
    #         temp = (response1[i].split(" "))
    #         if temp[0].find('\nContent-Length:') != -1:
    #             content_length = int(temp[1])
    #
    #     if response1[0] == 'HTTP/1.1 404 Not Found\r\n':
    #         print(str(counter) + " " + f"{url}" + f"(size={content_length}) is not downloaded")
    #     else:
    #         with open(url[url.rfind('/') + 1:], 'wb') as file:
    #             file.write(resp)
    #         print(str(counter) + " " + url + " " + str(content_length) + " is downloaded")
    # elif int(lower_endpoint) > content_length:
    #     print(str(counter) + f" {url}" + f"(size={content_length}) is not downloaded")
    #
    #     # Range is given and  satify requirements
    # elif int(lower_endpoint) <= int(content_length):
    #     internal_socket.close()
    #     internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     server_hostIP = socket.gethostbyname(url[:url.find("/")])
    #     internal_socket.connect((server_hostIP, server_port))
    #     local_range_header = f"Range:bytes={lower_endpoint}-{upper_endpoint}"
    #
    #     msg = get_request_msg(url, request_type="GET", custom_header=local_range_header)
    #     internal_socket.sendall(msg.encode())
    #     resp = internal_socket.recv(content_length)
    #     data = resp.decode()
    #     resp1 = data.split("\n")
    #     for i in range(0, len(resp1)):
    #         temp = (resp1[i].split(" "))
    #         if temp[0].find('\nContent-Length:') != -1:
    #             content_length = int(temp[1])
    #
    #     if resp1[0] == 'HTTP/1.1 404 Not Found\r':
    #         print(str(counter) + " " + f"{url}") + f"(size={content_length}) is not downloaded"
    #     else:
    #         with open(url[url.rfind('/') + 1:], 'wb') as file:
    #             bytes_recd = 0d
    #             flag = 0
    #             internal_socket.close()
    #             internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             server_hostIP = socket.gethostbyname(url[:url.find("/")])
    #             internal_socket.connect((server_hostIP, server_port))
    #             msg = get_request_msg(url, request_type="GET", custom_header=local_range_header)
    #             while bytes_recd < min(upper_endpoint, int(content_length)) and flag == 0:
    #                 if lower_endpoint < bytes_recd < upper_endpoint:
    #                     internal_socket.sendall(msg.encode())
    #                     chunk = internal_socket.recv(1)
    #                     if chunk != b'':
    #                         file.write(chunk)
    #                     else:
    #                         flag = 1
    #                 bytes_recd = bytes_recd + 1
    #             print(str(counter) + " " + url + " " + local_range_header + " is downloaded")

s.close()
print('Connection was closed.')
