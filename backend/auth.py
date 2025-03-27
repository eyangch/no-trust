active = set()
readers = {}

def add(ip):
    active.add(ip[0])
    readers[ip[0]] = {}
    print(f"Added IP {ip[0]}")

def remove(ip):
    active.discard(ip[0])
    for reader_arr in readers[ip[0]].values():
        for reader in reader_arr:
            reader.close()
    del readers[ip[0]]
    print(f"Removed IP {ip[0]}")

def add_readers(ip, reader_arr):
    readers[ip[0]][ip[1]] = reader_arr

def remove_readers(ip):
    if ip[0] in readers:
        del readers[ip[0]][ip[1]]

def exist(ip):
    return ip[0] in active