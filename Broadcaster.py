import json
import socket
import sys
import os
import time
from typing import List, Tuple

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.json')
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"ERROR: config.json not found at {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: config.json is not valid JSON")
        sys.exit(1)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def get_broadcast_address(local_ip):
    parts = local_ip.split('.')
    parts[-1] = '255'
    return '.'.join(parts)

def discover_listeners(config, timeout=3):
    print("Discovering listeners on network...")
    
    discovery_port = config.get('discovery_port', 8889)
    local_ip = get_local_ip()
    broadcast_addr = get_broadcast_address(local_ip)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)
    
    discovered = []
    
    try:
        discovery_message = json.dumps({
            'type': 'discovery',
            'password': config['password']
        })
        
        sock.sendto(discovery_message.encode('utf-8'), (broadcast_addr, discovery_port))
        
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                data, addr = sock.recvfrom(1024)
                
                try:
                    response = json.loads(data.decode('utf-8'))
                    if response.get('type') == 'listener_response':
                        listener_ip = addr[0]
                        listener_port = response.get('port', config['port'])
                        discovered.append((listener_ip, listener_port))
                        print(f"  Found listener at {listener_ip}:{listener_port}")
                except json.JSONDecodeError:
                    continue
            
            except socket.timeout:
                break
    
    except Exception as e:
        print(f"Discovery error: {str(e)}")
    finally:
        sock.close()
    
    return discovered

def connect_to_listener(ip, port, config):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        print(f"Connecting to {ip}:{port}...")
        sock.connect((ip, port))
        print("Connected!")
        
        return sock
    
    except socket.timeout:
        print(f"Connection timeout: Could not reach {ip}:{port}")
        return None
    except ConnectionRefusedError:
        print(f"Connection refused: Listener not running on {ip}:{port}")
        return None
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return None

def authenticate(sock, config):
    try:
        auth_message = json.dumps({
            'password': config['password']
        })
        sock.send(auth_message.encode('utf-8'))
        
        response_data = sock.recv(1024).decode('utf-8')
        response = json.loads(response_data)
        
        if response.get('status') == 'authenticated':
            print("Authentication successful!")
            return True
        else:
            print(f"Authentication failed: {response.get('error', 'Unknown error')}")
            return False
    
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return False

def send_command(sock, command):
    try:
        command_message = json.dumps({
            'command': command
        })
        sock.send(command_message.encode('utf-8'))
        
        result_data = sock.recv(4096).decode('utf-8')
        result = json.loads(result_data)
        
        return result
    
    except Exception as e:
        return {
            'success': False,
            'error': f"Communication error: {str(e)}",
            'output': '',
            'exit_code': -1
        }

def execute_remote_command(ip, port, command, config):
    sock = connect_to_listener(ip, port, config)
    if not sock:
        return None
    
    try:
        if not authenticate(sock, config):
            sock.close()
            return None
        
        result = send_command(sock, command)
        return result
    
    finally:
        sock.close()


def print_result(result):
    if not result:
        print("No result received")
        return
    
    print("\n" + "="*60)
    print("COMMAND RESULT")
    print("="*60)
    
    if result.get('success'):
        print("Status: SUCCESS ✓")
    else:
        print("Status: FAILED ✗")
    
    if result.get('output'):
        print(f"\nOutput:\n{result['output']}")
    
    if result.get('error'):
        print(f"\nError:\n{result['error']}")
    
    print(f"\nExit Code: {result.get('exit_code', 'N/A')}")
    print("="*60 + "\n")

def main():
    print("="*60)
    print("RemoteExe Broadcaster")
    print("="*60)
    
    config = load_config()
    listeners = discover_listeners(config)
    
    if not listeners:
        print("\nNo listeners found on network.")
        print("Options:")
        print("1. Enter IP address manually")
        print("2. Make sure listener is running on target PC")
        choice = input("\nEnter IP address manually? (y/n): ").strip().lower()
        
        if choice == 'y':
            ip = input(f"Enter IP address (default port {config['port']}): ").strip()
            
            # Allow user to specify IP:PORT or just IP
            if ':' in ip:
                # User specified IP:PORT format
                parts = ip.split(':')
                ip = parts[0].strip()
                try:
                    port = int(parts[1].strip())
                except ValueError:
                    print(f"Invalid port, using default {config['port']}")
                    port = config['port']
            else:
                # Just IP, use default port from config
                port = config['port']
            
            listeners = [(ip, port)]
            print(f"Connecting to {ip}:{port}")
        else:
            print("Exiting...")
            return
    
    if len(listeners) == 1:
        selected_ip, selected_port = listeners[0]
        print(f"\nUsing listener: {selected_ip}:{selected_port}")
    else:
        print("\nMultiple listeners found:")
        for i, (ip, port) in enumerate(listeners, 1):
            print(f"  {i}. {ip}:{port}")
        
        while True:
            try:
                choice = int(input(f"\nSelect listener (1-{len(listeners)}): "))
                if 1 <= choice <= len(listeners):
                    selected_ip, selected_port = listeners[choice - 1]
                    break
                else:
                    print("Invalid choice")
            except ValueError:
                print("Please enter a number")
    
    print("\n" + "="*60)
    print("Enter commands to execute on remote PC")
    print("Type 'exit' or 'quit' to stop")
    print("="*60 + "\n")
    
    while True:
        command = input("RemoteExe> ").strip()
        
        if not command:
            continue
        
        if command.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        result = execute_remote_command(selected_ip, selected_port, command, config)
        
        if result:
            print_result(result)
        else:
            print("Failed to execute command. Check connection and try again.")

if __name__ == '__main__':
    main()
