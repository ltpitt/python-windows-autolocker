import win32api
import time
import ctypes
import msvcrt
import bluetooth

class ScreenLock(object):
    """
    A simple object that checks if a user is in front of the computer
    If not his Windows Operating System will be locked
    """
    def __init__(self, user_phone_bluetooth_name, user_presence_timeout, mouse_coordinates=[0,0], seconds_user_missing_counter=0):
        """
        Initializing member variables
        """
        self.user_phone_bluetooth_name = user_phone_bluetooth_name
        self.mouse_coordinates = mouse_coordinates
        self.seconds_user_missing_counter = seconds_user_missing_counter
        self.user_presence_timeout = user_presence_timeout
        self.is_autolocker_enabled = False
        self.is_bluetooth_enabld = False


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
          # --- NOTE --- Keyboard check implementation is not working well
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
        target_address = None
        nearby_devices = bluetooth.discover_devices()
        for bdaddr in nearby_devices:
            if target_name == bluetooth.lookup_name( bdaddr ):
                target_address = bdaddr
                break
        if target_address is not None:
            services = bluetooth.find_service(address=target_address)
            if len(services) > 0:
                print "Found target bluetooth device with address ", target_address
                return True
            else:
                print "Could not find target bluetooth device nearby"
                return False
        else:
            print "Could not find target bluetooth device nearby"
            return False

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