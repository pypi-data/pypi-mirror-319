import argparse
import datetime


from start_watching_case_list.funcs.auth import login
from start_watching_case_list.funcs.query import get_new_case


parser = argparse.ArgumentParser(description="ตรวจสอบข้อมูลเคสที่เข้า")


def main():
    parser.add_argument("-u", "--username", type=str, help="USERNAME", required=True)
    parser.add_argument("-p", "--password", type=str, help="PASSWORD", required=True)
    parser.add_argument("-d", "--date", type=str, help="DATE", default=datetime.datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    token = login(args.username, args.password)
    get_new_case(token, args.date)


if __name__ == "__main__":
    main()
