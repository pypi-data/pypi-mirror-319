__version__ = '0.0.2'


def getConfig(config_list:list, section:str="DEFAULT", config_path:str='config.txt')->list: return get_config(config_list,section,config_path)
def get_config(config_list:list, section:str="DEFAULT", config_path:str='config.txt')->list:
    """ 환경변수 읽기

    Args:
        config_list: config 파일에서 읽을 항목 나열  
        section: config 파일에서 읽을 구간  
        config_path: config 파일 경로  

    Returns:
        @config_list에 대응하는 환경변수 값의 목록  

    Example:
        # --------------------------
        get_config(['item1','item2'])  
        # --------------------------
        ['igzg utils', 'get config']  
        # --------------------------
    """
    import configparser
    config = configparser.ConfigParser()

    def handle_error(e:Exception):
        print('config.txt파일 오류')
        write_error(e)
        return False

    for enc in ['utf-8','cp949']:
        try:
            config.read(config_path,encoding=enc)
            res_list = [config[section][x] for x in config_list]
            return res_list
        except UnicodeDecodeError as e:
            dec_error = e
            continue
        except Exception as e: 
            return handle_error(e)
    else:
        return handle_error(dec_error)

def getNowStr(format:str = "%Y-%m-%d %H:%M:%S")->str: return get_now_str(format)
def get_now_str(format:str = "%Y-%m-%d %H:%M:%S")->str:
    """ 현재시간 문자열 반환

    Args:
        format: 시간 문자열 형식

    Returns:
        @format에 대응하는 현재시간 문자열

    Example:
        # --------------------------
        get_now_str()  
        # --------------------------
        '2024-08-11 14:16:08'  
        # --------------------------
    """    
    from datetime import datetime
    now_str = datetime.now().strftime(format.encode('unicode-escape').decode()).encode().decode('unicode-escape')

    return now_str

def writeError(e:Exception, error_path:str='error.txt', console_logging:bool=False)->str: return write_error(e,error_path,console_logging)
def write_error(e:Exception, error_path:str='error.txt', console_logging:bool=False)->str:
    """ 오류 기록

    Args:
        e: 기록할 예외
        error_path: error log 경로
        console_logging: 콘솔에 오류 내용 출력 여부

    Returns:
        @e에 대응하는 오류 정보 str

    Example:
        # --------------------------  
        try:  
            a = {1:12}[2]  
        except Exception as e:  
            print(write_error(e))  
        # --------------------------  
        2024-08-11 14:22:56  
            [KeyError] - Mapping key not found.  
            function: <module>((2,))  
            traceback: Traceback (most recent call last):  
        File "D:.Github.igzg.igzg.utils.py", line 117, in <module>  
            a = {1:12}[2]  
        KeyError: 2  
        # --------------------------  
    """    
    import traceback
    error_log = f"""{getNowStr()}
    [{type(e).__name__}] - {e.__doc__}
    function: {e.__traceback__.tb_frame.f_code.co_name}({e.args})
    traceback: {traceback.format_exc()}
    """
    fwrite(error_log, error_path)
    if console_logging:
        print(error_log)
    return error_log

def fwrite(text, file_path:str="output.txt", encoding:str=None):
    """ 파일에 쓰기

    Args:
        text: 파일에 저장할 str
        file_path: 저장할 파일 경로
        encoding: 파일 인코딩

    Returns:
        None

    Example:
        # --------------------------
        fwrite("test")
        # --------------------------

        # --------------------------
    """      
    def handle_error(e:Exception):
        if e: write_error(e)
        return False

    text = str(text)
    text_str = text + '\n' if (not text) or (text[-1] != '\n') else text
    enc_list = [encoding] if encoding else ['utf-8','cp949']

    enc_error = None
    for enc in enc_list:
        try:
            with open(file_path, 'a', encoding=enc) as f:
                f.write(text_str)
            break
        except UnicodeEncodeError as e: 
            enc_error = e
            continue
        except Exception as e: 
            handle_error(e)
            break
    else:
        handle_error(enc_error)


if __name__ == "__main__":
    print(get_now_str())