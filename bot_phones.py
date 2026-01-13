import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. اسم الملف الذي نريد قراءته (الذي أنتجه الروبوت الأول)
filename = "google_maps_leads.xlsx"

print(f"📂 جاري قراءة ملف البيانات: {filename}...")

try:
    # نقرأ ملف الإكسل
    df = pd.read_excel(filename)
except FileNotFoundError:
    print("❌ خطأ: الملف غير موجود! تأكد أنك شغلت الكود الأول (bot_maps_final.py) أولاً.")
    exit()

# 2. تجهيز العمود الجديد
# إذا لم يكن هناك عمود اسمه "Phone"، نقوم بإنشائه
if 'Phone' not in df.columns:
    df['Phone'] = None

# 3. تشغيل المتصفح
print("🚀 جاري تشغيل المتصفح...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

print(f"🔍 لدينا {len(df)} شركة في القائمة. سأبدأ العمل عليها واحدة تلو الأخرى...")

# 4. الدوران (Loop) على كل صف في الإكسل
for index, row in df.iterrows():
    
    # ميزة ذكية: إذا كان الهاتف موجوداً مسبقاً، تخط هذا الصف (لا داعي لتضييع الوقت)
    # هذا مفيد جداً إذا أردت إيقاف البرنامج وتشغيله لاحقاً ليكمل من حيث توقف
    if pd.notna(row['Phone']) and str(row['Phone']) != 'nan':
        continue

    name = row['Name']
    link = row['Google Maps Link']
    
    print(f"➡️ [{index+1}/{len(df)}] جاري الدخول إلى: {name}")

    try:
        # الذهاب للرابط المباشر
        driver.get(link)
        
        # البحث عن زر الهاتف
        # هذا السطر يبحث عن أي زر يحتوي كوده المخفي على كلمة 'phone:'
        # وهي أضمن طريقة لأن جوجل يغير شكل الأزرار لكن لا يغير وظيفتها
        phone_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(@data-item-id, 'phone:')]")
        ))
        
        # الرقم موجود عادة في خاصية اسمها 'aria-label'
        phone_number = phone_btn.get_attribute("aria-label")
        
        # تنظيف الرقم من العبارات الزائدة (عربي، إنجليزي، فرنسي)
        if phone_number:
            phone_number = phone_number.replace("Phone:", "")\
                                       .replace("الهاتف:", "")\
                                       .replace("Numéro de téléphone:", "")\
                                       .replace("de téléphone:", "")\
                                       .strip()
                                       
            print(f"    📞 تم صيد الرقم: {phone_number}")
            
            # تحديث الخانة في الذاكرة
            df.at[index, 'Phone'] = phone_number
        else:
            print("    ⚠️ الزر موجود لكن لا يحتوي نصاً.")

    except Exception as e:
        print("    ❌ لا يوجد رقم هاتف (أو الصفحة مختلفة).")
        df.at[index, 'Phone'] = "Not Found" # نسجل أنه لا يوجد رقم حتى لا نعيد المحاولة

    # 5. الحفظ الدوري (Checkpoint)
    # كل 5 شركات، نحفظ الملف. لو انقطعت الكهرباء الآن، لن تخسر ما جمعته!
    if (index + 1) % 5 == 0:
        df.to_excel(filename, index=False)
        print("    💾 (تم حفظ التقدم...)")
    
    # استراحة قصيرة لتجنب الحظر
    time.sleep(1.5)

# الحفظ النهائي عند الانتهاء
df.to_excel(filename, index=False)
driver.quit()

print("\n" + "="*50)
print("✅ تمت المهمة بنجاح! مبروك، ملف الإكسل يحتوي الآن على الأرقام.")
print("="*50)