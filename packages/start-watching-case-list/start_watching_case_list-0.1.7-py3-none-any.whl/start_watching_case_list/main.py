import argparse
import datetime
import os

from dotenv import load_dotenv

from start_watching_case_list.funcs.auth import login
from start_watching_case_list.funcs.query import get_new_case


parser = argparse.ArgumentParser(description="ตรวจสอบข้อมูลเคสที่เข้า")
load_dotenv()


def main():
    parser.add_argument("-d", "--date", type=str, help="DATE", default=datetime.datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()
    USERNAME = os.getenv("USER")
    PASSWORD = os.getenv("PASS")

    token = login(USERNAME, PASSWORD)
    get_new_case(token, args.date)


if __name__ == "__main__":
    main()
