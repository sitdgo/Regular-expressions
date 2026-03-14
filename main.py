import csv
import re

# Читаем адресную книгу в формате CSV
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Наш шаблон для поиска телефонов остался прежним
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\s*\(?(доб\.)?\s*(\d+)?\)?"
)

# Создаем новый список для очищенных данных (совет преподавателя)
cleaned_contacts = []

for row in contacts_list[1:]:
    # 1. Работа с ФИО
    # Разбиваем строку на слова
    full_name = " ".join(row[:3]).split()

    # Добавляем пустые строки, если человек без отчества, чтобы длина всегда была 3
    while len(full_name) < 3:
        full_name.append("")

    # Формируем новую, чистую строку (избегаем "затирания" исходника)
    new_row = full_name + row[3:]

    # 2. Работа с телефонами (используем if-else вместо заплаток)
    phone = new_row[5]
    if phone:
        # Ищем совпадения по шаблону
        match = phone_pattern.search(phone)
        if match:
            # Собираем базовую часть: +7(код)ХХХ-ХХ-ХХ
            base_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"

            # Проверяем, нашлась ли 7-я группа (цифры добавочного номера)
            if match.group(7):
                # Если да, приклеиваем " доб.ХХХХ" СТРОГО без пробела после точки
                new_row[5] = f"{base_phone} доб.{match.group(7)}"
            else:
                # Если нет, оставляем только базу
                new_row[5] = base_phone

    # Добавляем обработанную строку в наш новый список
    cleaned_contacts.append(new_row)

# 3. Объединение дубликатов
contacts_dict = {}
for row in cleaned_contacts:
    key = (row[0], row[1])

    if key not in contacts_dict:
        contacts_dict[key] = row
    else:
        existing_row = contacts_dict[key]
        for i in range(len(existing_row)):
            if not existing_row[i]:
                existing_row[i] = row[i]

# Склеиваем заголовки (нулевую строку) и наши уникальные записи
final_contacts = [contacts_list[0]] + list(contacts_dict.values())

# Сохраняем результат
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts)

print("Данные успешно обработаны и сохранены!")