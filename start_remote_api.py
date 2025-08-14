#!/usr/bin/env python3
"""
Start the Kenya Sugar Board Analysis API for remote access
"""

import subprocess
import sys
import socket

def check_port_available(host, port):
    """Check if a port is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result != 0
    except:
        return False

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def main():
    port = 7560
    host = "0.0.0.0"  # Bind to all interfaces for remote access
    
    print("🚀 Kenya Sugar Board Analysis API - Remote Access Setup")
    print("=" * 60)
    
    # Check if port is available
    if not check_port_available("localhost", port):
        print(f"❌ Port {port} is already in use!")
        print("💡 Stop the existing server first:")
        print("   pkill -f simple_working_api")
        return
    
    # Get local IP for display
    local_ip = get_local_ip()
    
    print(f"🌐 Starting API server for remote access...")
    print(f"📍 Binding to: {host}:{port}")
    print(f"🔗 Local access: http://localhost:{port}")
    print(f"🔗 Local network: http://{local_ip}:{port}")
    print(f"🔗 Remote access: http://YOUR_PUBLIC_IP:{port}")
    print("")
    print("📋 Firewall Setup (if needed):")
    print(f"   sudo ufw allow {port}")
    print(f"   # Or for specific IP: sudo ufw allow from YOUR_CLIENT_IP to any port {port}")
    print("")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Start the API server
        subprocess.run([sys.executable, "simple_working_api.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()