import requests

url = 'https://ahmed-mohamed2011-prodcut-system-api.hf.space/api/v1/products/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
def get_product_by_category():
    pass


def create_product(title, description, discount, stock, images):

    pass


def delete_product():
    pass


def update_product(id:str,data,files):
    try:
        response = requests.put(url+id,data=data,files=files, timeout=10)
        if response.status_code != 200:
            print("======== تفاصيل خطأ الباك إيند ========")
            print(response.text) # سيطبع لك الحقل المخطئ أو الناقص بالظبط
            print("======================================")

        response.raise_for_status()
        raw_json = response.json()
        return response.status_code
        if not response.status_code ==200 or not response.status_code == 201:
            return False
        return raw_json
    except Exception as e:
        raise e



def get_all_products():
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        raw_json = response.json()
        print("====== الـ JSON القادم من السيرفر ======")
        print(raw_json)
        print("=======================================")
        
        return raw_json

    except Exception as e:
        print(f"❌ حدث خطأ أثناء معالجة الـ JSON: {e}")
        return []