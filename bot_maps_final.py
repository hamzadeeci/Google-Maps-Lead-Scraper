from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd # لا تنس استدعاء مكتبة الباندا
import time

# 1. تشغيل المتصفح
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

print("🌍 جاري فتح خرائط جوجل...")
driver.get("https://www.google.com/maps")

# ---------------------------------------------------------
# الجزء اليدوي (Human Mode)
# ---------------------------------------------------------
print("\n" + "="*50)
print("🛑 تعليمات المدير:")
print("1. ابحث بيدك عن (Restaurants in Dubai) أو (Dentists in Riyadh)...")
print("2. تأكد أن القائمة الجانبية ظهرت.")
print("3. عد لهنا واضغط ENTER.")
print("="*50 + "\n")

input("⌨️ أنا جاهز.. اضغط Enter بعد أن تنتهي من البحث...")

# ---------------------------------------------------------
# الجزء الآلي: التمرير والسحب
# ---------------------------------------------------------
print("🤖 جاري العمل... سأقوم بتحميل المزيد من النتائج أولاً.")

try:
    # 1. الإمساك بالقائمة
    scrollable_div = driver.find_element(By.XPATH, "//div[@role='feed']")
    
    # 2. التمرير (سنجعله 5 مرات، يمكنك زيادتها لـ 10 أو 20 لجلب مئات النتائج)
    for i in range(5):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        print(f"🔄 تمرير رقم {i+1}...")
        time.sleep(3) # الانتظار مهم جداً هنا

    print("🛑 انتهى التمرير. جاري سحب البيانات الآن...")
    
    # 3. سحب البيانات
    # الخدعة: نبحث عن كل الروابط التي تحتوي على كلمة "google.com/maps/place"
    # لأن هذه هي روابط المحلات فقط
    results = driver.find_elements(By.XPATH, "//a[contains(@href, '/maps/place')]")

    print(f"📦 وجدنا {len(results)} محلاً. جاري استخراج التفاصيل...")

    data = [] # السلة

    for item in results:
        # جوجل تضع اسم المحل داخل خاصية aria-label للرابط
        name = item.get_attribute("aria-label")
        
        # الرابط نفسه
        link = item.get_attribute("href")

        # نتأكد أن الاسم ليس فارغاً (أحياناً توجد روابط مخفية)
        if name and link:
            # تنظيف البيانات: أحياناً الاسم يكون طويلاً جداً
            print(f"📌 سحب: {name}")
            
            data.append({
                'Name': name,
                'Google Maps Link': link
            })

    # 4. الحفظ في Excel
    if len(data) > 0:
        df = pd.DataFrame(data)
        df.to_excel("google_maps_leads.xlsx", index=False)
        print(f"\n✅ تم حفظ {len(data)} شركة في ملف 'google_maps_leads.xlsx' بنجاح!")
    else:
        print("⚠️ لم يتم العثور على بيانات لسحبها.")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")

print("تم الانتهاء. اضغط Enter للإغلاق.")
input()
driver.quit()