from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Configuração do navegador em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Usar o ChromeDriver gerenciado pelo webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Função para realizar a automação no Instagram
def automatizar_instagram(username, password):
    try:
        # Abrir a página de login do Instagram
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)  # Aguardar a página carregar

        # Preencher o campo de usuário
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)

        # Preencher o campo de senha
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        # Clicar no botão de login
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(5)  # Aguardar o login ser processado

        # Verificar se o login foi bem-sucedido
        if "accounts/onetap" in driver.current_url:
            return "Login realizado com sucesso!"
        else:
            return "Falha ao fazer login. Verifique suas credenciais."

    except Exception as e:
        return f"Erro durante a automação: {str(e)}"

# Rota principal do Flask
@app.route('/')
def home():
    return "Bem-vindo à automação do Instagram!"

# Rota para executar a automação
@app.route('/automatizar', methods=['GET'])
def automatizar():
    # Obter as credenciais do Instagram (substitua por variáveis de ambiente ou secrets)
    INSTAGRAM_USERNAME = "seu_usuario"
    INSTAGRAM_PASSWORD = "sua_senha"

    # Executar a automação
    resultado = automatizar_instagram(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    return jsonify({"resultado": resultado})

# Executar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
