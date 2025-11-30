from cnocr import CnOcr
import os
from tqdm import tqdm

def main():
    ocr = CnOcr()  # 默认模型

    root_dir = "images/record"
    parse_dir = "images/parsed_record_cnocr"
    os.makedirs(parse_dir, exist_ok=True)

    for name in tqdm(os.listdir(root_dir)):
        img_path = os.path.join(root_dir, name)
        # img_path = "Screenshot_2025-07-05-09-42-28-960_com.alibaba.android.rimet.jpg"
        result = ocr.ocr(img_path)
        with open(os.path.join(parse_dir, name + ".txt"), "w", encoding="utf-8") as f:
            for line in result:
                f.write(line['text'] + "\n")
        # break


if __name__ == "__main__":
    main()