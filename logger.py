import os
import datetime

def logger(path=None):    
    def __logger(old_function):
        
        def new_function(*args, **kwargs):
            log_path = ['main.log', path][bool(path)] #if path = None, logs will be put in main.log
            launch_date = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            
            if not os.path.exists(log_path): open(log_path, 'x').close()
                
            with open(log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f'launch date:{launch_date}; function name:{old_function.__name__}; arguments:{args}; keyword arguments:{kwargs}; returned value:{result} \n')
                        
            return result
        
        return new_function
    
    return __logger

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        div(4, 2)
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()