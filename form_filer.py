from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import time

# הגדרות:
# החלף את ה-URL בכתובת של הטופס שלך
URL_TO_FORM = "https://url.com/" 
# מספר הפעמים שתרצה למלא את הטופס
NUMBER_OF_SUBMISSIONS = 1

# הגדרת ה-Faker ליצירת נתונים אקראיים
fake = Faker('he_IL') # ניתן להשתמש בשפה ספציפית

# מזהי רכיבים
FIELD_FIRST_NAME_ID = "first_name" 
FIELD_LAST_NAME_ID = "last_name" 
FIELD_MOBILE_PHONE_ID = "mobile_phone"
FIELD_EMAIL_ID = "email" 
FIELD_ID_NUMBER_ID = "id_number"
FIELD_CURRENT_INSTITUTION_ID = "current_institution"
FIELD_EDUCATOR_NAME_ID = "educator_name"
FIELD_EDUCATOR_PHONE_ID = "educator_phone"
FIELD_CITY_ID = "city"
FIELD_FULL_ADDRESS_ID = "full_address"
FIELD_IMAGE_UPLOAD_ID = "photo"
ABSOLUTE_IMAGE_PATH = "C:/Users/User/Downloads/photo.jpg"

SUBMIT_BUTTON_XPATH = "//button[contains(., 'שלח')]"  # משתמשים ב-XPath שמחפש את הטקסט "שלח" בתוך כפתור

def fill_and_submit_form(driver, attempt_num):
    """ממלא את הטופס בנתונים אקראיים ושולח אותו."""
    try:
        # 1. ניווט לדף הטופס
        driver.get(URL_TO_FORM)
        print(f"--- starting to try {attempt_num} ---")
        
        # 2. יצירת נתונים אקראיים לניסיון הנוכחי
        data = {
            FIELD_FIRST_NAME_ID: fake.first_name(),
            FIELD_LAST_NAME_ID: fake.last_name(),
            FIELD_MOBILE_PHONE_ID: fake.phone_number(),
            FIELD_EMAIL_ID: fake.email(),
            FIELD_ID_NUMBER_ID: str(fake.unique.random_int(min=100000000, max=999999999)), # 9 ספרות רנדומליות
            FIELD_CURRENT_INSTITUTION_ID: fake.company(),
            FIELD_EDUCATOR_NAME_ID: fake.name(),
            FIELD_EDUCATOR_PHONE_ID: fake.phone_number(),
            FIELD_CITY_ID: fake.city(),
            FIELD_FULL_ADDRESS_ID: fake.address(),
        }
        driver.implicitly_wait(10)
        # 3. מילוי שדות הטקסט
        for field_id, value in data.items():
            try:
                # משתמשים ב-By.ID כפי שהגדרת
                field = driver.find_element(By.ID, field_id)
                field.send_keys(value)
                # print(f"filled: {field_id}")
            except Exception as e:
                print(f"eror at {field_id}: {e}")
                
        # 4. העלאת קובץ (תמונה)
        try:
            upload_element = driver.find_element(By.ID, FIELD_IMAGE_UPLOAD_ID)
            # שליחת הנתיב המוחלט לקובץ הקלט (זה מה ש-Selenium דורש)
            upload_element.send_keys(ABSOLUTE_IMAGE_PATH)
            print("הועלה קובץ תמונה בהצלחה.")
        except Exception as e:
            print(f"eror uploading file {e}")


        # 5. לחיצה על כפתור השליחה
        submit_button = driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH)
        submit_button.click()
        
        # 6. המתנה לתגובת המערכת
        time.sleep(3) 

        print("✔ הטופס נשלח בהצלחה.")

    except Exception as e:
        print(f"❌ כשל קריטי בניסיון {attempt_num}: {e}")
        # אם יש כשל, שמור צילום מסך לצורך ניפוי באגים
        driver.save_screenshot(f"error_screenshot_{attempt_num}.png")

if __name__ == "__main__":
    # שימוש ב-webdriver_manager כדי לנהל את ה-Chromedriver באופן אוטומטי
    # (מומלץ במקום להוריד ידנית)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    for i in range(1, NUMBER_OF_SUBMISSIONS + 1):
        fill_and_submit_form(driver, i)
        
    # סגירת הדפדפן בסיום
    driver.quit()
    print(f"\nהסתיימו {NUMBER_OF_SUBMISSIONS} ניסיונות מילוי.")