import pandas as pd
import os

from utils.getCharacteristics import getCharateristics
from utils.parseJson import parse_json

features_dir = os.path.join(os.path.pardir, os.path.join('jupyterNotebook', 'dataset'))
data_dir = os.path.abspath('D:\Repository\ActivityRecognition\dataSet\dataPrepared')
log_file = open('process.log', 'a+')

individuals = [
        'Belly','ChenCi','ChenHeDing','ChenXuanJin','ChenXue','DingWeiJie','FengShuYi','GaoMin',
        'GuoXinYi','HuangMingMei','HuangSiMin','Jessie','KongLingSheng','LiTing','LiYang','LiYuePeng',
        'LiZheMing','LiZunCong','LieZhenRong','LinGuanHao','LinMiQing','LinRuiSheng','LiuJinGe','LuJieYu',
        'LuZhiHao','LuoLi','LuoShuYing','MoYiHua','Molly','OuYangJiang','TaoKun','WangHuan','WangWenWei',
        'WangZhouHong','WengCanBiao','ZengLiYa','ZhangTao','ZhangZhuang','ZhaoRan','ZhaoYun','ZouBoWen','ZuoTianLong',
        'DaiLu','LiuSheng','YuShaoQing','ChenGuan','KongTaoMing','ChenLiang','FuWenHui','LiPeiQi','ZhouYiTing'
    ]

check_list = individuals

coloum_name = [    'acceX_rms', 'acceX_mean', 'acceX_std', 'acceX_int_rms', 'acceX_fft', 'acceX_idx',
                   'acceY_rms', 'acceY_mean', 'acceY_std', 'acceY_int_rms', 'acceY_fft', 'acceY_idx',
                   'acceZ_rms', 'acceZ_mean', 'acceZ_std', 'acceZ_int_rms', 'acceZ_fft', 'acceZ_idx',
                   'label', 'name', 'file_path']

def extract_feature(map_list):
    #逐个读取data文件夹下子文件夹，并给每个子文件夹生成三个已经提取特征的合并文件
    merge_all_train_df = pd.DataFrame()
    output_all_train_file = 'featuresForTrain.csv'
    winlen = 4
    wingap = 0.5
    # winlen = 1
    # wingap = 0.2

    test_data_map = {}

    for x in individuals:
        test_data_map[x] = pd.DataFrame()

    if not os.path.exists(features_dir):
        os.mkdir(features_dir)

    indi_dir = os.path.join(features_dir, 'individualTestSet')
    if not os.path.exists(indi_dir):
        os.mkdir(indi_dir)

    for motion_dict in map_list:
        # 循环所有运动分类
        motion = motion_dict['motion']
        for each_dict in motion_dict['list']:
            dirname = each_dict['dirname']
            label = each_dict['label']
            hasHead = each_dict['hasHead']
            fs = each_dict['sampleRate']
            hand = each_dict['hand']
            brand = each_dict['brand']

            # if hand != 'left':  # 只训练左手的数据
            #     continue
            if brand != 'huami': # 只训练华米品牌的数据
                continue

            sample_gap = int(fs * wingap)  # 滑动窗口
            sample_len = int(fs * winlen)
            if hasHead == False:
                header = each_dict['header']

            for file in os.listdir(dirname):
                # 循环一个运动分类下的每一个实验对应的文件夹
                # try:
                file_full_path = os.path.join(dirname, file)
                print('正在处理文件：' + os.path.join(dirname, file))
                if hasHead == False:
                    ori_df = pd.read_csv(os.path.join(dirname, file), names=header)
                else:
                    ori_df = pd.read_csv(os.path.join(dirname, file))

                individual_name = file.split('_')[0]
                tmp_df = extract_feature_from_dataframe(ori_df, sample_gap, sample_len, label, winlen, fs, file_full_path, individual_name)
                test_data_map[individual_name] = pd.concat((test_data_map[individual_name], tmp_df))
                merge_all_train_df = pd.concat((merge_all_train_df, tmp_df.drop(['file_path'], axis=1)))

        print('运动分类{} 提取特征完成'.format(motion))

    merge_all_train_df.to_csv(os.path.join(features_dir,output_all_train_file), header=True, index=False)


    for indi_name, indi_df in test_data_map.items():
        if len(indi_df) == 0:
            continue
        indi_file = os.path.join(indi_dir, indi_name)
        indi_df.to_csv(indi_file+'.csv', header=True, index=False)
    print('All done!')


def extract_feature_from_dataframe(dataframe, step_window, step_sample, label, winlen, fs, file_full_path, individual_name='no'):
    # 从一个DataFrame中提取特征
    sample_len = len(dataframe)
    feature_list = []

    for i in range(0, sample_len - int(winlen * fs), step_window):
        # 只提取加速度的三个数据
        acceX_col = dataframe['acceX'][i: i + step_sample]
        acceY_col = dataframe['acceY'][i: i + step_sample]
        acceZ_col = dataframe['acceZ'][i: i + step_sample]

        acceX_features = getCharateristics(acceX_col, winlen, fs)
        acceY_features = getCharateristics(acceY_col, winlen, fs)
        acceZ_features = getCharateristics(acceZ_col, winlen, fs)

        tmp_list = []
        for each in acceX_features:
            tmp_list.append(each)
        for each in acceY_features:
            tmp_list.append(each)
        for each in acceZ_features:
            tmp_list.append(each)
        tmp_list.append(label)
        tmp_list.append(individual_name)
        tmp_list.append(file_full_path)
        feature_list.append(tmp_list)

    result_df = pd.DataFrame(feature_list,columns=coloum_name)
    return result_df

if __name__ == '__main__':
    json_file = 'dlrcDataStructure.json'
    map_list = parse_json(json_file)
    extract_feature(map_list)


