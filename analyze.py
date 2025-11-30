import os
from tqdm import tqdm
import re
from datetime import datetime, timedelta
import csv
import shutil

def save_results_to_csv(results, filename="attendance.csv"):
    header = ["date", "weekday", "start_time", "end_time", "work_hours", "overtime_hours"]

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(results)

    print("CSV 已保存：", filename)


def parse_text(text):
    # 正则
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    datetime_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")

    APPLY_FORCE_START_DATE = datetime(2025, 4, 22)
    FORCE_START_TIME = "09:30:00"

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    results = []

    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # 1. 找到日期行
        if date_pattern.match(line):
            date_str = line
            weekday = ""
            start_time = ""
            end_time = ""
            work_hours = 0.0
            overtime = 0.0

            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # 2. 星期
            if i + 1 < n and ("星期" in lines[i+1]):
                weekday = lines[i+1]
                i += 2
            else:
                i += 1
                continue

            # 3. 查询开始/结束时间字段
            while i < n and not date_pattern.match(lines[i]):
                if lines[i] == "开始时间":
                    if i + 1 < n:
                        m = datetime_pattern.search(lines[i+1])
                        if m:
                            start_time = m.group(1)
                    i += 2
                    continue

                elif lines[i] == "结束时间":
                    if i + 1 < n:
                        m = datetime_pattern.search(lines[i+1])
                        if m:
                            end_time = m.group(1)
                    i += 2
                    continue

                else:
                    i += 1

            # 4. 特殊规则：2025-04-22 之后强制 start_time = date + 09:30:00
            if date_obj >= APPLY_FORCE_START_DATE:
                start_time = f"{date_str} {FORCE_START_TIME}"

            # 5. 计算工作时长
            if start_time and end_time:
                t1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                delta = (t2 - t1).total_seconds() / 3600.0
                work_hours = round(delta, 2)

                # 6. 加班时长（工作时长 - 9），向下取 0.5
                overtime_raw = work_hours - 9
                if overtime_raw > 0:
                    overtime = max(0.5, (int(overtime_raw * 2) / 2))
                else:
                    overtime = 0.0

            results.append((date_str, weekday, start_time, end_time, work_hours, overtime))

        else:
            i += 1

    return results


def dedup_by_first_element(results):
    seen = {}
    for item in results:
        key = item[0]   # tuple 的第一个元素
        if key not in seen:
            seen[key] = item
    return list(seen.values())

def main():
    parse_dir = "images/parsed_record_cnocr"
    os.makedirs(parse_dir, exist_ok=True)
    csv_dir = "images/parsed_record_cnocr_csv"
    os.makedirs(csv_dir, exist_ok=True)

    csv_dir_year = "images/parsed_record_cnocr_csv_year"
    os.makedirs(csv_dir_year, exist_ok=True)

    img_ori_dir = "images/record"
    img_dir_renamed = "images/record_renamed"
    os.makedirs(img_dir_renamed, exist_ok=True)
    img_dir_renamed_clean = "images/record_renamed_clean"
    os.makedirs(img_dir_renamed_clean, exist_ok=True)

    all_results = []
    for name in tqdm(os.listdir(parse_dir)):
        # if "Screenshot_2025-07-05-09-42-28-960_com.alibaba.android.rimet" not in name: continue
        # if "Screenshot_2025-11-25-14-29-10-528_com.eg.android.AlipayGphone" not in name: continue

        with open(os.path.join(parse_dir, name), "r", encoding="utf-8") as f:
            txt = f.read()
            result = parse_text(txt)
            if(len(result)==0): continue
            result=result[::-1]
            all_results += result
            # import pdb; pdb.set_trace()
            save_results_to_csv(result, filename=os.path.join(csv_dir, name + ".csv"))
            data_str = result[0][0][:-3]
            save_results_to_csv(result, filename=os.path.join(csv_dir_year, result[0][0][:-3] + ".csv"))

            #按照图片名称整理图片
            shutil.copy(os.path.join(img_ori_dir, name[:-4]), os.path.join(img_dir_renamed, data_str + "_" + name[:-4]))
            shutil.copy(os.path.join(img_ori_dir, name[:-4]), os.path.join(img_dir_renamed_clean, data_str + ".jpg"))


    # 汇总所有结果
    all_results = dedup_by_first_element(all_results)
    all_results.sort(key=lambda x: x[0])
    save_results_to_csv(all_results, filename=os.path.join(csv_dir_year, "all.csv"))



if __name__ == "__main__":
    main()