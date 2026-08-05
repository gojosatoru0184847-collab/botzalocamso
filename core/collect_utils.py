# -*- coding: utf-8 -*-
import os, json, threading, re

COLLECT_CONFIG_FILE = "data/collect_settings.json"
CACHE_FILE = "data/hunted_files_cache.json"
cache_lock = threading.Lock()

# --- 🎯 DANH SÁCH ĐUÔI FILE "VÀNG" (CHỈ HÚT NHỮNG THỨ NÀY) ---
STRICT_EXT_WHITELIST = [
    ".apk", ".lua", ".zip", ".7z", ".py", ".sh", ".js", ".json", ".txt", ".cpp", ".h",
    ".mobileconfig", ".mobileprovision", ".pem", ".crt", ".p12", ".plist", ".conf", ".ipa",
    ".imazingapp", ".deb", ".dex", ".so", ".rar",
    ".html", ".htm", ".css", ".ts", ".java", ".kt", ".go", ".rb", ".rs", ".c", ".cs", ".sql"
]

# --- 🛑 CHẶN RÁC TUYỆT ĐỐI (BAO GỒM VOICE AAC/AMR) ---
EXT_BLACKLIST = [
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
    ".mp4", ".mp3", ".pdf", ".tmp", ".cache",
    ".aac", ".acc", ".amr", ".m4a", ".opus" # Voice message rác
]

# --- 🛑 CHẶN WEB RÁC (KHÔNG PHẢI LINK TẢI) ---
DOMAIN_BLACKLIST = [
    "tiktok.com", "facebook.com", "fb.com", "youtube.com", "youtu.be",
    "zdn.vn", "zadn.vn", "zalo.me", "postimg.cc", "imgur.com",
    "netlify.app", "github.io", "vercel.app", "pages.dev", "web.app",
    "google.com", "bing.com", "yahoo.com", "shopee.vn", "lazada.vn"
]

STRICT_HOST_WHITELIST = [
    "mediafire.com", "mega.nz", "terabox.com", "dlfl.vn", "apkadmin.com",
    "gofile.io", "top1mmo.com", "drive.google.com", "dropbox.com", "t.me"
]

MOD_KEYWORDS = ["mod", "menu", "ff", "hack", "vip", "script", "crack", "aimlock", "headshot", "regoil", "antena", "skin", "config", "v4", "v5", "v6", "ob5", "tut", "trick", "cấu hình", "khẩu lệnh", "mẹo"]

MOD_LINK_PATTERNS = [
    r'https?://(?:www\.)?mediafire\.com/\S+',
    r'https?://(?:www\.)?mega\.nz/\S+',
    r'https?://drive\.google\.com/\S+',
    r'https?://(?:www\.)?terabox\.com/\S+',
    r'https?://(?:www\.)?gofile\.io/\S+',
    r'https?://(?:www\.)?apkadmin\.com/\S+',
    r'https?://(?:www\.)?dlfl\.vn/\S+',
    r'https?://(?:www\.)?top1mmo\.com/\S+',
    r'https?://t\.me/\S+',
    r'https?://bit\.ly/\S+',
    r'https?://tinyurl\.com/\S+'
]

def load_hunted_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding='utf-8') as f: return set(json.load(f))
    except: pass
    return set()

def save_hunted_cache(cache_set):
    try:
        os.makedirs("data", exist_ok=True)
        with open(CACHE_FILE, "w", encoding='utf-8') as f: json.dump(list(cache_set)[-10000:], f)
    except: pass

global_hunted_cache = load_hunted_cache()

def load_collect_settings():
    try:
        if os.path.exists(COLLECT_CONFIG_FILE):
            with open(COLLECT_CONFIG_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
                data["enabled"] = True
                return data
    except: pass
    return {"enabled": True, "share_to_group": "3391175843265507499"}

def save_collect_settings(settings):
    try:
        os.makedirs("data", exist_ok=True)
        with open(COLLECT_CONFIG_FILE, "w", encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
    except: pass
