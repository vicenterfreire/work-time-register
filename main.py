import logging
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from random import choice
from datetime import datetime, timedelta
from holidays import BR
from tomllib import load
from tomli_w import dump
from time import sleep

# Configuração básica de logging
logging.basicConfig(
    filename='ponto_log.log',  # Arquivo de log
    level=logging.INFO,        # Nível de log (INFO e superior)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem de log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato da data e hora
)

# Espera até um elemento ser clicável
def wait_for_element(driver, by, value, timeout=(60*3)):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

# Realiza o login no sistema
def do_login(driver: webdriver.Chrome, user: str, passwd: str) -> None:
    try:
        logging.info("Iniciando login")
        wait_for_element(driver, By.XPATH, '//input[@id="txtUser"]').send_keys(user)
        wait_for_element(driver, By.XPATH, '//input[@id="txtPass"]').send_keys(passwd)
        wait_for_element(driver, By.XPATH, '//input[@id="btnLogin"]').click()
        logging.info("Login realizado com sucesso")
    except Exception as e:
        logging.error(f"Erro durante o login: {e}")
        raise

# Navega até a página de espelho de ponto
def goto_hours_grid(driver: webdriver.Chrome) -> None:
    try:
        logging.info("Navegando para a página de espelho de ponto")
        wait_for_element(driver, By.XPATH, '//a[@id="ctl18_REC_PtoEspCartaoActionWeb_LinkControl"]').click()
    except Exception as e:
        logging.error(f"Erro ao acessar a página de espelho de ponto: {e}")
        raise

# Abre o modal para inserção de batidas
def open_insert(driver: webdriver.Chrome, handler: str) -> None:
    try:
        logging.info("Abrindo o modal de inserção de batidas")
        wait_for_element(driver, By.XPATH, '//div[@id="ctl26_ctl01_ctl01"]').click()
        wait_for_element(driver, By.XPATH, '//table[@id="ctl26_ctl01_ctl09"]/..').click()

        # Muda para a nova janela
        for handle in driver.window_handles:
            if handle != handler:
                driver.switch_to.window(handle)
                break
        logging.info("Modal de inserção de batidas aberto com sucesso")
    except Exception as e:
        logging.error(f"Erro ao abrir o modal de inserção: {e}")
        raise

# Função que insere as horas de ponto
def insert_hours(driver: webdriver.Chrome, team: str, data_validation: dict, compensacao: bool=True, config_hours:list= ['07:50', '07:55', '08:00']) -> None:
    try:
        def is_valid_day(date: datetime, day: str) -> bool:
            not_valid_days = ('SÁB', 'DOM')
            if datetime.now().time().hour > 17:
                tomorrow = (datetime.now() + timedelta(days=1))
            else:
                tomorrow = datetime.now()
            return (day not in not_valid_days) and (date not in BR()) and (date <= tomorrow)

        def add_hours(hour: str, qtt: float) -> str:
            return (datetime.strptime(hour, "%H:%M") + timedelta(hours=qtt)).strftime("%H:%M")

        def validate_hours(date: str, validation: dict) -> bool:
            return validation[date] != ' '

        def calculate_hours(curr_hour, target: str) -> tuple:
            time_1 = add_hours(curr_hour, 4)
            time_2 = add_hours(time_1, 1)
            time_3 = add_hours(time_2, 4.4 if (target.find(':24') != -1) else 4)
            return (curr_hour, time_1, time_2, time_3)

        logging.info("Iniciando inserção das batidas de ponto")
        justify = wait_for_element(driver, By.XPATH, '//input[@id="GB_txtJustificativa"]')
        justify.send_keys(team)
        print(data_validation)

        rows = driver.find_elements(By.XPATH, '//div[@id="GB_pnGridBatidas"]/table')
        for row in rows:
            curr_hour = choice(config_hours)

            date = row.find_element(By.XPATH, './/span[contains(@id, "lblData")]').text
            day = row.find_element(By.XPATH, './/span[contains(@id, "lblDia")]').text

            if validate_hours(date, data_validation) is False:
                continue

            day_hours = calculate_hours(curr_hour, data_validation[date])

            if is_valid_day(datetime.strptime(date, '%d/%m/%Y'), day):
                row.find_element(By.XPATH, './/input[contains(@id, "txtEnt1")]').send_keys(day_hours[0])
                row.find_element(By.XPATH, './/input[contains(@id, "txtSai1")]').send_keys(day_hours[1])
                row.find_element(By.XPATH, './/input[contains(@id, "txtEnt2")]').send_keys(day_hours[2])
                row.find_element(By.XPATH, './/input[contains(@id, "txtSai2")]').send_keys(day_hours[3])

        logging.info("Inserção das batidas de ponto concluída com sucesso")
        while True:
            sleep(1)
    except Exception as e:
        logging.error(f"Erro ao inserir horas de ponto: {e}")
        raise

# Atualiza a página
def do_update(driver: webdriver.Chrome) -> None:
    try:
        logging.info("Atualizando a página")
        wait_for_element(driver, By.XPATH, '//button[contains(@id, "ctl26_btnAtualizar_tblabel")]').click()
    except Exception as e:
        logging.error(f"Erro ao atualizar a página: {e}")
        raise

def generate_time_range(start_time: str = '07:50', end_time: str = '08:00'):
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')

    time_range = []

    current_time = start
    while current_time <= end:
        time_range.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=1)

    return time_range


def generate_data_for_validation(driver: webdriver.Chrome, data_structure: dict) -> dict:
    rows = driver.find_elements(By.XPATH, ".//tr[contains(@class,'RowGrid')]")
    for row in rows:

        date = row.find_element(By.XPATH, './/td[2]').text
        validation_time = row.find_element(By.XPATH, './/td[17]').text
        data_structure.update({date: re.sub(r'[a-zA-Z]', '', validation_time)})
    return data_structure

def main() -> None:
    if not os.path.exists("settings.toml"):
        with open('settings.toml', 'w') as f:
            dump({'login': '','senha': '','desc': '','minhour': '','maxhour': '', 'url': ''}, f)
        exit()
    else:
        settings = load(open("settings.toml", 'rb'))
    validation_data = {}

    # Utiliza o WebDriver como context manager para garantir que ele será fechado
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(settings.get("url"))
        curr_handle = driver.current_window_handle

        try:
            logging.info("Iniciando processo de registro de ponto")
            do_login(driver, settings.get("login"), settings.get("senha"))
            goto_hours_grid(driver)
            validation_data = generate_data_for_validation(driver, validation_data)
            open_insert(driver, curr_handle)
            insert_hours(driver, settings.get("desc"), validation_data, settings.get("comp",''), generate_time_range(settings.get("minhour"), settings.get("maxhour")))
            do_update(driver)
            logging.info("Processo de registro de ponto concluído com sucesso")
        except Exception as e:
            logging.error(f"Erro durante o processo: {e}")
        finally:
            logging.info("Finalizando execução...")

if __name__ == '__main__':
    main()
