import argparse
from tabulate import tabulate

from yml_stat.main import get_yml_statistics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url", nargs="?", type=str, help="Url to YML-file", default="https://nnetwork.ru/yandex-market.xml"
    )
    args = parser.parse_args()

    result = get_yml_statistics(args.url)
    print(tabulate(result, headers="keys", tablefmt="github", showindex=False))


if __name__ == "__main__":
    main()
