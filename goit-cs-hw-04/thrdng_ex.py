import threading
import os
import glob
import time

# Коренева папка для пошуку файлів
root_folder = r"D:\GoIT\PROJECTS Python\Comp_Systems\goit-cs-hw-04"

# Пошук всіх .txt файлів у кореневій папці та підпапках
files = glob.glob(os.path.join(root_folder, '**', '*.txt'), recursive=True)
keywords = ["тест", "файл", "пошук"]
result_threading = {}
threads = []

print("Знайдені файли:")
for file in files:
    print(file)

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(filename, keywords, result):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword in result:
                        result[keyword].append(filename)
                    else:
                        result[keyword] = [filename]
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
    except Exception as e:
        print(f"Помилка при обробці файлу {filename}: {str(e)}")

# Створення потоків
start_time = time.time()
for file in files:
    thread = threading.Thread(target=search_keywords_in_file, args=(file, keywords, result_threading))
    threads.append(thread)
    thread.start()

# Очікування завершення всіх потоків
for thread in threads:
    thread.join()

end_time = time.time()

print("Результати для threading:")
print(result_threading)
print(f"Час виконання: {end_time - start_time:.2f} секунд")
