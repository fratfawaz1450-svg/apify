import os
import json
from apify_client import ApifyClient
from datetime import datetime

def main():
    # قراءة المفاتيح من المتغيرات البيئية
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
    INSTAGRAM_SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID")
    
    if not APIFY_API_TOKEN or not INSTAGRAM_SESSION_ID:
        print("Error: Missing API Token or Session ID")
        return

    # اسم المستخدم الخاص بك - غيّره إلى اسم حسابك
    YOUR_USERNAME = "f.f_aa.aa"

    # تهيئة عميل Apify
    client = ApifyClient(APIFY_API_TOKEN)

    # ============================================
    # 1. جلب قائمة المتابَعين (Following)
    # ============================================
    print(f"🔄 جاري جلب قائمة المتابَعين لحساب {YOUR_USERNAME}...")
    
    following_input = {
        "urls": [f"https://www.instagram.com/{YOUR_USERNAME}/following"],
        "resultsLimit": 500,
        "sessionId": INSTAGRAM_SESSION_ID
    }
    
    try:
        following_run = client.actor("api-ninja/instagram-scraper").call(run_input=following_input)
        following_items = list(client.dataset(following_run["defaultDatasetId"]).iterate_items())
        print(f"✅ تم جلب {len(following_items)} متابع")
        
        with open('following_data.json', 'w', encoding='utf-8') as f:
            json.dump(following_items, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ فشل في جلب قائمة المتابَعين: {e}")
        following_items = []

    # ============================================
    # 2. جلب قائمة المتابعين (Followers)
    # ============================================
    print(f"🔄 جاري جلب قائمة المتابعين لحساب {YOUR_USERNAME}...")
    
    followers_input = {
        "urls": [f"https://www.instagram.com/{YOUR_USERNAME}/followers"],
        "resultsLimit": 500,
        "sessionId": INSTAGRAM_SESSION_ID
    }
    
    try:
        followers_run = client.actor("api-ninja/instagram-scraper").call(run_input=followers_input)
        followers_items = list(client.dataset(followers_run["defaultDatasetId"]).iterate_items())
        print(f"✅ تم جلب {len(followers_items)} متابع")
        
        with open('followers_data.json', 'w', encoding='utf-8') as f:
            json.dump(followers_items, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"❌ فشل في جلب قائمة المتابعين: {e}")
        followers_items = []

    # ============================================
    # 3. إنشاء تقرير ملخص
    # ============================================
    summary = {
        "username": YOUR_USERNAME,
        "scraped_at": datetime.now().isoformat(),
        "followers_count": len(followers_items),
        "following_count": len(following_items)
    }
    
    with open('summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
    
    print("\n📊 ملخص:")
    print(f"   - عدد المتابعين: {len(followers_items)}")
    print(f"   - عدد المتابَعين: {len(following_items)}")

if __name__ == "__main__":
    main()