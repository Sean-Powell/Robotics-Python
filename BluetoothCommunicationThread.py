from bluetooth import *

latestGpsData = 0

def run():
    getCommuicationData()



def getCommuicationData():
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service(server_sock, "RPiServer",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE], )

    while True:
        print("Wating for RFCOMM connection")

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        try:
            # client_ock has no attribute 'rcv'
            gpsData = client_sock.recv(1024)
            if len(gpsData) == 0:
                print("GPS data is empty")
                break
            else:
                print("GPS data received ", gpsData)

                # call 2nd class to handle gpsData

        except IOError:
            pass
        except KeyboardInterrupt:
            print("Keyboard interrupt")

            client_sock.close()
            server_sock.close()

            print("All done")
            break
    return


