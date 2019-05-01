import SensorThread
import BluetoothCommunicationThread
import threading

try:
    sensorThread = threading.Thread(target=SensorThread.run)
    bluetoothThread = threading.Thread(target=BluetoothCommunicationThread.run)

    sensorThread.daemon = True
    bluetoothThread.daemon = True
    sensorThread.start()
    bluetoothThread.start()

    
except:
    print("Error starting threads")
