import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1398723132721860649/My7tTG5YKIV4PRs6AxXvr4CMRxRtCeOhzgCnwWmX2gxgrXsyiU6oL-jnY7HblisKo3vg"
URL = "https://www.backmarket.fr/fr-fr/p/iphone-14-pro-128-go-violet-intense-debloque-tout-operateur/fa0b419c-f920-4e16-837f-d17e44d94475?l=10"

def send_discord_message(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message envoyé sur Discord ✅")
    else:
        print(f"Erreur en envoyant sur Discord : {response.status_code} - {response.text}")

def main():
    driver = None
    try:
        driver = uc.Chrome()
        driver.get(URL)

        wait = WebDriverWait(driver, 15)

        # Cliquer sur le bouton "Parfait" (état parfait)
        try:
            condition_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[data-test='productpage-condition-button']")))
            for btn in condition_buttons:
                if "parfait" in btn.text.lower():
                    btn.click()
                    print("État 'Parfait' sélectionné")
                    break
            time.sleep(2)  # attendre que le prix se mette à jour
        except Exception as e:
            print("Bouton 'Parfait' non trouvé ou erreur :", e)

        # Récupérer le prix
        prix_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-qa='productpage-product-price']")))
        prix = prix_element.text

        print(f"Prix violet parfait état trouvé : {prix}")
        send_discord_message(f"📢 Prix iPhone 14 Pro 128Go Violet Intense parfait état sur Back Market : {prix}")

    except Exception as e:
        print("Erreur durant l'extraction ou l'envoi :", e)

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
