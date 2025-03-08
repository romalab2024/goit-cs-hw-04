import multiprocessing
import os
import glob
import time
from collections import defaultdict

# Функція для пошуку ключових слів у файлі (для процесів)
def search_keywords_in_file_multiprocessing(args):
    filename, keywords, queue = args  # Додаємо queue як аргумент
    result = defaultdict(list)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result[keyword].append(filename)
        # Додаємо результат у чергу
        queue.put(result)  # Зберігаємо результат у черзі
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
    except Exception as e:
        print(f"Помилка при обробці файлу {filename}: {str(e)}")

# Головна частина коду
if __name__ == "__main__":
    root_folder = r"D:\GoIT\PROJECTS Python\Comp_Systems\goit-cs-hw-04"
    files = glob.glob(os.path.join(root_folder, '**', '*.txt'), recursive=True)
    keywords = ["тест", "файл", "пошук"]

    print("Знайдені файли:")
    for file in files:
        print(file)

    start_time = time.time()

    result_multiprocessing = defaultdict(list)
    queue = multiprocessing.Queue()  # Створюємо чергу

    # Адаптивний вибір підходу залежно від кількості файлів
    if len(files) > 10:
        # Використовуємо Pool для великої кількості файлів
        with multiprocessing.Pool() as pool:
            results = pool.map(search_keywords_in_file_multiprocessing, [(file, keywords, queue) for file in files])
    else:
        # Використовуємо простий multiprocessing для невеликої кількості файлів
        processes = []

        # Створення процесів з передачею queue
        for file in files:
            process = multiprocessing.Process(target=search_keywords_in_file_multiprocessing, args=((file, keywords, queue),))
            processes.append(process)
            process.start()

        # Очікування завершення всіх процесів
        for process in processes:
            process.join()

        # Збирання результатів з черги
        results = []
        while not queue.empty():
            results.append(queue.get())

    # Об'єднання результатів
    for partial_result in results:
        for keyword, files_list in partial_result.items():
            result_multiprocessing[keyword].extend(files_list)

    end_time = time.time()

    # Форматований вивід результатів
    print("\nРезультати для адаптивного multiprocessing:")
    if result_multiprocessing:
        for keyword, files_list in result_multiprocessing.items():
            print(f"Ключове слово: '{keyword}'")
            for file in files_list:
                print(f"   - {file}")
    else:
        print("Жодних збігів не знайдено.")

    print(f"\nЧас виконання: {end_time - start_time:.2f} секунд")
