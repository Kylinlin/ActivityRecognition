import json
import os


data_dir = os.path.abspath('D:\ActivityRecognition\DataSet')

map_for_class = {
    'idle'        : 0,
    'body'        : 1,
    'swing'       : 2,
    'run'         : 3
}

def getHeader(keys, expriment):
    # 返回每个文件对应的列名
    head_dict = {}
    if 'acce' in keys:
        acce_label = ['acceX', 'acceY', 'acceZ']
        for index,label in zip(expriment['acce'], acce_label):
            head_dict[label] = index
    if 'grav' in keys:
        gray_label = ['grayX', 'grayY', 'grayZ']
        for index,label in zip(expriment['grav'], gray_label):
            head_dict[label] = index
    if 'gyro' in keys:
        gyro_label = ['gyroX', 'gyroY', 'gyroZ']
        for index,label in zip(expriment['gyro'], gyro_label):
            head_dict[label] = index
    if 'timestamp' in keys:
        index = expriment['timestamp']
        label = 'timestamp'
        head_dict[label] = index[0]
    if 'undefined' in keys:
        undefined_label = ['undefined_{}'.format(n) for n in expriment['undefined']]
        for index,label in zip(expriment['undefined'], undefined_label):
            head_dict[label] = index

    head_dict = sorted(head_dict.items(), key = lambda d:d[1])
    head_list = []
    for each in head_dict:
        head_list.append(each[0])
    return head_list

def parse_json(json_file):
    # 解析json配置文件，注意，与其他人的json文件不同之处在于添加了几个"undefined"字段
    config_file = json.load(open(json_file))
    read_json = []
    for motion,motion_dict in config_file.items():
        motion_list = []
        class_type = motion_dict['class']
        expriments_list = motion_dict['expriments']
        for expriment in expriments_list:
            brand_name = expriment['name'].split('_')[0]
            dir_name = os.path.join(data_dir, os.path.join(motion, expriment['name']))
            sampleRate = expriment['sampleRate']
            hand = expriment['hand']
            hasHead = expriment['hasHead']
            keys = expriment.keys()
            if hasHead == False :
                header_list = getHeader(keys, expriment)
                motion_list.append(dict(dirname = dir_name, label=map_for_class[class_type], hasHead = hasHead, header=header_list,sampleRate=sampleRate,hand=hand, brand=brand_name))
            elif hasHead == True:
                motion_list.append(dict(dirname = dir_name, label=map_for_class[class_type], hasHead = hasHead, sampleRate=sampleRate,hand=hand, brand=brand_name))
        read_json.append(dict(motion=motion, list=motion_list))

    # print(read_json)
    return read_json