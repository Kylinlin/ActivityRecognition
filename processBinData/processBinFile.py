# 将原始的二进制文件中的数据提取出来
import os
import readBinFile
import time

map_for_class = {
    '健走_打电话'  : 'phonecall',
    '健走_端着手机': 'playPhone',
    '健走_打伞'    : 'umbrella',
    '健走_插裤口袋': 'trousersPocket',
    '健走_自然摆臂': 'swing',
    '慢跑_自然摆臂': 'slowRun',
    '快跑_自然摆臂': 'fastRun',
    '健走_端手机'  : 'playPhone',
    '健走_提重物'  : 'heavybag',
    '健走_提物品'  : 'heavybag',
    '健走_提东西'  : 'heavybag',
    }

map_for_individual = {
    '高总'         :   'GaoMin',
    '林冠豪'       :   'LinGuanHao',
    '陳辭'         :   'ChenCi',
    '陈辞'         :   'ChenCi',
    '黃思敏'       :   'HuangSiMin',
    '黄思敏'       :   'HuangSiMin',
    '陳雪'         :   'ChenXue',
    '陈雪'         :   'ChenXue',
    '王歡'         :   'WangHuan',
    '王欢'         :   'WangHuan',
    '李婷'         :   'LiTing',
    '罗淑英'       :   'LuoShuYing',
    '淑英'         :   'LuoShuYing',
    '淑仪'         :   'FengShuYi',
    '冯淑仪'         :   'FengShuYi',
    '刘金戈'       :   'LiuJinGe',
    '欧阳江'       :   'OuYangJiang',
    '文威'         :   'WangWenWei',
    '王文威'       :   'WangWenWei',
    '罗梨'         :   'LuoLi',
    '天龙'         :   'ZuoTianLong',
    '左天龙'         :   'ZuoTianLong',
    '王周红'      :   'WangZhouHong',
    'Jessie'       :    'Jessie',
    '李悦鹏'       :   'LiYuePeng',
    '赵云'        :   'ZhaoYun',
    '陶昆'        :   'TaoKun',
    '丁伟杰'       :   'DingWeiJie',
    'Belly'       :   'Belly',
    '和定'        :   'ChenHeDing',
    '志豪'        :   'LuZhiHao',
    '金戈'        :   'LiuJinGe',
    '赵然'        :   'ZhaoRan',
    '陈和定'       :   'ChenHeDing',
    '李悅鵬'       :   'LiYuePeng',
    '代露'         :   'DaiLu',
    '刘晟'        :    'LiuSheng',
    '周怡婷'       :    'ZhouYiTing',
    '趙然'        :    'ZhaoRan',
    '李佩起'       :   'LiPeiQi',
    '陈亮'        :   'ChenLiang',
    '付文慧'       :   'FuWenHui',
    '孔涛铭'       :   'KongTaoMing',
    '余劭晴'       :   'YuShaoQing',
    '灿标'         :   'WengCanBiao',
    '陈冠'         :   'ChenGuan'
}

