import datetime
from string import Template
import requests

PATH_QUERY = "http://192.168.5.195:7004/api/forensics?start_date=$start_date&end_date=$end_date&field_sort=created_at&limit=1000&status&status_integrity"
BASIC_TOKEN = "Y2NpYjpjY2li"


def get_new_case(token, target_date):
    target_date = datetime.datetime.now().strftime("%Y-%m-%d") if target_date is None else datetime.datetime.strptime(target_date, "%Y-%m-%d")
    headers = {"Authorization": f"Basic {BASIC_TOKEN}", "Cookie": f"token={token}", "Content-Type": "application/json"}
    url = Template(PATH_QUERY)
    url = url.substitute(start_date=target_date, end_date=target_date)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        data_field = json_data.get("data", {}).get("data", [])
        if data_field is not None:
            print(f"ข้อมูลเคสประจำวันที่: {target_date}")
            for case in data_field:
                print(f"- เคส: {case.get('case_id')}, จำนวนพยานหลักฐาน: {len(case.get("evidences"))}")
        else:
            print("ไม่พบข้อมูลเคสในวันที่ที่ระบุ")
    else:
        print(f"Failed to access protected route: {response.status_code}")
