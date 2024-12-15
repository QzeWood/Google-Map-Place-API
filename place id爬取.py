# Date： 2024/11/16 17:56
# Author: Mr. Q
# Introduction：

import time
import requests
import csv
import os
import winsound  # 用於播放提示音

start_time = time.time()
print(start_time)
print("======================================")

# Google Maps API Key
API_KEY = "AIzaSyBaKsCij23Pap0MbkSvgVAkWhx5vgroHlc"

# API URL 模板
API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

# 查詢參數
QUERY = "路易莎 in Taiwan"
FIELDS = "business_status,formatted_address,place_id,name,address_components,adr_address,url,geometry,user_ratings_total,rating"
CSV_FILE = r"D:\桌面散件\Study\★博士班\△真D Lab\資料科學研究\爬蟲\2025科技部\Google map評論\全台路易莎調研.csv"

# 台灣主要城市區塊地理座標和半徑（米）
LOCATIONS = [
    {"name": "台北 - 中正區 + 萬華區", "query": "路易莎 in Zhongzheng District and Wanhua District Taipei"},
    {"name": "台北 - 信義區 + 大安區 + 文山區", "query": "路易莎 in Xinyi, Da’an and Wenshan Districts Taipei"},
    {"name": "台北 - 松山區 + 北投區 + 內湖區 + 南港區",
     "query": "路易莎 in Songshan, Beitou, Neihu and Nangang Districts Taipei"},
    {"name": "台北 - 士林區 + 大同區 + 中山區", "query": "路易莎 in Shilin, Datong and Zhongshan Districts Taipei"},
    {"name": "新北 - 中和區 + 永和區 + 新店區 + 板橋區",
     "query": "路易莎 in Zhonghe, Yonghe, Xindian and Banqiao New Taipei"},
    {"name": "新北其他剩餘區 + 基隆市", "query": "路易莎 in other New Taipei districts and Keelung"},
    {"name": "桃園市", "query": "路易莎 in Taoyuan"},
    {"name": "新竹 + 苗栗", "query": "路易莎 in Hsinchu and Miaoli"},
    {"name": "台中 - 中心區域", "query": "路易莎 in central districts of Taichung"},
    {"name": "台中其他剩餘區", "query": "路易莎 in other Taichung districts"},
    {"name": "彰化 + 南投 + 雲林 + 嘉義", "query": "路易莎 in Changhua, Nantou, Yunlin and Chiayi"},
    {"name": "台南市", "query": "路易莎 in Tainan"},
    {"name": "高雄市", "query": "路易莎 in Kaohsiung"},
    {"name": "宜蘭 + 花蓮 + 台東 + 屏東 + 連江 + 澎湖 + 金門",
     "query": "路易莎 in Yilan, Hualien, Taitung, Pingtung, Lienchiang, Penghu and Kinmen"}

]

# 已處理的 place_id 集合
processed_place_ids = set()

# 初始化 CSV 文件
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            "商業狀態", "格式化地址", "地點ID", "名稱", "地址組成部分", "ADR地址", "Google地圖URL",
            "經緯度", "總用戶評分", "平均評分"
        ])

# 加載已處理的 place_id（如果存在）
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            processed_place_ids.add(row["地點ID"])

# 抓取並解析資料的函數
def fetch_data(query, next_page_token=None):
    params = {
        "query": query,
        "key": API_KEY,
        "language": "zh-TW",  # 繁體中文
        "pagetoken": next_page_token if next_page_token else None
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# 保存資料到 CSV
def save_to_csv(results, loc_name):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        for result in results:
            place_id = result.get("place_id", "N/A")
            # 跳過已處理的資料
            if place_id in processed_place_ids:
                continue
            processed_place_ids.add(place_id)
            row = [
                result.get("business_status", "N/A"),
                result.get("formatted_address", "N/A"),
                place_id,
                result.get("name", "N/A"),
                str(result.get("address_components", "N/A")),
                result.get("adr_address", "N/A"),
                result.get("url", "N/A"),
                str(result.get("geometry", {}).get("location", "N/A")),
                result.get("user_ratings_total", "N/A"),
                result.get("rating", "N/A"),
                # str(result.get("reviews", "N/A"))
            ]
            writer.writerow(row)

# 主邏輯
def main():
    total_store_count = 0  # 用於統計所有區域的門市總數
    store_count_by_location = {}  # 每個地區的門市數量

    for loc in LOCATIONS:
        print(f"Fetching data for {loc['name']}...")
        location_store_count = 0  # 當前地區的門市數量
        next_page_token = None

        while True:
            data = fetch_data(loc["query"], next_page_token)
            if not data or data.get("status") != "OK":
                print(f"Failed to fetch data for {loc['name']}: {data.get('status', 'No Data') if data else 'No Response'}")
                break

            results = data.get("results", [])
            save_to_csv(results, loc["name"])
            location_store_count += len(results)

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

            # 等待 2 秒以確保 token 生效
            time.sleep(2)

        print(f"Data fetched for {loc['name']}: {location_store_count} stores.")
        store_count_by_location[loc["name"]] = location_store_count
        total_store_count += location_store_count

        # 打印統計結果
    print("======================================")
    print("Store count by location:")
    for location, count in store_count_by_location.items():
        print(f"{location}: {count} stores")
    print(f"Total stores fetched: {total_store_count}")

    winsound.Beep(240, 400)  # 播放提示音
    print("資料處理完畢！")


# 執行主程序
main()

print("======================================")
print("ok!!")

end_time = time.time()
print(end_time)
duration = end_time - start_time
print(f"程式執行時間為 {duration:.2f} 秒")
