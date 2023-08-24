#"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9998 --user-data-dir=openai

import json
import subprocess
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import threading

##################################################################CHAT GPT
app = Flask(__name__)

@app.route('/ricevi_domanda', methods=['POST'])
def ricevi_domanda():
    data = request.get_json()
    domanda = data['domanda']
    print(domanda)
    
    # Inietta la domanda nel browser e ottieni la risposta
    risposta = send_text_to_browser(domanda)
    return jsonify({"message": f"Domanda ricevuta e risposta ottenuta: {risposta}"})


def send_text_to_browser(text):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9998")
    driver = webdriver.Chrome(options=options)
    
    # Codice JavaScript per iniettare la domanda nel browser
    script_injection = f'''
    function setValueWithXPath(xpath, value) {{
        let element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) {{
            element.value = value;
            element.dispatchEvent(new Event('input', {{ 'bubbles': true }}));
        }} else {{
            console.error("Elemento per la scrittura non trovato!");
        }}
    }}
    setValueWithXPath("/html/body/div[1]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/textarea", "{text}");
    '''
    driver.execute_script(script_injection)
    
    # Simula la pressione del tasto "Enter"
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/textarea")
    element.send_keys(Keys.ENTER)

    # Aspetta 10 secondi
    time.sleep(10)

    # Codice JavaScript per estrarre la risposta dal browser
    script_extraction = '''
    function findLastElementWithClasses(element, classes) {{
        let matches = true;
        classes.forEach(cls => {{
            if (!element.classList.contains(cls)) {{
                matches = false;
            }}
        }});
        return matches ? element : null;
    }}

    function extractTextFromDivs() {{
        const divClasses = ["group", "w-full", "text-token-text-primary", "border-b", "border-black/10", "dark:border-gray-900/50", "bg-gray-50", "dark:bg-[#444654]"];
        const textDivClasses = ["markdown", "prose", "w-full", "break-words", "dark:prose-invert", "light"];
        const divs = document.querySelectorAll('div');
        let lastDiv = null;
        divs.forEach(div => {{
            if (findLastElementWithClasses(div, divClasses)) {{
                lastDiv = div;
            }}
        }});
        if (lastDiv) {{
            const textDivs = lastDiv.querySelectorAll('div');
            let textDivFound = null;
            textDivs.forEach(textDiv => {{
                if (findLastElementWithClasses(textDiv, textDivClasses)) {{
                    textDivFound = textDiv;
                }}
            }});
            if (textDivFound) {{
                return textDivFound.innerText;
            }} else {{
                return null;
            }}
        }} else {{
            return null;
        }}
    }}
    return extractTextFromDivs();
    '''
    risposta = driver.execute_script(script_extraction)
    return risposta
def run_flask_app():
    app.run(port=5001)
    
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()
CHATGPT##################################################################################



INVIA DOMANDA A CHATGPT###################################################################################################

            user_comment = "Ciao, fino a che ora siete aperti?"
            premessa = ("Risposte in italiano, brevi e dirette.Massimo 150 caratteri."
                        "Risposte non troncate e con senso."
                        "Se una domanda è generica, risposta vaga."
                        "Rispondi come proprietario account e-commerce."
                        "Se complimenti: ringrazia."
                        "Se offese: chiedi motivazioni."
                        "Se domande sui corsi: frase di circostanza per prendere tempo. "
                        "questa è la domanda: ")
            
            domanda_content = premessa + user_comment
            data_payload = {"domanda": domanda_content}
            json_data = json.dumps(data_payload).replace('"', '\\"')
            
            command = f'''curl -X POST -H "Content-Type: application/json" -d "{json_data}" http://127.0.0.1:5001/ricevi_domanda'''

            print(f"Executing command: {command}")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Log the result of the command execution
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            response_json = json.loads(result.stdout)
            risposta = response_json["message"].split("risposta ottenuta:")[-1].strip()
            print(risposta)

            




    


