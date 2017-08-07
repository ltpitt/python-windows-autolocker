#!/usr/bin/python
import wx

class AutolockSettingsDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        first_row_x = 15
        first_row_y = 40
        second_row_y = 70
        third_row_y = 130
        wx.Dialog.__init__(self, parent, id, title, size=(500, 250))
        self.setting_static_box = wx.StaticBox(self, -1, 'Settings', (5, 5), size=(480, 170))
        # First row
        self.first_row_text = wx.StaticText(self, -1, 'Lock threshold (seconds):', (first_row_x, first_row_y))
        self.first_row_spin = wx.SpinCtrl(self, 1, '1', (first_row_x+140, first_row_y-2), (60, -1), min=1, max=120)
        # Second row
        self.second_row_text = wx.StaticText(self, -1, 'Bluetooth check enable:', (first_row_x, second_row_y+20))
        self.second_row_checkbox = wx.CheckBox(self, 1, '', (first_row_x+140, second_row_y+21))
        # Third row
        self.bluetooth_refresh_button = wx.Button(self, 3, 'Refresh paired bluetooth devices', (10, third_row_y), (200, -1))
        self.bluetooth_text = wx.StaticText(self, -1, 'Choose Device:', (235, third_row_y+5))
        bluetooth_devices_list = ['Me','You']
        self.bluetooth_device_combobox = wx.ComboBox(self, -1, pos=(328, third_row_y+1), size=(150, -1), choices=bluetooth_devices_list, style=wx.CB_READONLY)
        # Buttons
        self.button_ok = wx.Button(self, 1, 'Ok', (330, 185), (60, -1))
        self.button_cancel = wx.Button(self, 2, 'Cancel', (398, 185))
        # Listeners
        self.Bind(wx.EVT_BUTTON, self.OnOk, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnBluetoothSearch, id=3)
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck, id=1)
        # Quit
        self.Centre()
        self.ShowModal()
        self.Destroy()

    def OnBluetoothSearch(self, event):
        print "Searching!"

    def OnCancel(self, event):
        self.Close()

    def OnOk(self, event):
        self.Close()

    def OnSelect(self, event):
        return event.GetSelection()

    def OnCheck(self, event):
        checkbox = event.GetEventObject()
        if checkbox.GetValue() == True:
            self.bluetooth_refresh_button.Enable()
            self.bluetooth_text.Enable()
            self.bluetooth_device_combobox.Enable()
        else:
            self.bluetooth_refresh_button.Disable()
            self.bluetooth_text.Disable()
            self.bluetooth_device_combobox.Disable()


class AutolockApp(wx.App):
    def OnInit(self):
        dlg = AutolockSettingsDialog(None, -1, 'Autolock')
        dlg.ShowModal()
        dlg.Destroy()
        return True

app = AutolockApp(0)
app.MainLoop()