# 项目作用
处理导出的二进制原始文件

- extractNegativesamples.py：根据切割点数据提取负样本
- processBinFile.py：处理二进制文件
- readBinFile.py：被processBinFile.py调用的函数


# 文件夹及文件的作用
## all_records_for_extractNegtivesamples：存放所有文件的切割点数据
- left_5.3.txt    保存2017年5月3号之后，6月12号之前的测试数据（左手）
- left_6.12.txt   保存2017年6月12号之后的测试数据（左手）
- right_5.3.txt   保存2017年5月3号之后，6月12号之前的测试数据（右手）   
- left6_12.txt    保存2017年6月1号之后的测试数据（右手）

## single_record_for_extractNegativesamples：存放每一次切割文件的数据，数字后为处理日期

## dataset：数据文件
- data：存放处完成的文件
- left：原始的二进制文件（全部人的左手数据）
- right：原始的二进制文件（全部人的右手数据）


