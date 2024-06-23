using Python.Runtime;
using System;

namespace RFIDReaderApp
{
    class Program
    {
        public static void DataCallback(dynamic data)
        {
            Console.WriteLine("接收到的数据: " + data.ToString());
            // 根据需要处理数据
        }

        static void Main(string[] args)
        {
            Environment.SetEnvironmentVariable("PYTHONNET_PYDLL", "/usr/lib/arm-linux-gnueabihf/libpython3.7m.so");
            Environment.SetEnvironmentVariable("PYTHONHOME", "/usr");

            PythonEngine.Initialize();
            using (Py.GIL())
            {
                dynamic sys = Py.Import("sys");
                sys.path.append("/root/indy/pyImpinj");
                dynamic E710APIs = Py.Import("E710_APIs");

                // 从命令行参数中获取串口和天线配置，如果没有提供，则使用默认值
                string port = args.Length > 0 ? args[0] : "/dev/ttyS3";
                string[] antennas = args.Length > 1 ? args[1].Split(',') : new string[] { "ANTENNA1" };

                // 创建一个 Python 列表以存储天线配置
                dynamic pyAntennas = new PyList();
                foreach (string antenna in antennas)
                {
                    pyAntennas.append(antenna);
                }

                // 使用提供的串口和天线配置实例化 RFIDReader 类
                using (dynamic reader = E710APIs.RFIDReader(port, pyAntennas))
                {
                    reader.initialize();
                    reader.set_callback(new Action<dynamic>(DataCallback));

                    // 此方法可能需要在不同的线程上运行
                    reader.read_and_process();

                    // 根据需要进行停止和清理操作
                    // reader.stop();
                    // reader.cleanup();
                }
            }
            PythonEngine.Shutdown();
        }
    }
}
