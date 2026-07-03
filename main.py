import csv
import pprint
from typing import Callable
import time

path = 'contacts.csv'

'''
phone_dict_columns - это заготовка для того, чтобы полноценно проверять корректность файла CSV(Столбцы, размер)
доработка не планируется
Используется один раз для форматированного вывода
'''
phone_dict_columns = ["ID",'Name','Surname','Email','Tel','Comment']

### Блок основной функции, которая является точкой входя для пользователя
def main_function():
    """
    Точка входя для пользователя. Обеспечивает вызов ужных методов
    :return: None
    """
    global path
    while True:
        print(
        f'''
        
    Справочник электронной почты, используется файл {path}
    
      ########################
     ######## МЕНЮ ##########
    ########################
    1. Вывод на экран всех контактов
    2. Добавить новый контакт
    3. Поиск контакта
    4. Изменить контакт
    5. Удалить контакт
    6. Выход из программы
    7. Изменение пути к справочнику
'''
        )
        try:
            n=int(input('Для продолжение введите номер меню требуемой операции: '))
        except:
             n = -1
        if int(0<n<6):
            print(f'Обрабатываем пункт {n}')
            run_action(n)
        elif n==6:
            print('Выход из программы')
            break
        elif n==7:
            path=input(f'''
            Введите новый путь к справочнику: 
''')
        else: print('Введите корректный номер меню.')
def run_action(n: int)-> None:
    """
    Запуск действия в заисимости отвыбора пользователя
    args n integer, переменная которая передаётся при вызове из основного метода
    """
    match n:
        case 1:
            print('Список контактов:\n')
            show_contacts()
        case 2:
            print("Добавление контакта")
            add_new_contact(path, ask_new_contact)
        case 3:
            print("Поиск контакта")
            search_user(search_contact_menu,path)
        case 4:
            print("Изменить контакт")
            ask_contact_to_modify(path)
        case 5:
            print('Удаление контакта')
            delete_contact(path)

# Блок показа всех контактов
def show_contacts():
    """
    Показ списка пользлвателей в форматированном виде
    :return: Null
    """
    with open(path, encoding="utf-8") as f:
        data = csv.reader(f)
        format_str = '  '.join(['{:<15}'] * len(phone_dict_columns))
        for row in data:
            print(format_str.format(*row))
#    print(data)
    input('Нажмите ENTER для продолжения: ')

### Блок добавления нового контакта
def ask_new_contact()->dict|None:
    """
    Метод для запроса данных о новом контакте
    :return: Данные контакта или ничего в случае, если пользователь передумал
    """
    while True:
        name = ''
        tel = ''
        while not name:
            name=input('Введите имя: ')
        surname = input('Введите фамилию: ')
        email = input('Введите почтовый адрес: ')
        while not tel:
            tel = input('Введите номер телефона: ')
        comment = input('Введите комментарий: ')
        print(f'''
        Имя: {name}
        Фамилия: {surname}
        почта: {email}
        телефон: {tel}
        комментарий: {comment}
            '''
        )
        answer=input('''Если данные верны, Введите 'Y'
        Если данные не верны и требуется ввести их заново Введите 'N'
        Для Выхода нажмите 'Enter'
        ''')
        if answer.upper()=='Y':
            new_contact =  {'ID': int(time.time()), 'Name': name,'Surname': surname, "Email": email,'Tel': tel,"Comment": comment}
            #time оборачиваем в int, чтобы ID был короче
            time.sleep(1) # Пауза для того, чтобы точно всегда был уникальный ID, Иначе надо убирать int от time.time()
            print(new_contact)
            return new_contact
        elif answer.upper()=='N':
            pass
        else: break
def add_new_contact(file_path: str, func: Callable)->None:
    """
    Функция записи нового контакта в файл
    :param file_path: Путь к файлу с контактами
    :param func: функция, которая возвращает словарь с данными контакта
    :return: Ничего
    """
    rows = func()
#    rows.insert(0,int(time.time()))
    if type(rows)==dict:
        with open(file_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows.keys())
            writer.writerow(rows)

### Блок Поиска контактов
def search_contact_menu()->int|None:
    """
        Функция для показа меню поиска контакта
        :return:  ID найденного контакта или ничего, если контакт не найден
    """
    print(
        f'''Введите тип поиска:
        1. Поиск по имени
        2. Поиск по номеру телефона
        3. Поиск по почте
        4. Поиск по всем полям
        5. Выход в предыдущее меню
''')
    while True:
        try:
            n = int(input('Для продолжение введите номер меню требуемой операции: '))
        except:
            n = -1
        if int(0 < n < 5):
            print(f'Обрабатываем пункт {n}')
            return n
        elif n == 5:
            break
        else:
            print('Введено неверное значение')
