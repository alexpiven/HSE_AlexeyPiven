import time
from lesson_2_data import respondents
from lesson_2_data import courts

def gen_court_header(court):
    # header = "Ответчик: " + respondent['short_name'] + '\n' + 'ИНН: ' + respondent['inn']

    header = f"В: {court['court_name']} \n" \

    return header
print('stop')

def gen_respondent_header(respondent):
    # header = "Ответчик: " + respondent['short_name'] + '\n' + 'ИНН: ' + respondent['inn']

    header = f"Ответчик: {respondent['short_name']} \n" \
             f"ИНН  {respondent['inn']} ОГРН {respondent['ogrn']}  \n" \
             f"Адрес: {respondent['address']} \n"
    return header

def main():
    print ('start')
    court_mapping = {i['court_code']: i for i in courts}
    for i in respondents:
        try:
            code = i['case_number'][:3]
            court = court_mapping[code]
            court_header = gen_court_header(court=court)
            print (court_header)
            respondent_header = gen_respondent_header(respondent=i)
            print(respondent_header)
        except Exception:
            print('error')
            continue
    print ('stop')

if __name__== "__main__":
    main()

