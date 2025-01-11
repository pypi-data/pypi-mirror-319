import argparse

from funcs.auth import login

parser = argparse.ArgumentParser(description="Get data from case services")


def main():
    parser.add_argument("-t", "--task", type=str, help="[login]")
    args = parser.parse_args()
    if args.task == "login":
        login()
    else:
        print("Please enter valid task")


if __name__ == "__main__":
    main()
