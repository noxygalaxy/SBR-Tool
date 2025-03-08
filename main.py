import winreg
import time
import os

def decode_binary_value(binary_data):
    if isinstance(binary_data, bytes):
        try:
            if binary_data[-1] == 0:
                binary_data = binary_data[:-1]
            return binary_data.decode('ascii') + '.'
        except:
            pass
    
    if isinstance(binary_data, str):
        try:
            chars = []
            for hex_byte in binary_data.split():
                decimal = int(hex_byte, 16)
                if decimal != 0:
                    chars.append(chr(decimal))
            return ''.join(chars) + '.'
        except:
            pass
    
    return "Unable to decode value"

def monitor_registry_key():
    reg_path = r"Software\Linked Squad\SchoolBoy Runaway"
    value_name = "_password_h1669098341"
    update_interval = 1.0
    
    os.system('cls')
    print("SBR Password Changes Monitor")
    print("github.com/noxygalaxy")
    print("-" * 35)
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        try:
            old_value, value_type = winreg.QueryValueEx(key, value_name)
            print("Initial password value detected.")
        except FileNotFoundError:
            print("Registry key or value not found.")
            old_value = None
        finally:
            winreg.CloseKey(key)
    
        print("Monitoring for password changes...")
        print("-" * 35)
        
        while True:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
                try:
                    current_value, value_type = winreg.QueryValueEx(key, value_name)
                    
                    if current_value != old_value:
                        decoded_password = decode_binary_value(current_value)
                        print(f"Password changed to - {decoded_password}")
                        old_value = current_value
                except FileNotFoundError:
                    if old_value is not None:
                        print("Password value deleted.")
                        old_value = None
                finally:
                    winreg.CloseKey(key)
                    
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(update_interval)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        monitor_registry_key()
    except KeyboardInterrupt:
        pass