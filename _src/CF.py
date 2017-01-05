from PyObjCTools import AppHelper  # BLE
import objc  # BLE
import sys  # IO
import time # time.sleep()
import struct #send
from threading import Timer
from threading import Thread


objc.loadBundle("CoreBluetooth", globals(),
                bundle_path=objc.pathForFramework(
                    u'/System/Library/Frameworks/CoreBluetooth.framework/Versions/A/CoreBluetooth'))

crazyflie_service_uuid = CBUUID.UUIDWithString_(u'00000201-1C7F-4F9E-947B-43B7C00A9A08')
crtp_characteristic_uuid = CBUUID.UUIDWithString_(u'00000202-1C7F-4F9E-947B-43B7C00A9A08')
crtp_UpCharacteristic_uuid = CBUUID.UUIDWithString_(u'00000203-1C7F-4F9E-947B-43B7C00A9A08')
crtp_DownCharacteristic_uuid = CBUUID.UUIDWithString_(u'00000204-1C7F-4F9E-947B-43B7C00A9A08')


def main():
    cf = BLECrazyFlie()
    # add methods that the crazyflie executes
    cf.add_callback(fly)

    manager = CBCentralManager.alloc()
    manager.initWithDelegate_queue_options_(cf, None, None)

    try:
        AppHelper.runConsoleEventLoop(installInterrupt=True)
    except KeyboardInterrupt:
        AppHelper.stopEventLoop()


def fly(cf):
    while 1:

        user_input= input("Roll Pitch Yaw Thrust values por favor : ")
        roll_input_str, pitch_input_str, yaw_input_str, thrust_input_str = user_input.split()
        roll_input_int = int(roll_input_str)
        pitch_input_int = int(pitch_input_str)
        yaw_input_int = int(yaw_input_str)
        thrust_input_int = int(thrust_input_str)
        end_time = time.time() + 8
        while time.time() < end_time:
        #while 1:
            print(roll_input_int, pitch_input_int, yaw_input_int, thrust_input_int)
            cf.send_setpoint(roll_input_int, pitch_input_int, yaw_input_int, thrust_input_int)
            time.sleep(.5)
            cf.send_setpoint(0, 0, 0, 0)
            time.sleep(2)
        cf.send_setpoint(0, 0, 0, thrust_input_int / 1.3)
        time.sleep(.500)
        cf.send_setpoint(0, 0, 0, thrust_input_int / 1.6)
        time.sleep(.500)
        cf.send_setpoint(0, 0, 0, thrust_input_int / 2)

class BLECrazyFlie():
    def __init__(self):
        self.manager = None
        self.peripheral = None
        self.service = None
        self.crtp_characteristic_uuid = None
        self.connected = False
        self.callbacks = []

        self.init = False

    def send_setpoint(self, roll, pitch, yaw, thrust):
        # print ("Roll : {1} , Pitch : {2} , Yaw : {3} , Thrust : {4} ".format(roll, pitch, yaw, thrust))
        # print ("<BfffH : {1} , Pitch : {2} , Yaw : {3} , Thrust : {4} ".format(roll, pitch, yaw, thrust))
        ##Format Python :
        # B : integer, size : 1
        # f : float, size : 4
        # H : interger, size : 2
        ##Format C :
        # B : unsigned char, size : 1
        # f : float, size : 4
        # H : unsigned short, size : 2
        data = struct.pack('<BfffH', 0x30, roll, -pitch, yaw, thrust)
        # print("data value : {}".format(data))
        bytes = NSData.dataWithBytes_length_(data, len(data))
        # print("bytes value : {}".format(data))
        self.peripheral.writeValue_forCharacteristic_type_(bytes, self.crtp_characteristic_uuid, 1)

    def add_callback(self, cb):
        if ((cb in self.callbacks) is False):
            self.callbacks.append(cb)

    def remove_callback(self, cb):
        self.callbacks.remove(cb)

    def call(self, *args):
        for cb in self.callbacks:
            cb(*args)

    def centralManagerDidUpdateState_(self, manager):
        # Invoked when the central manager's state is updated.
        if self.connected == False:
            self.manager = manager
            manager.scanForPeripheralsWithServices_options_(None, None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        # Invoked when the central manager discovers a peripheral while scanning.
        print('Found ' + peripheral.name())
        if peripheral.name() == 'Crazyflie':
            manager.stopScan()
            self.peripheral = peripheral
            manager.connectPeripheral_options_(self.peripheral, None)

    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        # Invoked when a connection is successfully created with a peripheral.
        print('Connected to ' + peripheral.name())
        self.connected = True
        self.peripheral.setDelegate_(self)
        self.peripheral.readRSSI()
        self.peripheral.discoverServices_([crazyflie_service_uuid])

    def centralManager_didFailToConnectPeripheral_error_(self, manager, peripheral, error):
        # Invoked when the central manager fails to create a connection with a peripheral.
        print(repr(error))

    def centralManager_didDisconnectPeripheral_error_(self, manager, peripheral, error):
        # invoked when an existing connection with a peripheral is torn down.
        self.connected = False
        AppHelper.stopEventLoop()

    def peripheral_didDiscoverServices_(self, peripheral, error):
        # Invoked when you discover the peripheral's available services.
        if (error == None):
            self.service = self.peripheral.services()[0]
            self.peripheral.discoverCharacteristics_forService_([crtp_characteristic_uuid], self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        # Invoked when you discover the characteristics of a specified service.
        for characteristic in self.service.characteristics():
            if characteristic.UUID().UUIDString() == crtp_characteristic_uuid.UUIDString():
                self.crtp_characteristic_uuid = characteristic
                self.peripheral.setNotifyValue_forCharacteristic_(True, self.crtp_characteristic_uuid)

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        # Invoked when you write data to a characteristic's value.
        if error != None:
            print(repr(error))

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        # Invoked when the peripheral receives a request to start or stop providing notifications
        #  for a specified characteristic's value.
        print('Receiving notifications')
        # unlock thrust
        #self.send_setpoint(0, 0, 0, 0)
        self.call(self)

    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        # Invoked when you retrieve a specified characteristic's value,
        # or when the peripheral device notifies your app that the characteristic's value has changed.
        print('Updated value')
        print(repr(characteristic.value().bytes().tobytes()))


#if __name__ == "__main__" is used to execute some code
# only if the file was run directly, and not imported.
if __name__ == "__main__":
    main()
