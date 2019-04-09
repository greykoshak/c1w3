# Первое задание у нас для разогрева. Ваша задача написать Python-модуль solution.py, внутри
# которого определен класс FileReader.
# Инициализатор этого класса принимает аргумент - путь до файла на диске.
# У класса должен быть метод read, возвращающий содержимое файла в виде строки.
# Еще один момент - внутри метода read вы должны обрабатывать исключение IOError, возникающее,
# когда файла, с которым был инициализирован класс, на самом деле нет на жестком диске.
# В случае возникновения такой ошибки метод read должен возвращать пустую строку "".

class FileReader:
    """Класс FileReader помогает читать из файла"""

    def __init__(self, path_to):
        self.path_to = path_to

    def read(self):
        try:
            with open(self.path_to, "r") as f:
                data = f.read()
        except IOError:
            return ""
        else:
            return data


if __name__ == "__main__":
    reader = FileReader("example.txt")
    print(reader.read())
