import json
import requests
import re

# رابط تغذية بلوجر وملف الجيسون في المستودع
blogger_api_url = "https://el-gubba-guide.blogspot.com/feeds/posts/default?alt=json"
json_file_path = "blog_notifications.json"

try:
    res = requests.get(blogger_api_url, timeout=10)
    if res.status_code == 200:
        data = res.json()
        entries = data.get('feed', {}).get('entry', [])
        if entries:
            latest = entries[0]
            title = latest.get('title', {}).get('$t', '')
            post_id = str(latest.get('id', {}).get('$t', title))
            
            # استخراج ملخص النص وتنظيف وسوم HTML
            content = latest.get('summary', {}).get('$t', latest.get('content', {}).get('$t', 'توجد تفاصيل جديدة في المنصة'))
            clean_content = re.sub('<.*?>', '', content).strip()[:100]

            new_data = [{
                "id": post_id,
                "title": title,
                "message": clean_content if clean_content else "عرض جديد في منصة القبة",
                "date": latest.get('published', {}).get('$t', '')[:10]
            }]

            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            print("تم تحديث الملف بنجاح بآخر منشور من بلوجر!")
except Exception as e:
    print(f"حدث خطأ أثناء التحديث: {e}")
  
