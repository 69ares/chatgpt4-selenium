from flask import Flask, request, jsonify
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

@app.route('/ricevi_domanda', methods=['POST'])
def ricevi_domanda():
    data = request.get_json()
    domanda = data['domanda']
    print(domanda)

    # Inietta la domanda nel browser
    send_text_to_browser(domanda)
    
    return jsonify({"message": "Domanda ricevuta con successo!"})

def send_text_to_browser(text):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9998")
    driver = webdriver.Chrome(options=options)
    
    # Usa il codice JavaScript solo per inserire il testo
    script = f"""
    function setValueWithXPath(xpath, value) {{
        let element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {{
            element.value = value;
            element.dispatchEvent(new Event('input', {{ 'bubbles': true }})); // Per triggerare eventi di input
        }} else {{
            console.error("Elemento per la scrittura non trovato!");
        }}
    }}

    setValueWithXPath("/html/body/div[1]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/textarea", "{text}");
    """
    
    driver.execute_script(script)
    
    # Trova l'elemento e simula la pressione del tasto "Invio"
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/textarea")
    element.send_keys(Keys.ENTER)

    # Aspetta 5 secondi
    time.sleep(10)

    # Esegui il codice JavaScript per estrarre il testo e ottieni il valore di ritorno
    script_extraction = """
    function findLastElementWithClasses(element, classes) {
        let matches = true;
        classes.forEach(cls => {
            if (!element.classList.contains(cls)) {
                matches = false;
            }
        });
        return matches ? element : null;
    }

    function extractTextFromDivs() {
        const divClasses = ["group", "w-full", "text-token-text-primary", "border-b", "border-black/10", "dark:border-gray-900/50", "bg-gray-50", "dark:bg-[#444654]"];
        const textDivClasses = ["markdown", "prose", "w-full", "break-words", "dark:prose-invert", "light"];
        const divs = document.querySelectorAll('div');
        let lastDiv = null;
        divs.forEach(div => {
            if (findLastElementWithClasses(div, divClasses)) {
                lastDiv = div;
            }
        });
        if (lastDiv) {
            const textDivs = lastDiv.querySelectorAll('div');
            let textDivFound = null;
            textDivs.forEach(textDiv => {
                if (findLastElementWithClasses(textDiv, textDivClasses)) {
                    textDivFound = textDiv;
                }
            });
            if (textDivFound) {
                return textDivFound.innerText;
            } else {
                return null;
            }
        } else {
            return null;
        }
    }

    return extractTextFromDivs();
    """

    risposta = driver.execute_script(script_extraction)
    print(risposta)
    return risposta
        
if __name__ == '__main__':
    app.run(port=5001)
