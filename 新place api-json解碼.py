# Date： 2024/11/17 04:02
# Author: Mr. Q
# Introduction：

import time

start_time = time.time()
print(start_time)
print("======================================")
import json
import csv

# 定義文件路徑
input_txt_file = r"D:\桌面散件\Study\★博士班\△真D Lab\資料科學研究\爬蟲\2025科技部\Google map評論\input.txt"  # 替換為你的txt文件路徑
output_csv_file = r"D:\桌面散件\Study\★博士班\△真D Lab\資料科學研究\爬蟲\2025科技部\Google map評論\output.csv"  # 替換為你的輸出csv文件路徑

# 讀取JSON數據
with open(input_txt_file, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# 提取JSON中的相關數據
data_rows = []
for review in json_data.get("reviews", []):
    data_rows.append({
        "Place ID": json_data["id"],
        "Name": json_data["name"],
        "Phone Number": json_data.get("nationalPhoneNumber"),
        "Formatted Address": json_data["formattedAddress"],
        "Rating": json_data.get("rating"),
        "Review Author": review["authorAttribution"]["displayName"],
        "Review Rating": review["rating"],
        "Review Text": review["text"]["text"],
        "Review Publish Time": review["publishTime"],
        "Author Profile": review["authorAttribution"]["uri"]
    })

# 將數據寫入CSV文件
with open(output_csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = [
        "Place ID", "Name", "Phone Number", "Formatted Address", "Rating",
        "Review Author", "Review Rating", "Review Text", "Review Publish Time", "Author Profile"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data_rows)

print(f"JSON數據已成功解析並保存到CSV文件：{output_csv_file}")



print("======================================")
print("ok!!")

end_time = time.time()
print(end_time)
duration = end_time - start_time
print(f"程式執行時間為 {duration:.2f} 秒")
