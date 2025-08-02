import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://www.backmarket.fr/fr-fr/p/iphone-14-pro-128-go-violet-intense-debloque-tout-operateur/fa0b419c-f920-4e16-837f-d17e44d94475?l=10"

def send_discord_message(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message envoyé sur Discord ✅")
    else:
        print(f"Erreur en envoyant sur Discord : {response.status_code} - {response.text}")

def main():
    try:
        driver = uc.Chrome()
        driver.get(URL)

        wait = WebDriverWait(driver, 15)
        prix_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.heading-2[data-qa='productpage-product-price']")))
        prix = prix_element.text

        print(f"Prix trouvé : {prix}")
        send_discord_message(f"📢 Prix iPhone 14 Pro Violet Intense 128Go (Parfait état) : {prix}")

    except Exception as e:
        print("Erreur durant l'extraction ou l'envoi :", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
