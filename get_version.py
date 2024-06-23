# !/usr/bin/python
# -*- coding:utf-8 -*-
""" Test script."""
# Python:   3.6.5+
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test script( Auto Config ).
# Package:  pip3 install pyImpinj.
# Drivers:  None.
# History:  2020-02-27 Ver:1.0 [Heyn] Initialization

import time
import queue
import logging

from pyImpinj import ImpinjR2KReader

from pyImpinj.constant import READER_ANTENNA, FREQUENCY_TABLES
from pyImpinj.enums    import ImpinjR2KFastSwitchInventory

logging.basicConfig( level=logging.ERROR )

def main( ):
    TAG_QUEUE = queue.Queue( 1024 )
    R2000 = ImpinjR2KReader( TAG_QUEUE, address=1 )

    try:
        R2000.connect( '/dev/ttyUSB0' )
    except BaseException as err:
        print( err )
        return

    R2000.worker_start()
    #R2000.fast_power( 30 )
    # print( R2000.set_frequency_region( start=905, stop=911.3 ) )
    # print( R2000.get_frequency_region( ) )
    time.sleep( 1 )
    data = R2000.get_version( )
    print("Version:",[ '%02X' % x for x in data ])
    data = R2000.get_work_antenna()
    print("antenna:",[ '%02X' % x for x in data ])

if __name__ == "__main__":
    main()
