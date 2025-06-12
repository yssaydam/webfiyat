from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time
import subprocess

# === Selenium Ayarları ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# === ekeo.org.tr'ye Git ===
driver.get("https://ekeo.org.tr/")
time.sleep(5)  # Sayfa yüklenmesi için bekle

# === Tablo Verilerini Al ===
fiyatlar = {}
satirlar = driver.find_elements(By.CSS_SELECTOR, ".table tbody tr")
for satir in satirlar:
    kolonlar = satir.find_elements(By.TAG_NAME, "td")
    if len(kolonlar) >= 2:
        isim = kolonlar[0].text.strip()
        fiyat = kolonlar[1].text.strip()
        fiyatlar[isim] = fiyat

driver.quit()

# === JSON Dosyasına Yaz ===
with open("fiyatlar.json", "w", encoding="utf-8") as f:
    json.dump(fiyatlar, f, ensure_ascii=False, indent=2)

print("✅ fiyatlar.json güncellendi.")

# === Git Commit ve Push ===
try:
    subprocess.run(["git", "add", "fiyatlar.json"], check=True)
    subprocess.run(["git", "commit", "-m", "Otomatik fiyat güncellemesi"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ GitHub'a gönderildi.")
except subprocess.CalledProcessError as e:
    print("❌ GitHub güncelleme HATASI:", e)