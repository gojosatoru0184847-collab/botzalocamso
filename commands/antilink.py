import json
import os
import time
from zlapi.models import Message, ThreadType, MultiMsgStyle, MessageStyle, Mention
from config import PREFIX

class AntiLinkHandler:
    def __init__(self, client):
        self.client = client
        self.settings_file = "data/antilink_settings.json"
        self.enabled_groups = self.load_settings()
        self.link_violations = {}
        # Khoảng thời gian tính vi phạm: 30 ngày (tính theo giây) => 1 tháng gần nhất
        self.violation_window = 30 * 24 * 60 * 60
        # Kick sau 2 lần trong khoảng violation_window (2 lần/tháng)
        self.kick_threshold = 2
        # Nhắc lần 1 (không cần biến riêng nhưng giữ logic cho rõ ràng)
        self.warn_threshold = 1

    def load_settings(self):
        if not os.path.exists("data"): os.makedirs("data")
        try:
            with open(self.settings_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.enabled_groups, f, indent=4)

    def is_enabled(self, thread_id):
        return self.enabled_groups.get(str(thread_id), False)

    def get_user_name(self, uid):
        try:
            user_info = self.client.fetchUserInfo(uid)
            return user_info.changed_profiles.get(str(uid), {}).get('zaloName', str(uid))
        except:
            return str(uid)

    def handle_antilink_command(self, message_text, message_object, thread_id, thread_type, author_id):
        name = self.get_user_name(author_id)
        
        if str(author_id) not in self.client.ADMIN:
            rest_text = "⚠️ Bạn không có quyền sử dụng lệnh này."
            msg = f"{name}\n➜{rest_text}"
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=0, length=len(name), style="bold", auto_format=False)
            ])
            self.client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type, ttl=60000)
            for r_icon in ["❌", "🚫", "🔐"]:
                self.client.sendReaction(message_object, r_icon, thread_id, thread_type, reactionType=75)
            return

        parts = message_text.lower().split()
        action = parts[1] if len(parts) > 1 else ""

        if action not in ["on", "off"]:
            current_status = "Bật ✅" if self.is_enabled(thread_id) else "Tắt ❌"
            rest_text = f"🚦Hướng dẫn: {PREFIX}antilink <on/off>\n➜Trạng thái hiện tại: {current_status}"
            msg = f"{name}\n➜{rest_text}"
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=0, length=len(name), style="bold", auto_format=False)
            ])
            self.client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type, ttl=60000)
            for r_icon in ["👉", "📜", "ℹ️"]:
                self.client.sendReaction(message_object, r_icon, thread_id, thread_type, reactionType=75)
            return

        thread_id_str = str(thread_id)
        if action == "on":
            if self.is_enabled(thread_id_str):
                rest_text = "Chế độ Anti-Link đã được bật trước đó. 🔄"
                reactions = ["⚠️", "🔗", "🔄"]
            else:
                self.enabled_groups[thread_id_str] = True
                self.save_settings()
                rest_text = f"Đã bật Anti-Link. Vi phạm {self.kick_threshold} lần/tháng sẽ bị kick. 🛡️"
                reactions = ["✅", "🛡️", "🔗"]
        else:
            if not self.is_enabled(thread_id_str):
                rest_text = "Chế độ Anti-Link đã được tắt trước đó. 🔄"
                reactions = ["⚠️", "🔗", "🔓"]
            else:
                if thread_id_str in self.enabled_groups:
                    del self.enabled_groups[thread_id_str]
                self.save_settings()
                rest_text = "Đã tắt chế độ Anti-Link. 🔓"
                reactions = ["🚫", "🔗", "🔓"]
        
        msg = f"{name}\n➜{rest_text}"
        styles = MultiMsgStyle([
            MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
            MessageStyle(offset=0, length=len(name), style="bold", auto_format=False)
        ])
        self.client.replyMessage(Message(text=msg, style=styles), message_object, thread_id, thread_type, ttl=60000)
        for r_icon in reactions:
            self.client.sendReaction(message_object, r_icon, thread_id, thread_type, reactionType=75)

    def check_and_handle_link(self, message_object, thread_id, thread_type, author_id):
        # Kiểm tra điều kiện không xử lý
        if not self.is_enabled(thread_id):
            return False
        if not self.client.is_url_in_message(message_object):
            return False
        if self.client.is_group_admin(thread_id, author_id):
            return False
        if (str(thread_id) in self.client.whitelist and
                str(author_id) in self.client.whitelist.get(str(thread_id), [])):
            return False

        try:
            msg_id, cli_msg_id = message_object.get('msgId'), message_object.get('cliMsgId')
            if msg_id:
                self.client.deleteGroupMsg(msg_id, author_id, cli_msg_id, thread_id)
        except Exception as e:
            self.client.logger.error(f"[AntiLink] Lỗi khi xóa link: {e}")
            return False

        now = time.time()
        thread_key = str(thread_id)
        author_key = str(author_id)

        if thread_key not in self.link_violations:
            self.link_violations[thread_key] = {}

        user_violations = self.link_violations[thread_key].get(author_key, {'count': 0, 'first_violation_time': now})

        # Nếu đã vượt qua khung thời gian (ví dụ hơn 30 ngày), reset về 1 lần vi phạm mới
        if now - user_violations['first_violation_time'] > self.violation_window:
            user_violations = {'count': 1, 'first_violation_time': now}
        else:
            user_violations['count'] += 1

        self.link_violations[thread_key][author_key] = user_violations
        count = user_violations['count']

        name = self.get_user_name(author_id)
        tag_author = f"{name}"
        msg = ""

        if count >= self.kick_threshold:
            # Sau lần thứ 2 trong khung violation_window: xóa + kick/block
            try:
                self.client.blockUsersInGroup(author_id, thread_id)
                rest_text = f"📣 {tag_author} đã bị kick khỏi nhóm vì gửi link vi phạm ({count}/{self.kick_threshold} lần trong vòng 30 ngày)."
                # Xóa record vi phạm sau khi đã kick để tránh kick lặp lại khi user quay lại
                try:
                    del self.link_violations[thread_key][author_key]
                except KeyError:
                    pass
            except Exception as e:
                rest_text = f"Đã cố gắng chặn {tag_author} nhưng thất bại. Lỗi: {e}"
            msg = f"➜ [ANTI-LINK]\n{tag_author}\n➜ {rest_text}"
        elif count == self.warn_threshold:
            # Lần 1: xóa + nhắc
            rest_text = "🚦 Nhóm có quy định không gửi link công khai. Đây là lần nhắc nhở đầu tiên trong vòng 30 ngày."
            msg = f"➜ [ANTI-LINK]\n{tag_author}\n➜ {rest_text}"

        if msg:
            tag_offset = msg.find(tag_author)
            styles = MultiMsgStyle([
                MessageStyle(offset=len("➜ "), length=len("[ANTI-LINK]"), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=len("➜ "), length=len("[ANTI-LINK]"), style="bold", auto_format=False)
            ])
            self.client.replyMessage(
                Message(
                    text=msg,
                    mention=Mention(uid=author_id, offset=tag_offset, length=len(tag_author)),
                    style=styles
                ),
                message_object,
                thread_id,
                thread_type,
                ttl=120000
            )
        return True
des = {
    'version': "1.0.0",
    'credits': "HOANG LAM",
    'description': "Bật/Tắt chống gửi đường link URL trong nhóm",
    'power': "Admin"
}

def PTA():
    return {'antilink': AntiLinkHandler(None).handle_antilink_command}
