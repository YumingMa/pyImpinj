import serial
import time

# 打开串口
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

# 要发送的字节序列
bytes_to_send = [0xA0, 0x03, 0x01, 0x72, 0xEA]

# 发送字节序列
ser.write(serial.to_bytes(bytes_to_send))

# 给设备一些时间来响应
time.sleep(0.1)

# 读取返回的数据
# 注意：这里假设返回数据的长度是已知的，例如7个字节
# 如果不知道长度，可以适当设置timeout并连续读取，直到没有更多数据为止
returned_data = ser.read(7)

# 关闭串口
ser.close()

# 打印返回的数据（以十六进制形式）
print(returned_data.hex())

