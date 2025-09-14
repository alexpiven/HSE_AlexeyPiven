class CourtCase:
    def __init__(self, case_number):
        """
        Создаем новое судебное дело
        """
        self.case_number = case_number  # номер дела - обязательный параметр
        self.case_participants = []  # список всех участников дела
        self.listening_datetimes = []  # список дат заседаний
        self.is_finished = False  # закончено ли дело (по умолчанию False)
        self.verdict = ""  # решение суда (по умолчанию пустая строка)

    def set_a_listening_datetime(self, datetime):
        """
        Добавляем дату и время судебного заседания
        """
        self.listening_datetimes.append(datetime)

    def add_participant(self, participant, status="третье лицо"):
        """
        Добавляем участника в дело с указанием статуса
        Статус может быть: "истец", "ответчик", "третье лицо"
        """
        uchastnik = {
            "имя": participant,
            "статус": status
        }
        # Проверяем, нет ли уже такого участника
        est_li = False
        for sushchestvuyushchiy in self.case_participants:
            if sushchestvuyushchiy["имя"] == participant:
                est_li = True
                break

        if not est_li:
            self.case_participants.append(uchastnik)

    def remove_participant(self, participant):
        """
        Убираем участника из дела
        """
        for uchastnik in self.case_participants:
            if uchastnik["имя"] == participant:
                self.case_participants.remove(uchastnik)
                break

    def make_a_decision(self, verdict):
        """
        Выносим решение по делу
        """
        self.verdict = verdict
        self.is_finished = True


# Пример использования для арбитражного суда РФ:
# Создаем дело
delo = CourtCase("А40-123456/2025")

# Добавляем участников с разными статусами
delo.add_participant("ООО \"Ромашка\"", "истец")
delo.add_participant("АО \"Сосна\"", "ответчик")
delo.add_participant("Министерство финансов РФ", "третье лицо")

# Добавляем заседание
delo.set_a_listening_datetime("15.04.2025 10:00")

# Выносим решение
delo.make_a_decision("В удовлетворении исковых требований отказать")

# Проверяем результаты
print("Номер дела:", delo.case_number)
print("Участники:")
for uchastnik in delo.case_participants:
    print("  ", uchastnik["имя"], "-", uchastnik["статус"])
print("Заседания:", delo.listening_datetimes)
print("Решение:", delo.verdict)
print("Дело закончено:", delo.is_finished)