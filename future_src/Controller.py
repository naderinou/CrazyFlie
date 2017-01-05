import BLE_CF
import time
from PyObjCTools import AppHelper  # BLE
import objc # BLE
import struct #send
from multiprocessing import Pool

objc.loadBundle("CoreBluetooth", globals(),
                bundle_path=objc.pathForFramework(
                    u'/System/Library/Frameworks/CoreBluetooth.framework/Versions/A/CoreBluetooth'))




crazyflie_service_uuid = CBUUID.UUIDWithString_(u'00000201-1C7F-4F9E-947B-43B7C00A9A08')
crtp_characteristic_uuid = CBUUID.UUIDWithString_(u'00000202-1C7F-4F9E-947B-43B7C00A9A08')
crtp_UpCharacteristic_uuid = CBUUID.UUIDWithString_(u'00000203-1C7F-4F9E-947B-43B7C00A9A08')
crtp_DownCharacteristic_uuid = CBUUID.UUIDWithString_(u'00000204-1C7F-4F9E-947B-43B7C00A9A08')

DEBUG = True
class Controller():

    #initialize class variable
    rollValue = 0
    pitchValue = 1
    yawValue = 0
    thrustValue = 10001


    def __init__(self):
        self.cf = BLE_CF.BLE_CrazyFlie()
        # add methods that the crazyflie executes
        #Pool().map(self.cf.add_callback, self._preCtrlFly())
        Pool().map(self.cf.add_callback, self._liveFly())
        #self.cf.add_callback(self._preCtrlFly)
        #self.cf.add_callback(self._liveFly)
        manager = CBCentralManager.alloc()
        manager.initWithDelegate_queue_options_(self.cf, None, None)

        try:
            AppHelper.runConsoleEventLoop(installInterrupt=True)
        except KeyboardInterrupt:
            AppHelper.stopEventLoop()


    def _setRollValue(value):
        Controller.rollValue += value
        print("Roll value updated : " + str(Controller.rollValue))

    def _setPitchValue(value):
        Controller.pitchValue += value
        print("Pitch value updated : " + str(Controller.pitchValue))

    def _setYawValue(value):
        Controller.yawValue += value
        print("Yaw value updated : " + str(Controller.yawValue))

    def _setThrustValue(value):
        Controller.thrustValue += value
        print("Thrust value updated : " + str(Controller.thrustValue))

    def _getRollValue(self):
        return Controller.rollValue

    def _getPitchValue(self):
        return Controller.pitchValue

    def _getYawValue(self):
        return Controller.yawValue

    def _getThrustValue(self):
        return Controller.thrustValue

    def _liveFly(cf):
        print("Live Mode Control")
        while 1:
            #print(Controller.rollValue, Controller.pitchValue, Controller.yawValue, Controller.thrustValue)
            cf.send_setpoint(Controller.rollValue, Controller.pitchValue, Controller.yawValue, Controller.thrustValue)
            time.sleep(.5)
            #Todo - Just in case
            #self.cf.send_setpoint(0,0,0,0)
            #time.sleep(.5)


    def _preCtrlFly(cf):
        print("Presave Mode Control")
        while 1:
            user_input = input("Roll Pitch Yaw Thrust values por favor : ")
            roll_input_str, pitch_input_str, yaw_input_str, thrust_input_str = user_input.split()
            roll_input_int = int(roll_input_str)
            pitch_input_int = int(pitch_input_str)
            yaw_input_int = int(yaw_input_str)
            thrust_input_int = int(thrust_input_str)
            end_time = time.time() + 5
            while time.time() < end_time:
                # while 1:
                print(roll_input_int, pitch_input_int, yaw_input_int, thrust_input_int)
                cf.send_setpoint(roll_input_int, pitch_input_int, yaw_input_int, thrust_input_int)
                time.sleep(1)
            cf.send_setpoint(0, 0, 0, thrust_input_int / 1.3)
            time.sleep(.500)
            cf.send_setpoint(0, 0, 0, thrust_input_int / 1.6)
            time.sleep(.500)
            cf.send_setpoint(0, 0, 0, thrust_input_int / 2)

if __name__ == "__main__":
    Controller()


