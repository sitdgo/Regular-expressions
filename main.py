import csv
import re

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# 1. Поместить Фамилию, Имя и Отчество человека в правильные поля
for row in contacts_list[1:]:
    full_name = " ".join(row[:3]).split()

    row[0] = full_name[0] if len(full_name) > 0 else ""
    row[1] = full_name[1] if len(full_name) > 1 else ""
    row[2] = full_name[2] if len(full_name) > 2 else ""

# 2. Привести все телефоны в нужный формат
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\s*\(?(доб\.)?\s*(\d+)?\)?"
)

for row in contacts_list[1:]:
    phone = row[5]
    if phone:
        # Подставляем найденные группы
        formatted_phone = phone_pattern.sub(r"+7(\2)\3-\4-\5 доб.\7", phone)
        # Убираем " доб.", только если он оказался в самом конце (то есть добавочных цифр не было)
        if formatted_phone.endswith(" доб."):
            formatted_phone = formatted_phone.replace(" доб.", "")

        row[5] = formatted_phone

# 3. Объединить все дублирующиеся записи о человеке в одну
contacts_dict = {}
for row in contacts_list[1:]:
    key = (row[0], row[1])

    if key not in contacts_dict:
        contacts_dict[key] = row
    else:
        existing_row = contacts_dict[key]
        for i in range(len(existing_row)):
            if not existing_row[i]:
                existing_row[i] = row[i]

final_contacts = [contacts_list[0]] + list(contacts_dict.values())

# Сохраняем получившиеся данные
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts)