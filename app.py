from flask import Flask, request, jsonify
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

# Função para baixar a imagem
def baixar_imagem(url, caminho):
    response = requests.get(url)
    with open(caminho, "wb") as file:
        file.write(response.content)

# Função para publicar no Instagram
def publicar_no_instagram(titulo, legenda, imagem_path):
    # Configuração do navegador em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.instagram.com")

    # Login
    time.sleep(5)
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    username.send_keys("SEU_USUARIO")  # Substitua pelo seu usuário do Instagram
    password.send_keys("SUA_SENHA")    # Substitua pela sua senha do Instagram
    password.send_keys(Keys.RETURN)

    # Aguardar login
    time.sleep(5)

    # Acessar a página de criação de postagem
    driver.get("https://www.instagram.com/create/")

    # Upload de imagem
    time.sleep(5)
    upload_button = driver.find_element_by_xpath("//input[@type='file']")
    upload_button.send_keys(imagem_path)

    # Adicionar legenda
    time.sleep(5)
    caption = driver.find_element_by_xpath("//textarea[@aria-label='Escreva uma legenda...']")
    caption.send_keys(f"{legenda} #wordpress #automacao")

    # Publicar
    time.sleep(5)
    post_button = driver.find_element_by_xpath("//button[text()='Compartilhar']")
    post_button.click()

    # Fechar navegador
    time.sleep(10)
    driver.quit()

@app.route("/publicar", methods=["POST"])
def publicar():
    data = request.json
    titulo = data.get("titulo")
    legenda = data.get("legenda")
    imagem_url = data.get("imagemUrl")

    if not titulo or not legenda or not imagem_url:
        return jsonify({"status": "erro", "mensagem": "Dados incompletos"}), 400

    try:
        # Baixar a imagem
        imagem_path = "/tmp/imagem.png"
        baixar_imagem(imagem_url, imagem_path)

        # Publicar no Instagram
        publicar_no_instagram(titulo, legenda, imagem_path)

        return jsonify({"status": "sucesso", "mensagem": "Postagem publicada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
