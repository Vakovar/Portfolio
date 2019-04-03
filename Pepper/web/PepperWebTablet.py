"""
Script for creating a webpage-interface to pepper
Local files located at /data/home/nao/.local/share/PackageManager/apps/customPage/html/
Script created by Persijn
"""
import qi
import sys
import time
import naoqi
import argparse

def main(args):
    #print args
    service = naoqi.ALProxy("ALTabletService", args.ip, 9559)
    #service.enableWifi()
    #service.configureWifi("wpa2","LAPTOP_NET5","Pepper123")
    #con = service.connectWifi("LAPTOP_NET5")
    #if (con):
    #    print "connected"
    #service.loadUrl("http://google.com")
    show(service)
    reload(service)
    #runJs(service)
    #hide(service)

def runJs(service):

    script = """
        var name = prompt("name", "Test")
        ALTabletBinding.raiseEvent(close)
    """
    #signalID = 0

    def callback(event):
        print "closePage "+event
        #service.hideWebview()
        #service.onJSEvent.disconnect(signalID)

    #singalID = service.onJSEvent.connect(callback)
    service.executeJS(script)
    

def reload(service):
    service.reloadPage(True)

def show(service):
    robotIp = service.robotIp()
    service.showWebview("http://"+robotIp+"/apps/customPage/hello-website.html")

def hide(service):
    print "End webview"
    service.hideWebview()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.137.57",
                        help="Robot IP address. On robot or Local Naoqi: use the hotstop.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    main(args)