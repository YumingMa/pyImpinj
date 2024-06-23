# !/usr/bin/python
# -*- coding:utf-8 -*-
""" Test script."""
# Python:   3.6.5+
# Platform: Windows/Linux/MacOS
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Test script.
# Package:  None.
# Drivers:  None.
# History:  2020-02-20 Ver:1.0 [Heyn] Initialization

import time
import queue
import struct
import logging

from pyImpinj import ImpinjR2KReader

from pyImpinj.constant import READER_ANTENNA
from pyImpinj.enums    import ImpinjR2KFastSwitchInventory

logging.basicConfig( level=logging.INFO )

def main( ):
    TAG_QUEUE = queue.Queue( 1024 )
    R2000 = ImpinjR2KReader( TAG_QUEUE, address=1 )

    try:
        R2000.connect( '/dev/ttyUSB0' )
    except BaseException as err:
        print( err )
        return

    R2000.worker_start()
    R2000.fast_power( 22 )
    R2000.set_work_antenna( READER_ANTENNA['ANTENNA1'] )

    while True: #将这个True修改为上层应用的程序是否停止的变量标志位，如果上次应用将此标志位设置为“停止”，那循环读取就停止
        try:
            data = TAG_QUEUE.get( timeout=0.2 )
        except BaseException:
            R2000.rt_inventory( repeat=1 )
            continue

        time.sleep( 1 )     # Read data must be delay 1s above.
        if 'DONE' == data.get('type'):
            continue

        #将数据反馈给上层应用，交给上层应用处理。

        print('\n', data)
        print( 'EPC  --> {}'.format( data['epc'] ) )
        print( 'TID  >>> ', end='' )
        print( R2000.read( data['epc'], bank='TID',  size=3 ) )
        print( 'EPC  >>> ', end='' )
        print( R2000.read( data['epc'], bank='EPC',  size=8 )[8:] ) # Removed PC(2Bytes) and CRC[2Bytes]
        print( 'USER >>> ', end='' )
        print( R2000.read( data['epc'], bank='USER', size=2 ) )

if __name__ == "__main__":
    main()
