# E710_APIs.py

import time
import queue
from pyImpinj import ImpinjR2KReader
from pyImpinj.constant import READER_ANTENNA
from pyImpinj.enums    import ImpinjR2KFastSwitchInventory

class RFIDReader:
    def __init__(self, port='/dev/ttyS3', antennas=None):
        self.port = port  # 保存传入的串口名称或使用默认值
        # 设置天线列表，如果没有提供，则使用默认值 ['ANTENNA1']
        self.antennas = antennas if antennas is not None else ['ANTENNA1', 'ANTENNA2']
        self.TAG_QUEUE = queue.Queue(1024)
        self.R2000 = ImpinjR2KReader(self.TAG_QUEUE, address=1)
        self.callback = None  # 默认回调函数为空
        self.running = False  # 控制读取循环的标志位

    def set_callback(self, callback):
        self.callback = callback

    def initialize(self):
        try:
            self.R2000.connect(self.port)
            self.R2000.worker_start()
            self.R2000.fast_power(22)
            # 设置指定的工作天线，这里假设可以一次性设置多个天线
            for antenna in self.antennas:
                if antenna in READER_ANTENNA:
                    self.R2000.set_work_antenna(READER_ANTENNA[antenna])
                    print(f"有效的天线编号：{antenna}")
                else:
                    print(f"无效的天线编号：{antenna}")
            self.running = True
        except BaseException as err:
            print(err)
            raise  # 重新抛出异常以便 .NET Core 可以捕捉



    def switch_ant_inventory(self):
        # 初始化 param 字典
        param = dict(Interval=0, Repeat=1)
        antenna_parameters = {
            'ANTENNA1': ('A', 'Aloop'),
            'ANTENNA2': ('B', 'Bloop'),
            'ANTENNA3': ('C', 'Cloop'),
            'ANTENNA4': ('D', 'Dloop')
        }

        # 根据 self.antennas 列表中的天线动态构建 param
        for index, antenna in enumerate(self.antennas, start=1):
            if antenna in antenna_parameters:
                key, loop_key = antenna_parameters[antenna]
                param[key] = getattr(ImpinjR2KFastSwitchInventory, antenna)
                param[loop_key] = 1  # 或者其他你希望设定的 loop 值
        return param  # 返回构建好的 param 字典

    def read_and_process(self):
        param = self.switch_ant_inventory()
        print(param)
        try:
            while self.running:
                try:
                    data = self.TAG_QUEUE.get(timeout=0.2)
                #except BaseException:
                except queue.Empty:
                    self.R2000.fast_switch_ant_inventory(param=param)
                    continue

                self.callback(data)  # 调用回调函数处理数据
        finally:
            self.cleanup()



    def read_and_process_switch(self):
        try:
            while self.running:
                for antenna in self.antennas:
                    self.R2000.set_work_antenna(READER_ANTENNA[antenna])

                    try:
                        data = self.TAG_QUEUE.get(timeout=0.2)
                    except queue.Empty:
                        self.R2000.rt_inventory(repeat=1)
                        continue

                    time.sleep(1)  # 延迟以确保数据读取稳定
                    if 'DONE' != data.get('type') and self.callback:
                        self.callback(data)  # 调用回调函数处理数据
        finally:
            self.cleanup()

    def cleanup(self):
        self.R2000.worker_stop()
        self.R2000.disconnect()
        self.running = False

    def stop(self):
        self.running = False

    def set_antennas(self, antennas):
        """设置要使用的天线列表"""
        self.antennas = antennas

# 测试程序
if __name__ == "__main__":
    def test_callback(data):
        print(f"接收到数据: {data}")

    # 创建 RFIDReader 实例，指定串口和天线
    reader = RFIDReader(port='/dev/ttyS3', antennas=['ANTENNA1', 'ANTENNA2', 'ANTENNA3', 'ANTENNA4'])
    #reader = RFIDReader(port='/dev/ttyS3', antennas=['ANTENNA1'])
    reader.set_callback(test_callback)
    reader.initialize()


    try:
        reader.read_and_process()  # 开始处理数据
    except KeyboardInterrupt:  # 允许使用 Ctrl+C 来停止程序
        pass
    finally:
        reader.stop()  # 停止读取数据
        reader.cleanup()  # 清理资源

