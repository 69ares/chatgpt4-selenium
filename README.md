# GPT4 - SeleniumChat 
Free chatgpt4 with Selenium

# Setup:
Ensure you have Chrome installed

- https://chromedriver.chromium.org/downloads


Start it with the given command to enable remote debugging.

Windows:

- "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9998 --user-data-dir=openai


You can send a POST request with a different question payload to http://127.0.0.1:5001/ricevi_domanda to get an answer
- curl -X POST -H "Content-Type: application/json" -d "{\"domanda\":\"ciao come stai?\"}" http://127.0.0.1:5001/ricevi_domanda


### Media:
![Screenshot 2023-08-24 182007](https://github.com/69ares/chatgpt4-selenium/assets/35406032/0794079a-abde-48e4-be79-26013533bdd5)



# Possible Uses:
## Automated Question-Answer System:
The script can be used as an automated system to pose questions to a web-based chatbot and obtain answers.

## Testing and Validation:
If you're developing or testing a web-based chat system, this script can be a tool to automatically pose questions and verify the responses.

## Data Collection:
You can modify the script to send a series of questions and collect answers, which can then be used for data analysis or training machine learning models.
