import os
import logging
import functools

class FileNotFound(Exception):
    pass

class FileCorrupted(Exception):
    pass

def get_logger(mode):
    logger = logging.getLogger("file_logger")

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    if mode == "console":
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler("file_operations.log", encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def logged(exception_types, mode="console"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(mode)

            try:
                result = func(*args, **kwargs)
                logger.info(f"Операція {func.__name__} виконана успішно.")
                return result
            except exception_types as e:
                logger.error(f"Помилка у {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


class FileHandler:
    @logged((FileNotFound, FileCorrupted), mode="console") 
    def __init__(self, path):
        self.path = os.path.abspath(path)

        if not os.path.exists(self.path):
            raise FileNotFound("Файл не знайдено.")

        if not self.path.endswith(".txt"):
            raise FileCorrupted("Потрібен файл з розширенням .txt")

    @logged(FileCorrupted, mode="file")
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            raise FileCorrupted("Неможливо прочитати файл")

    @logged(FileCorrupted, mode="file")
    def write(self, text):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            raise FileCorrupted("Неможливо записати у файл")

    @logged(FileCorrupted, mode="file")
    def append(self, text):
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            raise FileCorrupted("Неможливо дописати у файл")



if __name__ == "__main__":
    file_path = "labor_6.txt"

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Текстовий файл створено.\n")

    try:
        fh = FileHandler(file_path)
    except Exception as e:
        print("Помилка при створенні:", e)
        exit()

    try:
        content = fh.read()
        print("\nВміст файлу:")
        print(content if content else "(Файл порожній)")

        print("\nСтатистика літер:")
        ukr_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        lower_content = content.lower()

        for letter in ukr_alphabet:
            count = lower_content.count(letter)
            if count > 0:
                print(f"{letter} - {count}")
            else:
                print(f"{letter} - нема")

        new_text = "Перезаписаний текст."
        fh.write(new_text + "\n")
        print("Файл перезаписано.")

        add_text = "Текст додано."
        fh.append(add_text + "\n")
        print("Текст дописано.")
    except Exception as e:
        print("Помилка виконання:", e)