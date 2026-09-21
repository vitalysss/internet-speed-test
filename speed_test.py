import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REQUESTS_COUNT = 10
CHUNK_SIZE = 64 * 1024


def download(url: str, timeout: int) -> tuple[float, int]:
    request = Request(url, headers={"User-Agent": "internet-speed-test/1.0"})
    downloaded = 0
    started_at = time.perf_counter()

    with urlopen(request, timeout=timeout) as response:
        while chunk := response.read(CHUNK_SIZE):
            downloaded += len(chunk)

    elapsed = time.perf_counter() - started_at
    return elapsed, downloaded


def measure(url: str, timeout: int) -> None:
    times = []
    total_bytes = 0

    for number in range(1, REQUESTS_COUNT + 1):
        elapsed, downloaded = download(url, timeout)
        times.append(elapsed)
        total_bytes += downloaded
        print(f"Запрос {number}/{REQUESTS_COUNT}: {elapsed:.2f} сек., {downloaded} байт")

    total_time = sum(times)
    average_time = total_time / REQUESTS_COUNT
    speed_mbps = total_bytes * 8 / total_time / 1_000_000

    print("\nРезультат:")
    print(f"Среднее время запроса: {average_time:.2f} сек.")
    print(f"Скачано данных: {total_bytes / 1024 / 1024:.2f} МБ")
    print(f"Средняя скорость: {speed_mbps:.2f} Мбит/с")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Последовательно скачивает файл 10 раз и считает среднюю скорость."
    )
    parser.add_argument("url", help="Прямой URL большого файла или изображения")
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Тайм-аут одного запроса в секундах (по умолчанию 30)",
    )
    args = parser.parse_args()

    try:
        measure(args.url, args.timeout)
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        parser.exit(1, f"Ошибка при скачивании: {error}\n")


if __name__ == "__main__":
    main()
