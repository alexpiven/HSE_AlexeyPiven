class LegalContract:
    def __init__(self, contract_number, contract_type):
        """
        Создаем новый договор
        """
        self.contract_number = contract_number  # номер договора
        self.contract_type = contract_type  # тип договора (купля-продажа, аренды и т.д.)
        self.parties = []  # стороны договора
        self.terms = []  # условия договора
        self.signing_date = ""  # дата подписания
        self.expiration_date = ""  # дата окончания
        self.is_signed = False  # подписан ли договор
        self.is_active = False  # действующий ли договор
        self.obligations = []  # обязательства сторон

    def add_party(self, party_name, party_role):
        """
        Добавляем сторону договора
        """
        party = {
            "имя": party_name,
            "роль": party_role  # например: "арендодатель", "арендатор", "продавец", "покупатель"
        }
        self.parties.append(party)

    def add_term(self, term_description):
        """
        Добавляем условие договора
        """
        self.terms.append(term_description)

    def set_dates(self, signing_date, expiration_date):
        """
        Устанавливаем даты договора
        """
        self.signing_date = signing_date
        self.expiration_date = expiration_date

    def sign_contract(self):
        """
        Подписываем договор
        """
        self.is_signed = True
        self.is_active = True
        print(f"Договор {self.contract_number} подписан")

    def add_obligation(self, party, obligation):
        """
        Добавляем обязательство для стороны договора
        """
        obligation_item = {
            "сторона": party,
            "обязательство": obligation
        }
        self.obligations.append(obligation_item)

    def terminate_contract(self):
        """
        Расторгаем договор
        """
        self.is_active = False
        print(f"Договор {self.contract_number} расторгнут")

    def get_contract_info(self):
        """
        Получаем информацию о договоре
        """
        info = f"Договор №{self.contract_number}\n"
        info += f"Тип: {self.contract_type}\n"
        info += f"Дата подписания: {self.signing_date}\n"
        info += f"Дата окончания: {self.expiration_date}\n"
        info += f"Статус: {'Действующий' if self.is_active else 'Не действующий'}\n"
        info += "Стороны:\n"
        for party in self.parties:
            info += f"  - {party['имя']} ({party['роль']})\n"
        return info

    def check_deadline(self, current_date):
        """
        Проверяем, не истек ли срок действия договора
        """
        if current_date > self.expiration_date and self.is_active:
            self.is_active = False
            print(f"Срок действия договора {self.contract_number} истек")
            return True
        return False


# Пример использования:
# Создаем договор аренды
dogovor = LegalContract("АР-2025-001", "Аренда помещения")

# Добавляем стороны
dogovor.add_party("ООО \"Ромашка\"", "Арендодатель")
dogovor.add_party("ИП Иванов И.И.", "Арендатор")

# Устанавливаем даты
dogovor.set_dates("01.04.2025", "31.03.2026")

# Добавляем условия
dogovor.add_term("Срок аренды: 12 месяцев")
dogovor.add_term("Ежемесячная арендная плата: 50 000 руб.")
dogovor.add_term("Предмет договора: офисное помещение по адресу...")

# Добавляем обязательства
dogovor.add_obligation("ООО \"Ромашка\"", "Предоставить помещение в надлежащем состоянии")
dogovor.add_obligation("ИП Иванов И.И.", "Оплачивать аренду ежемесячно до 10 числа")

# Подписываем договор
dogovor.sign_contract()

# Получаем информацию о договоре
print(dogovor.get_contract_info())

# Проверяем срок действия
dogovor.check_deadline("01.04.2026")