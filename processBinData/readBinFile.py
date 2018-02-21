import struct
import numpy as np
import pandas as pd
import os


def readfile(filename, out_file, csv_format=True):
    # print(filename)
    # print(os.stat(filename).st_size)
    if os.stat(filename).st_size == 0:
        print()
        return
    imu_datas = []
    file_obj = open(filename, 'rb')
    try:
        state = struct.unpack('b', file_obj.read(1))[0]
        samplerate = struct.unpack('b', file_obj.read(1))[0]
        label = struct.unpack('b', file_obj.read(1))[0]
        while label > 0:
            if label == 10:
                data = np.array(struct.unpack('>fffffffff', file_obj.read(4 * 9)))
                imu_datas.append(data)
            elif label == 11:
                data = struct.unpack('>dd', file_obj.read(8 * 2))

            data = file_obj.read(1)
            if (len(data) > 0):
                label = struct.unpack('b', data)[0]
            else:
                label = -1
    except:
        print(filename)
    finally:
        file_obj.close()

    imu_datas = np.array(imu_datas)
    columns = ['acceX', 'acceY', 'acceZ', 'magnX', 'magnY', 'magnZ', 'gyroX', 'gyroY', 'gyroZ']
    # 三轴加速度，磁场计，陀螺仪
    df = pd.DataFrame(imu_datas, columns=columns)
    if csv_format == True:
        df.to_csv(out_file, index=False, header=True)
    else:
        df.to_excel(out_file, index=False, header=True)

    print('{} Done'.format(out_file))

if __name__ == '__main__':
    #filename = '20170519153938_王周红_右手_健走_自然摆臂.bin'
    filename = '20180202150910_林一_左手_健走_测试_小米手机.bin'
    readfile(filename,'tttt.csv')