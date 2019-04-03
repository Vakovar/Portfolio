#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use showWebview Method"""

import argparse
import sys
import time
import qi


def main(session):
    """
    This example uses the showWebview method.
    To Test ALTabletService, you need to run the script ON the robot.
    """
    # Get the service ALTabletService.

    network_name    = "pepper06"
    network_pw      = "peppermat"
    pepper_ip       = "192.168.43.163"

    try:
        tabletService = session.service("ALTabletService")

        # Ensure that the tablet wifi is enable
        tabletService.enableWifi()
        # Ensure that the tablet wifi can connect to your network
        tabletService.configureWifi("wpa2",network_name,network_pw)
        time.sleep(3)
        # "your network name"
        tabletService.connectWifi(network_name)

        time.sleep(3)

        # Display a web page on the tablet "webpage"
        tabletService.showWebview("https://bitbucket.org/hioarobotics/pepper-docs")

        time.sleep(5)

        # Display a local web page located in boot-config/html folder
        # The ip of the robot from the tablet is 198.18.0.1
        tabletService.showWebview("http://198.18.0.1/apps/boot-config/preloading_dialog.html")

        time.sleep(5)

        # Hide the web view
        tabletService.hideWebview()
    except Exception, e:
        print "Error was: ", e


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.43.163",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
    