import re
import csv
from logger import logger

@logger('main.log')
def get_list_from_file(raw_file_name:str):
    '''returns a list containing each line from csv'''
    with open(raw_file_name, 'r', encoding="utf-8") as f:
        return list(csv.reader(f, delimiter=","))

@logger('main.log')
def correct_full_name(last_name:str, first_name:str, middle_name:str):
    '''recieves raw inputs and returns a list - [last name, first name, middle name]'''
    full_name = (last_name + ' ' + first_name + ' ' + middle_name).split()
    while len(full_name) != 3:
        full_name.append('')
    return full_name

@logger('main.log')
def get_data_to_record(raw_file_name:str):
    '''transforms raw data from csv file to list of lists with uniformed records'''
    contacts_list = get_list_from_file(raw_file_name)
    result_dic = {lastname: ['' for _ in range(7)] for lastname in [line[0].split()[0] for line in contacts_list]} #creates a dict {last_name:[data]} for every record in csv
    for raw_record in contacts_list:
        full_name = correct_full_name(raw_record[0], raw_record[1], raw_record[2])
        fine_record = full_name + [raw_record[3], raw_record[4], uniform_phoes(raw_record[5]), raw_record[6]]
        for i, element in enumerate(fine_record):
            if not result_dic[full_name[0]][i]:
                result_dic[full_name[0]][i] = element
    return [record for record in result_dic.values()]

@logger('main.log')
def uniform_phoes(raw_phone:str):
    '''transformes phone number from csv into "+7(999)999-99-99" or "+7(999)999-99-99 доб.9999" format'''
    phone_pattern = r'(\+7|8)?[\s\(]*(\d{3})[\s\)-]*(\d{3})[\s\)-]*(\d{2})[\s\)-]*(\d{2})\s?\(?(доб)?.?\s?(\d{4})?\)?'
    if 'доб' in raw_phone:
        return re.sub(phone_pattern, r"+7(\2)\3-\4-\5 \6.\7", raw_phone)
    else:
        return re.sub(phone_pattern, r"+7(\2)\3-\4-\5", raw_phone)

@logger('main.log')    
def record_data_to_csv(data:list, fine_file_name):
    '''records a list with data to csv file'''
    with open(fine_file_name, "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(data)

@logger('main.log')
def make_contacts_similar(raw_file_name:str, fine_file_name:str):
    result = get_data_to_record(raw_file_name)
    record_data_to_csv(result, fine_file_name)
    
if __name__ =='__main__':
    make_contacts_similar("phonebook_raw.csv", "phonebook.csv")