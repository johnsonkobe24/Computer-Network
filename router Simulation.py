import getopt
import json
import os
import sys
import time
from socket import gethostbyaddr, gethostname
from socket import socket, AF_INET, SOCK_DGRAM, error as socket_error
import collections

class Node:
    # Build a UDP socket, store your arguments
    # Initialize your routing table, etc.
    # Port could be none. If it is, use 10000 + os.geteuid()
    # Cities is: ['rome:1', 'paris':7]
    def __init__(self, port, cities):
        self.host=gethostbyaddr(gethostname())[0]
        host_name=self.host
        host_name_prefix=host_name.split('.')[0]
        self.city=host_name_prefix.split('@')[-1]
        self.port=port
        if(self.port is None):
           self.port=10000+os.geteuid() 
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
            self.socket.bind(('0.0.0.0', self.port))
        except socket_error:
            print("ERROR")
            sys.exit()
        self.output_directory = "."
        file_name = self.city + "_routing.txt"
        output_file = os.path.join(self.output_directory, file_name)
        self.file = open(output_file, mode='w')
        self.table = {}
        self.destination = []
        self.parse_nodes(cities)
        self.send_routing_table(update=True)

    # Dump current list of all nodes this router knows and
    # the weight of shortest path.
    # Please see berlin_routing.txt, paris_routing.txt
    # PLEASE USE <hostname>_routing.txt names.
    # For a sanity check, you can check the last line of your text file
    # with mine. If it matches, great!
    def dump_routing_table(self):
        txt = []
        for city in self.table.keys():
            txt.append(city + " " + str(self.table[city]))
        line = '|'.join(txt)
        self.file.write(line)
        self.file.write("\n")
        self.file.flush()

    # Parse Arguments
    # Initialize list of neighbors and T = 0 of RIP Table
    # Only call this once
    # Cities is: ['rome:1', 'paris':7]
    def parse_nodes(self, cities):
       self.table[self.city] = 0
       for city in cities:
            name, weight = city.split(':')
            host = name + ".clic.cs.columbia.edu"
            port = self.port
            self.destination.append((host, port))
            self.table[name] = int(weight)


    # Send all neighbors your current routing table
    def send_routing_table(self, update=False):
        table = self.table
        table = json.dumps(table)
        for host, port in self.destination:
            self.socket.sendto(table.encode(), (host, port))
        if update:
            print(self.table)
            self.dump_routing_table()


    # Receive data from a neighbor of their routing table
    # Update our routing table as needed
    def inbound(self):
        data, address = self.socket.recvfrom(4096)
        json_data = json.loads(data.decode())
        update_status = self.update_routing_table(json_data, gethostbyaddr(address[0])[0], address[1])
        return update_status

    # Called from inbound. Update Routing Table given what neighbor told you
    # argument: routing is the unpacked JSON file of routing table from neighbor
    #Djk algrorithm
    def update_routing_table(self, dict ,host, port):
        host_prefix=host.split('.')[0]
        city = host_prefix.split('@')[-1]
        update_status = False
        dist_to_neighbor = self.table[city]
        for city, weight in dict.items():
            new_dist = dist_to_neighbor + weight
            if city in self.table.keys():
                if self.table[city] > new_dist:
                    update_status = True
                    self.table[city] = new_dist
            else:
                update_status = True
                self.table[city] = new_dist
        return update_status


    # Called from inbound. After getting routing table updates
    # run Bellman Ford to update Routing Table values
    def bellman_ford(self):
        raise NotImplementedError


def main():
    # Turns: ["-p" "8000", "berlin:1", "Vienna:1"] to ("-p", "8000"), ["berlin:1", "Vienna:1"]
    # If no -p passed you get
    # ["berlin:1", "Vienna:1"] to (-p, None), ["berlin:1", "Vienna:1"]
    options, cities = getopt.getopt(sys.argv[1:], "p:")
    try:
        port = int(options[0][1])
    except IndexError:
        port = None
    except ValueError:
        port = None
    node = Node(port, cities)

    while True:
        try:
            # I'll leave this to you to implement
            # Should be obvious which order of functions to call in what order

            # It should converge super-fast without the timer!
            # But feel free to use sleep()
            # both for troubleshooting, and minimize risk of overloading CLIC
            # Although Please Remove any sleep in final submission!
            update_status=node.inbound()
            node.send_routing_table(update=update_status)
            time.sleep(2)

        # Use CTRL-C to exit
        # You do NOT need to worry of updating routing table
        # if a node drops!
        # Show final routing table for checking if RIP worked
        except KeyboardInterrupt:
            node.file.close()
            break


if __name__ == '__main__':
    main()
