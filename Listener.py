import json
import socket
import subprocess
import sys
import os
import logging
import threading
from datetime import datetime


def load_config():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    config_path = os.path.join(base_dir, 'config.json')
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"ERROR: config.json not found at {config_path}")
        print("Please make sure config.json is in the same folder as listener.py")
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: config.json is not valid JSON")
        sys.exit(1)

def setup_logging():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    log_file = os.path.join(base_dir, 'listener.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
def execute_command(command, logger):
    logger.info(f"Executing command: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'exit_code': result.returncode
        }
    
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {command}")
        return {
            'success': False,
            'output': '',
            'error': 'Command execution timed out after 30 seconds',
            'exit_code': -1
        }
    
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        return {
            'success': False,
            'output': '',
            'error': str(e),
            'exit_code': -1
        }


def handle_client(client_socket, address, config, logger):
    client_ip = address[0]
    logger.info(f"New connection from {client_ip}")
    
    try:
        client_socket.settimeout(config.get('timeout', 30))
        
        auth_data = client_socket.recv(1024).decode('utf-8')
        
        try:
            auth_message = json.loads(auth_data)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON from {client_ip}")
            client_socket.close()
            return
        
        if auth_message.get('password') != config['password']:
            logger.warning(f"Invalid password from {client_ip}")
            response = json.dumps({'error': 'Authentication failed'})
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            return
        
        logger.info(f"Authentication successful from {client_ip}")
        
        auth_response = json.dumps({'status': 'authenticated'})
        client_socket.send(auth_response.encode('utf-8'))
        
        while True:
            command_data = client_socket.recv(4096).decode('utf-8')
            
            if not command_data:
                logger.info(f"Client {client_ip} disconnected")
                break
            
            try:
                command_message = json.loads(command_data)
            except json.JSONDecodeError:
                logger.warning(f"Invalid command JSON from {client_ip}")
                continue
            
            command = command_message.get('command', '')
            
            if not command:
                logger.warning(f"Empty command from {client_ip}")
                continue
            
            result = execute_command(command, logger)
            
            response = json.dumps(result)
            client_socket.send(response.encode('utf-8'))
            
            logger.info(f"Command executed, result sent to {client_ip}")
    
    except socket.timeout:
        logger.warning(f"Connection timeout with {client_ip}")
    except Exception as e:
        logger.error(f"Error handling client {client_ip}: {str(e)}")
    finally:
        client_socket.close()
        logger.info(f"Connection closed with {client_ip}")

def discovery_server(config, logger):
    discovery_port = config.get('discovery_port', 8889)
    
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    discovery_socket.bind(('0.0.0.0', discovery_port))
    
    logger.info(f"Discovery server started on UDP port {discovery_port}")
    
    while True:
        try:
            data, addr = discovery_socket.recvfrom(1024)
            
            try:
                request = json.loads(data.decode('utf-8'))
                
                if (request.get('type') == 'discovery' and 
                    request.get('password') == config['password']):
                    
                    response = json.dumps({
                        'type': 'listener_response',
                        'port': config['port']
                    })
                    discovery_socket.sendto(response.encode('utf-8'), addr)
                    logger.info(f"Responded to discovery from {addr[0]}")
            
            except json.JSONDecodeError:
                continue
            except Exception as e:
                logger.error(f"Discovery error: {str(e)}")
        
        except Exception as e:
            logger.error(f"Discovery server error: {str(e)}")
            break
    
    discovery_socket.close()

def start_server(config, logger):
    discovery_thread = threading.Thread(
        target=discovery_server,
        args=(config, logger),
        daemon=True 
    )
    discovery_thread.start()
    logger.info("Discovery thread started")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = config['port']
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    
    logger.info(f"Listener started on port {port}")
    logger.info("Waiting for connections...")
    
    # Only print to console if not in background mode
    if sys.stdout.isatty():
        print(f"\n{'='*60}")
        print(f"RemoteExe Listener is running on port {port}")
        print(f"Discovery enabled on UDP port {config.get('discovery_port', 8889)}")
        print(f"Waiting for commands from broadcaster...")
        print(f"{'='*60}\n")
    
    while True:
        try:
            client_socket, address = server_socket.accept()
            
            handle_client(client_socket, address, config, logger)
        
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
            if sys.stdout.isatty():
                print("\nShutting down listener...")
            break
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            continue
    
    server_socket.close()

def is_running_in_background():
    """
    Detects if the script is running in background (no console).
    Returns True if running in background, False if in foreground.
    """
    # Check if running with pythonw.exe (Windows background mode)
    if sys.executable.endswith('pythonw.exe'):
        return True
    
    # Check if stdout is redirected (background process)
    try:
        # If we can't access the terminal, we're in background
        if not sys.stdout.isatty():
            return True
    except:
        pass
    
    return False

def main():
    # Check if running in background
    background_mode = is_running_in_background()
    
    if not background_mode:
        print("Starting RemoteExe Listener...")
    
    config = load_config()
    logger = setup_logging()
    
    logger.info("="*60)
    logger.info("RemoteExe Listener starting...")
    logger.info(f"Port: {config['port']}")
    logger.info(f"Password: {'*' * len(config['password'])}")
    logger.info(f"Background mode: {background_mode}")
    
    try:
        start_server(config, logger)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        if not background_mode:
            print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