def processDir(dirName, experiment_date, hasPhoneTag = False):

    brand_of_watch = 'huami'            # 手表品牌
    top_level_dir = os.path.join('../dataset', 'dataPrepared')              # 一级目录
    csv_format = True                  # 测试时使用csv格式，如果需要xlsx格式，就设置为False
    log_file= 'process.log'             # 日志文件

    exp_date = time.strptime(experiment_date, '%Y%m%d')
    if not os.path.exists(top_level_dir):
        os.mkdir(top_level_dir)
    if 'right' in dirName:
        hand = 'right'
    elif 'left' in dirName:
        hand = 'left'
    log_file = open(log_file, 'a+')
    print('文件夹:{} 下有文件:{} 个'.format(dirName,len(os.listdir(dirName))))
    log_file.write('\n记录时间：{}\n'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))))
    log_file.write('  文件夹:{} 下有文件:{} 个\n'.format(dirName,len(os.listdir(dirName))))
    exception_files = []
    count = 0
    for file in os.listdir(dirName):
        full_file = os.path.join(dirName, file)
        # 创建每个文件对应的分类文件夹
        filename_split = file.split('_')
        #print(filename_split)
        if (len(filename_split) == 6):
            hasPhoneTag = True
        else:
            hasPhoneTag = False

        if len(filename_split) == 1:
            exception_files.append(full_file)
            continue
        file_date = time.strptime(filename_split[0][0:8], '%Y%m%d')
        if file_date < exp_date:
            continue

        # 20170612093623_代露_右手_健走_自然摆臂.bin
        if hasPhoneTag == False:
            class_name_key = filename_split[-2] + "_" + filename_split[-1].split('.')[-2]
        else:
        # 20170731094041_余劭晴_左手_健走_自然摆臂_Galaxy A5 (2016).bin
            class_name_key = filename_split[-3] + "_" + filename_split[-2]
        individual_key = filename_split[1]

        try:
            individual_value = map_for_individual[individual_key]
        except Exception as e:
            print('人名匹配异常')
            exception_files.append(full_file) # 当文件名中的人名对应不上映射表时将该文件作为异常处理
            continue

        if class_name_key not in map_for_class.keys():
            print('运动类别名匹配异常')
            #print(class_name_key)
            exception_files.append(os.path.join(dirName, file))
            continue
        class_name_value = map_for_class[class_name_key]
        second_level_dir = os.path.join(top_level_dir, class_name_value)
        if not os.path.exists(second_level_dir):
            os.mkdir(second_level_dir)

        #获取文件的创建日期，如果不含有该日期对应的文件夹，就新建一个文件夹
        third_level_dir_tmp = brand_of_watch + '_' + hand + '_' + experiment_date
        third_level_dir = os.path.join(second_level_dir, third_level_dir_tmp)
        if not os.path.isdir(third_level_dir):
            os.mkdir(third_level_dir)

        #创建文件对应的文件名
        if csv_format == True:
            individual_file = os.path.join(third_level_dir, individual_value + '_' + filename_split[0]  + '.csv')
        else:
            individual_file = os.path.join(third_level_dir, individual_value + '_' + filename_split[0] + '.xlsx')
        if not os.path.exists(individual_file):
            output_file = individual_file
            readBinFile.readfile(full_file, output_file, csv_format)
        else:
            print('有文件名重复了')
        count += 1

    print('文件夹:{} 下成功转化文件:{} 个'.format(dirName,count))
    log_file.write('  文件夹:{} 下成功转化文件:{} 个\n'.format(dirName,count))

    #处理异常文件
    if len(exception_files) != 0:
        exception_dir = os.path.join(top_level_dir,'exception_files')
        if not os.path.exists(exception_dir):
            os.mkdir(exception_dir)
        for exception_file in exception_files:
            if csv_format == True:
                tmp_file = exception_file.split('\\')[-1].split('.')[0] + '.csv'
            else:
                tmp_file = exception_file.split('\\')[-1].split('.')[0] + '.xlsx'
            exception_output_file = os.path.join(exception_dir, tmp_file)
            readBinFile.readfile(exception_file, exception_output_file, csv_format)

    print('处理了{}个异常文件'.format(len(exception_files)))
    log_file.write('  处理了{}个异常文件\n'.format(len(exception_files)))
    print(exception_files)
    tmp = ''
    for file in exception_files:
        tmp += file
    log_file.write('  包括以下文件：' + tmp)

if __name__ == '__main__':
    # 这是分批处理新数据
    #processDir(os.path.join('../dataset/testSet/processBinData', 'left'),'20170612',hasPhoneTag=True)
    #processDir(os.path.join('../dataset/testSet/processBinData', 'right'),'20170612', hasPhoneTag=True)

    # 这是一次性处理全部数据
    processDir('../dataset/binaryDataSet/left_5.3', '20170503', hasPhoneTag=True)
    processDir('../dataset/binaryDataSet/left_6.12', '20170612', hasPhoneTag=True)
    processDir('../dataset/binaryDataSet/right_5.3', '20170503', hasPhoneTag=True)
    processDir('../dataset/binaryDataSet/right_6.12', '20170612', hasPhoneTag=True)