def search_user(func: Callable, file_path: str=path)->None:
    """
    Функция для осуществления поиска пользователя и отображения найденной записи
    :param func: функция, которая возвращает параметр для ветвления(поиск по имени, номеру телоефона ....)
    :param file_path: путь к файлу справочнику
    :return: Ничего
    """
    n = func()
    if not n:
        return
    search_pattern=None
    match n:
        case 1:
            print('Поиск по имени:\n')
            search_pattern = 'Name'
        case 2:
            print('Поиск по номеру телефона:\n')
            search_pattern = 'Tel'
        case 3:
            print('Поиск по почте:\n')
            search_pattern = 'Email'
        case 4:
            print('Поиск по всем полям:\n')
    text = input('Введите значние поиска: ')
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        count=0
        for row in reader:
            if n != 4:
                if str(row[search_pattern])==text:
                    pprint.pprint(row, indent=4)
                    count+=1
            elif n ==4:
#                print(str(row))
                if text in row.values():
                    pprint.pprint(row, indent=4)
                    count += 1
        if not count:
            print(f'Данные не найдены')
        input('Для продолжения нажмите Enter')

### Блок удаления записи
def delete_contact(file_path: str, id_to_delete: str='')->None:
    """
    Функция для удаления контакта по ID контакта
    :param file_path: путь к файлу справочнику
    :param id_to_delete: ID, который необходимо удалить
    :return: ничего
    """
    is_modify = True
    if id_to_delete=='':
        id_to_delete = input('Введите ID для удаления: ')
        is_modify = False
    with open(path, encoding="utf-8") as f:
        fields = f.readline().rstrip('\n').split(',')
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
#        print(type(reader))
        temp_dict=[]
        if not check_csv_emptiness(file_path):
            return None
        for row in reader:
            if str(row['ID']) != str(id_to_delete):
                temp_dict.append(row)
    with open('contacts.csv', "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for _ in range(len(temp_dict)):
            writer.writerow(temp_dict[_])
    if not is_modify:
        input('Нажмите Enter для продолжения')
    return None

#Блок изменения контакта
def ask_contact_to_modify(file_path: str)->None:
    """
    Функция для изменения контакта и формирования словаря с изменённым контактом
    :param file_path: путь к файлу справочнику
    :return: новая запись или ничего
    """
    id_to_delete = input('Введите ID контакта для изменения: ')
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        temp_dict={}
        if not check_csv_emptiness(file_path):
            return None
        # count = 0
        # for _ in f:
        #     count += 1
        # if count < 2:
        #     input(f'''В справочнике нет записей. Нажмите Enter для продолжения''')
        #     return None
        for row in reader:
            if str(row['ID']) == str(id_to_delete):
                temp_dict = row
        if not temp_dict:
            input('''
                ###ID не найдено###
            Для продолжения нажмите Enter
            ''')
            return None
    if input(f'''
    ################################################################
    Нажмите Y, если требуется изменить данный контакт:\n {temp_dict}
    ################################################################
''').upper() != 'Y':
        return None
    while True:
        temp_var = ''
        temp_var=input(f'''Старое имя: {temp_dict['Name']}. Введите новое имя или нажмите Enter для того, чтобы оставить старое.\n''')
        if temp_var != '':
            temp_dict['Name'] = temp_var
        temp_var=input(f'''Старая фамилия: {temp_dict['Surname']}'. Введите новую фамилию или нажмите Enter для того, чтобы оставить старую.\n''')
        if temp_var != '':
            temp_dict['Surname'] = temp_var
        temp_var=input(f'''Старый Email: {temp_dict['Email']}'. Введите новый Email или нажмите Enter для того, чтобы оставить старый.\n''')
        if temp_var != '':
            temp_dict['Email'] = temp_var
        temp_var=input(f'''Старый Tel: {temp_dict['Tel']}'. Введите новый телефон или нажмите Enter для того, чтобы оставить старый.\n''')
        if temp_var != '':
            temp_dict['Tel'] = temp_var
        temp_var=input(f'''Старый Comment: {temp_dict['Comment']}'. Введите новый комментарий или нажмите Enter для того, чтобы оставить старый.\n''')
        if temp_var != '':
            temp_dict['Comment'] = temp_var
        print(f'''
        ID: {temp_dict['ID']},
        Имя: {temp_dict['Name']}
        Фамилия: {temp_dict['Surname']}
        почта: {temp_dict['Email']}
        телефон: {temp_dict['Tel']}
        комментарий: {temp_dict['Comment']}
            '''
        )
        answer=input('''
        #############################################################
        Если данные верны, Введите 'Y'
        Если данные не верны и требуется ввести их заново Введите 'N'
        Для Выхода нажмите 'Enter'
        #############################################################
        ''').upper()
        if answer.upper()=='Y':
            print(temp_dict)
            delete_contact(file_path, id_to_delete)
            with open(file_path, "a", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=temp_dict.keys())
                writer.writerow(temp_dict)
            return None
#            return temp_dict
        elif answer.upper()=='N':
            pass
        else: break

#Функция для проверки на то, что справочник не пуст
def check_csv_emptiness(file_path: str)->int|None:
    """
    Функция проверяет, что справочник содержит контакты
    :param file_path: путь к файлу спрвочнику
    :return: int если справчоник НЕ пуст или Null, если справчник пуст
    """
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        count = 0
        for _ in f:
            count += 1
        if count < 2:
            input(f'''
            ###В справочнике нет записей. Нажмите Enter для продолжения###
''')
            return None
        else:
            return count
if __name__ == '__main__':
    main_function()