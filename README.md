## 0、钉钉滚动截图保存每月的打开记录
需要手机支持滚动屏幕截图，保存整个月份的打卡记录

## 1、安装cnocr等组件
pip install cnocr tqdm csv -i -i https://pypi.tuna.tsinghua.edu.cn/simple/
将.cnocr目录复制到用户目录下，命令为 cp -r .cnocr ~

## 2、解析手机打卡截图
python parse_all_cn_ocr.py
注意：需要将root_dir改为截图所在目录，将parse_dir改为文字识别结果所在目录

## 3、整理结果
python analyze.py
注意：parse_dir是文字识别结果所在目录，csv_dir是整理的表格结果所在目录，csv_dir_year是按照年份整理的表格目录，img_ori_dir是截图所在目录，img_dir_renamed是按照月份加原名字重新命名的截图目录，img_dir_renamed_clean是仅按照月份重命名的截图目录，最终的统计结果会保存在csv_dir_year/all.csv目录中

## 注意事项
最终的结果没有区分法定节假日和公司调休，按照每天工作时长9小时来统计的加班结果，后续可以自行根据实际情况调整下各自的加班时长
