import win32api
import time
import ctypes
import msvcrt
import bluetooth
import os
from ConfigParser import SafeConfigParser

class ScreenLock(object):
    """
    A simple object that checks if a user is in front of the computer
    If not his Windows Operating System will be locked
    """
    def __init__(self, mouse_coordinates=[0,0], seconds_user_missing_counter=0):
        """
        Initializing member variables and loading / creating config file
        """
        self.config_file_name = "autolocker.ini"
        self.script_path = os.path.abspath(os.path.dirname(__file__))
        self.config_file_path = os.path.join(self.script_path, self.config_file_name)
        self.mouse_coordinates = mouse_coordinates
        self.seconds_user_missing_counter = seconds_user_missing_counter
        self.is_autolocker_enabled = False
        self.read_config_file()

    def read_config_file(self):
        """
        Checks if a user is moving his mouse or typing on his keyboard

        Returns:
        {user_presence_timeout : value, is_bluetooth_enabled : value, user_phone_bluetooth_name : value}
        """
        try:
            with open(self.config_file_path):
                print "Loading Autolocker configuration"
                parser = SafeConfigParser()
                parser.read(self.config_file_path)
                self.user_presence_timeout = parser.get('autolocker', 'user_presence_timeout')
                self.is_bluetooth_enabled = parser.get('autolocker', 'is_bluetooth_enabled')
                self.user_phone_bluetooth_name = parser.get('autolocker', 'user_phone_bluetooth_name')
                print "user_presence_timeout: " + self.user_presence_timeout
                print "is_bluetooth_enabled: " + self.is_bluetooth_enabled
                print "user_phone_bluetooth_name: " + self.user_phone_bluetooth_name
        except IOError:
                self.write_config_file()
                self.read_config_file()

    def write_config_file(self, user_presence_timeout, is_bluetooth_enabled, user_phone_bluetooth_name):
        if not os.path.isfile(self.config_file_path):
            print "Creating Autolocker configuration file with default values"
            user_presence_timeout_value = '30'
            is_bluetooth_enabled_value = 'True'
            user_phone_bluetooth_name = 'None'
        else:
            print "Updating Autolocker configuration file with values provided by user"
            user_presence_timeout_value = user_presence_timeout
            is_bluetooth_enabled_value = is_bluetooth_enabled
            user_phone_bluetooth_name = user_phone_bluetooth_name
            
        f = open(self.config_file_path, 'w')
        parser = SafeConfigParser()
        parser.add_section('autolocker')
        parser.set('autolocker', 'user_presence_timeout', user_presence_timeout_value)
        parser.set('autolocker', 'is_bluetooth_enabled', is_bluetooth_enabled_value)
        parser.set('autolocker', 'user_phone_bluetooth_name', user_phone_bluetooth_name)
        parser.write(f)
        f.close()

    def is_user_present(self):
        """
        Checks if a user is moving his mouse or typing on his keyboard

        Returns:
        True or False accordingly
        """
        key = 0
        is_user_present = False
        new_mouse_coordinates = [0,0]
        try:
          # Let's check for mouse activity
          for index, value in enumerate(win32api.GetCursorPos()):
            new_mouse_coordinates[index] = value
          if (self.mouse_coordinates != new_mouse_coordinates):
              self.mouse_coordinates = new_mouse_coordinates
              is_user_present = True
          # --- NOTE ---
          # Keyboard activity check implementation is not working well (just works if Python has focus)
          # Needs to be checked / fixed, currently disabled
          #else:
              # Seems like there is no mouse activity, let's
              # check for keyboard, then...
              #key = ord(msvcrt.getch()) if msvcrt.kbhit() else 0
              #if key != 0:
              #  is_user_present = True
              #else:
              #  is_user_present = False
        except:
          # In case of errors we assume that user is not there
          is_user_present = False
        return is_user_present

    def is_user_phone_nearby(self):
        """
        Checks if user phone (with specified user_phone_bluetooth_name)
        is nearby

        Returns:
        True or False
        """
        target_name = self.user_phone_bluetooth_name
        nearby_devices = self.find_paired_bluetooth_devices()
        for nearby_device in nearby_devices:
            if nearby_device == target_name:
                services = bluetooth.find_service(address=nearby_devices[nearby_device])
                if len(services) > 0:
                    print "Found target bluetooth device"
                    print "Name: " + nearby_device
                    print "Address: " + nearby_devices[nearby_device]
                    return True
        else:
            print "Could not find target bluetooth device nearby"
            return False

    def find_paired_bluetooth_devices(self):
        """
        Finds paired bluetooth devices

        Returns:
        {bluetooth_device_name : bluetooth_device_address}
        """
        nearby_devices_dictionary = {}
        nearby_devices = bluetooth.discover_devices()
        for nearby_device in nearby_devices:
            nearby_devices_dictionary[bluetooth.lookup_name(nearby_device)] = nearby_device
        return nearby_devices_dictionary

    def is_user_presence_timeout_reached(self):
        """
        Checks if a user has been absent for more than user_presence_timeout

        Returns:
        True or False
        """
        self.seconds_user_missing_counter += 1
        if self.seconds_user_missing_counter >= self.user_presence_timeout and not self.is_user_phone_nearby():
            return True
        else:
            return False

    def reset_seconds_user_missing_counter(self):
        """
        Resets seconds_user_missing_counter to 0
        """
        self.seconds_user_missing_counter = 0

lock = ScreenLock()