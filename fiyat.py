from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time

# Tarayıcı ayarları
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# ekeo.org.tr sayfasını aç
driver.get("https://ekeo.org.tr/")
time.sleep(5)  # Sayfa yüklenmesini bekle

# Verileri oku
fiyatlar = {}
satirlar = driver.find_elements(By.CSS_SELECTOR, ".table tbody tr")

for satir in satirlar:
    kolonlar = satir.find_elements(By.TAG_NAME, "td")
    if len(kolonlar) >= 2:
        isim = kolonlar[0].text.strip()
        fiyat = kolonlar[1].text.strip()
        fiyatlar[isim] = fiyat

driver.quit()

# JSON dosyasına yaz
with open("fiyatlar.json", "w", encoding="utf-8") as f:
    json.dump(fiyatlar, f, ensure_ascii=False, indent=2)

print("✅ fiyatlar.json oluşturuldu.")