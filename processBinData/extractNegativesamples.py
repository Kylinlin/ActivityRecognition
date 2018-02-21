import os
import pandas as pd
import time

def extract_file_path(top_dir, time):
    # 提取全部文件的文件名，等待填充切割信息
    left_file_name = 'left_output_' + time +'.txt'
    left_file_name = os.path.join('single_record_for_extractNegativesamples', left_file_name)
    right_file_name = 'right_output_' + time + '.txt'
    right_file_name = os.path.join('single_record_for_extractNegativesamples', right_file_name)

    left_file = open(left_file_name,'w')
    right_file = open(right_file_name, 'w')
    for tmp_sec_dir in os.listdir(top_dir):
        if tmp_sec_dir == 'negativeSamples' or tmp_sec_dir == 'exception_files':
            continue
        sec_dir = os.path.join(top_dir, tmp_sec_dir)
        for tmp_thr_dir in os.listdir(sec_dir):
            thr_dir = os.path.join(sec_dir, tmp_thr_dir)
            hand = tmp_thr_dir.split('_')[1]
            if hand == 'left':
                for file in os.listdir(thr_dir):
                    file_path = os.path.join(thr_dir, file)

                    tmp_dict_name = file.split('_')[0] + '_left_' + tmp_sec_dir
                    # check_dict[tmp_dict_name] += 1
                    left_file.write(file_path+'\n')

            elif hand == 'right':
                for file in os.listdir(thr_dir):
                    file_path = os.path.join(thr_dir, file)
                    tmp_dict_name = file.split('_')[0] + '_right_' + tmp_sec_dir
                    # check_dict[tmp_dict_name] += 1
                    right_file.write(file_path+'\n')

    # return check_dict

def process_single_file(record_file, brand, experiment_date):
    # 将含有切割点数据的文件读入后切割数据
    negative_sample_dir = 'dataset\\data\\negativeSamples'
    sucess_count = 0
    log_file_name = 'process.log'
    log_file = open(log_file_name, 'a+')         # 把操作记录添加到日志文件中

    if not os.path.exists(negative_sample_dir):  # 创建负样本的文件夹
        os.mkdir(negative_sample_dir)

    if 'left' in record_file:
        negative_sample_dir = os.path.join(negative_sample_dir,brand + '_left_' + experiment_date)

    elif 'right' in record_file:
        negative_sample_dir = os.path.join(negative_sample_dir, brand + '_right_' + experiment_date)
    if not os.path.exists(negative_sample_dir):
        os.mkdir(negative_sample_dir)


    log_file.write('\n记录时间：{}\n'.format(time.strftime('%Y-%m-%d', time.localtime(time.time()))))
    log_file.write('  文件:{} 下有记录:{} 条\n'.format(record_file, len(open(record_file, 'r').readlines())))
    for line in open(record_file, 'r'):
        try:
            if line == ' ':
                continue
            if line.startswith('#'):
                continue
            record = line.strip()
            messages_list = record.split(' ')
            file_path = messages_list[0]
            split_point_head = int(messages_list[1])
            split_point_discard = int(messages_list[2])
            split_point_tail = int(messages_list[3])
            person_name = file_path.split('.')[0].split('\\')[-1]

            ori_pd = pd.read_excel(file_path)
            negative_sample_head = ori_pd.iloc[0:split_point_head,:]
            negative_sample_tail = ori_pd.iloc[split_point_tail:,:]
            save_sample = ori_pd.iloc[split_point_discard:split_point_tail,:]

            negative_sample_head_filename = person_name + '_head.xlsx'
            negative_sample_tail_filename = person_name + '_tail.xlsx'

            save_sample_filename = os.path.join(os.path.dirname(file_path), person_name + '.xlsx')

            os.remove(file_path) # 删除原来的文件

            negative_sample_head.to_excel(os.path.join(negative_sample_dir,negative_sample_head_filename), index=False, header=True)
            negative_sample_tail.to_excel(os.path.join(negative_sample_dir,negative_sample_tail_filename), index=False, header=True)
            save_sample.to_excel(save_sample_filename, index=False, header=True)
            sucess_count += 1
            print('成功处理文件： {}'.format(file_path))
        except Exception as e:
            log_file.write(e + ' ' + file_path + '\n')
            continue
    log_file.write('  文件:{} 成功处理记录:{} 条\n'.format(record_file, sucess_count))



if __name__ == '__main__':
    # extract_file_path(os.path.join('dataset', 'data'), '8-7')

    brand = 'huami'
    # experiment_date = '20170503'
    experiment_date = '20170612'
    record_dir = 'single_record_for_extractNegativesamples';
    process_single_file( os.path.join(record_dir,'left_output_8-7.txt'), brand, experiment_date)
    process_single_file( os.path.join(record_dir,'right_output_8-7.txt'), brand, experiment_date)
