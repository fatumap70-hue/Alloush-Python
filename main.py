import streamlit as st
import json
import hashlib
import random
import hmac
import asyncio
import aiohttp
import re
import uuid
from urllib.parse import urlparse, parse_qs

# --- خوارزمية Gorgon الأصلية (لم نلمس أي حرف منها) ---
class Gorgon:
    def __init__(self):
        self.key, self.aid, self.iv = "97551682", "1233", "7263291a"
    def Hrr(self, n):
        out = []
        while True:
            b = n & 0x7F
            n >>= 7
            if n: out.append(b | 0x80)
            else:
                out.append(b)
                break
        return bytes(out)
    def vgeta(self, num, data): return self.Hrr((num << 3) | 2) + self.Hrr(len(data)) + data
    def Quick(self, num, s): return self.vgeta(num, s.encode() if isinstance(s, str) else s)
    def Enc(self, num, TikTok, url=None):
        if TikTok is None and url: TikTok = {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}
        if TikTok is None: return b""
        if isinstance(TikTok, dict): TikTok = json.dumps(TikTok, separators=(",", ":"))
        return self.Quick(num, TikTok)
    def build(self, params=None, cookies=None, data=None, payload=None, url=None):
        AHMED = self.Enc(1, params, url) + self.Enc(2, cookies) + self.Enc(3, data or payload)
        return AHMED
    def Encoder(self, params=None, cookies=None, data=None, payload=None, url=None):
        builded = self.build(params, cookies, data, payload, url)
        msg = builded + self.iv.encode() + self.aid.encode()
        h = hmac.new(self.key.encode(), msg, hashlib.md5).hexdigest()       
        return f"8404{random.randint(0, 0xFFFF):04x}{random.randint(0, 0xFFFF):04x}0000{h}{random.randint(0, 0xFFFF):04x}"

# --- تصميم الواجهة الفخم (تعديلات الألوان والحركات) ---
st.set_page_config(page_title="علــش @GX1GX1", layout="centered")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    @keyframes pulse-gold {
        0% { transform: scale(1); box-shadow: 0 0 5px #FFD700; }
        50% { transform: scale(1.05); box-shadow: 0 0 25px #FFD700; }
        100% { transform: scale(1); box-shadow: 0 0 5px #FFD700; }
    }
    .user-avatar {
        display: block; margin: auto; border: 4px solid #FFD700;
        border-radius: 50%; animation: pulse-gold 2s infinite;
    }
    .stButton>button {
        width: 100%; border-radius: 15px; background: linear-gradient(45deg, #FFD700, #DAA520);
        color: black; font-weight: 900; border: none; height: 3.5em; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,215,0,0.3); }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: #FFD700; border: 1px solid #DAA520; text-align: center; border-radius: 12px; }
    div[data-testid="stMetricValue"] { color: #FFD700; font-family: 'Courier New', monospace; text-align: center; font-size: 50px !important; }
    </style>
    """, unsafe_allow_html=True)

# الصورة الشخصية
st.markdown(f'<img src="https://i.ibb.co/cXgRkRTf/6e37bd54624a0d987f097ff5bb04a58e.jpg" class="user-avatar" width="180">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #FFD700;'>عـلــش | @GX1GX1</h1>", unsafe_allow_html=True)
st.write("---")

url_input = st.text_input("أدخل الرابط", placeholder="URL⮕")

if st.button("بدأ"):
    if url_input:
        counter_placeholder = st.empty()
        status_log = st.empty()
        
        class SayidWeb:
            def __init__(self, url):
                self.gg_encoder = Gorgon()
                self.url_input = url
                self.API = "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/"
                self.counter = 0

            def gen_params(self):
                # قمنا بنسخ الباراميترز الأصلية الخاصة بك كما هي تماماً
                return {
                    "manifest_version_code": "350302", "_rticket": str(int(random.random() * 10**16)),
                    "app_language": "en", "iid": str(random.randint(7*10**18, 9*10**18)),
                    "device_type": "RMX3941", "openudid": str(uuid.uuid4().hex[:16]),
                    "cdid": str(uuid.uuid4()), "aid": "1340", "ts": str(int(random.random() * 10**10)),
                    "device_id": str(random.randint(7*10**18, 9*10**18)), "app_name": "musically_go"
                }

            async def worker(self, session, video_id):
                while True:
                    params = self.gen_params()
                    payload = {'item_id': video_id, 'aweme_type': "0", 'play_delta': "1"}
                    gorgon_hex = self.gg_encoder.Encoder(params=params, data=payload)
                    headers = {
                        'User-Agent': "com.zhiliaoapp.musically.go",
                        'x-gorgon': gorgon_hex,
                        'x-khronos': str(int(random.random() * 10**10)),
                        'Cookie': "store-idc=alisg; install_id=7516928038623151879;"
                    }
                    try:
                        async with session.post(self.API, data=payload, headers=headers, params=params) as resp:
                            if resp.status == 200:
                                res_json = await resp.json()
                                if res_json.get("status_code") == 0:
                                    self.counter += 1
                                    # تحديث العداد بشكل فوري في المتصفح
                                    counter_placeholder.metric("الـسـرعة (عدد المشاهدات)", self.counter)
                    except: pass
                    # تأخير بسيط جداً (0.01) لضمان أن المتصفح لا يتجمد (Freeze)
                    await asyncio.sleep(0.01)

            async def start(self):
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(self.url_input, allow_redirects=True) as r:
                            match = re.search(r'/video/(\d+)', str(r.url))
                            if match:
                                vid = match.group(1)
                                status_log.success(f"تم الاتصال بنجاح! ID: {vid}")
                                # تشغيل 30 مهمة متوازية (أفضل عدد لموارد الويب)
                                tasks = [asyncio.create_task(self.worker(session, vid)) for _ in range(30)]
                                await asyncio.gather(*tasks)
                            else: st.error("تأكد من الرابط!")
                    except Exception as e: st.error(f"Error: {e}")

        # تشغيل التطبيق
        app = SayidWeb(url_input)
        asyncio.run(app.start())
    else:
        st.warning("أدخل الرابط أولاً")
