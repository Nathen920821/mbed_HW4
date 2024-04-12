# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
       if isNewDev:
          print ("Discovered device", dev.addr)
       elif isNewData:
          print ("Received new data from", dev.addr)
class WriteDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)
scanner = Scanner().withDelegate(ScanDelegate())
dev = Peripheral("d1:0f:23:61:ec:3e", "random")
#
print ("Connecting...")
dev.setDelegate(WriteDelegate())
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    testService = dev.getServiceByUUID(UUID(0x180D))
    for ch in testService.getCharacteristics():
        print (str(ch))
    ch = dev.getCharacteristics(uuid=UUID(0x2A37))[0]

    descriptors = ch.getDescriptors(forUUID=0x2902)[0]
    print(descriptors)
    # Changing the value of the descriptor
    new_value = b'\x01\x00'  # Provide the new valu

    desc_read = descriptors.read()
    print(desc_read)

    descriptors.write(new_value)
    while True:
        if dev.waitForNotifications(1.0):
            continue
        print ("Waiting...")
    desc_read = descriptors.read()
    print(desc_read)
    #ch.write(bytes("python","utf-8"),withResponse = True)
#
finally:
    dev.disconnect()
