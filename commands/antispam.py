from zlapi.models import Message, MultiMsgStyle, MessageStyle, Mention
from logging_utils import Logging
import time
from config import PREFIX 
logger = Logging()

class AntiSpamHandler:
    def __init__(self, client):
        self.client = client
        # Khởi tạo các biến để theo dõi spam (MỚI)
        self.spam_violations = {}
        self.violation_window = 5  # 5 giây
        self.kick_threshold = 5    # 5 tin nhắn trong 5 giây sẽ bị coi là spam
        
    def get_user_name(self, uid):
        # Hàm tiện ích lấy tên người dùng (MỚI)
        try:
            user_info = self.client.fetchUserInfo(uid)
            return user_info.changed_profiles.get(str(uid), {}).get('zaloName', str(uid))
        except: 
            return str(uid)

    def handle_antispam_command(self, message, message_object, thread_id, thread_type, author_id):
        command = message.lower().split()
        # Dùng hàm get_user_name mới
        name = self.get_user_name(author_id)

        if len(command) != 2:
            rest_text = f"Ê cu! Dùng đúng cú pháp {PREFIX}antisp on/off hộ cái nhá! 🙄"
            msg = f"{name}\n➜{rest_text}"
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
            ])
            self.client.replyMessage(
                Message(text=msg, style=styles),
                message_object, thread_id, thread_type, ttl=30000
            )
            self.client.sendReaction(message_object, "👉", thread_id, thread_type, reactionType=75)
            return

        if str(author_id) not in self.client.ADMIN:
            rest_text = "Xin lỗi bạn iu nha, lệnh này chỉ admin mới được dùng thôi 🥲"
            msg = f"{name}\n➜{rest_text}"
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
            ])
            self.client.replyMessage(
                Message(text=msg, style=styles),
                message_object, thread_id, thread_type, ttl=30000
            )
            self.client.sendReaction(message_object, "🔒", thread_id, thread_type, reactionType=75)
            return

        action = command[1]
        current_state = self.client.spam_enabled.get(thread_id, False)

        if action == 'on':
            if current_state:
                rest_text = "Chế độ chống spam đã bật sẵn rồi mà, cần bật lại đâu! 😎"
                msg = f"{name}\n➜{rest_text}"
                styles = MultiMsgStyle([
                    MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                    MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
                ])
                self.client.replyMessage(
                    Message(text=msg, style=styles),
                    message_object, thread_id, thread_type, ttl=30000
                )
                self.client.sendReaction(message_object, "🔄", thread_id, thread_type, reactionType=75)
            else:
                self.client.spam_enabled[thread_id] = True
                # Cập nhật thông báo trạng thái với ngưỡng mới
                rest_text = f" đã bật chế độ chống spam. Gửi >{self.kick_threshold} tin nhắn trong {self.violation_window}s sẽ bị chặn ngay lập tức. 💪"
                msg = f"{name}\n➜{rest_text}"
                styles = MultiMsgStyle([
                    MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                    MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
                ])
                self.client.replyMessage(
                    Message(text=msg, style=styles),
                    message_object, thread_id, thread_type, ttl=30000
                )
                self.client.sendReaction(message_object, "✅", thread_id, thread_type, reactionType=75)
        elif action == 'off':
            if not current_state:
                rest_text = "Chế độ chống spam đã tắt sẵn rồi, tắt thêm chi nữa! 😜"
                msg = f"{name}\n➜{rest_text}"
                styles = MultiMsgStyle([
                    MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                    MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
                ])
                self.client.replyMessage(
                    Message(text=msg, style=styles),
                    message_object, thread_id, thread_type, ttl=30000
                )
                self.client.sendReaction(message_object, "🔄", thread_id, thread_type, reactionType=75)
            else:
                self.client.spam_enabled[thread_id] = False
                rest_text = " đã tắt chống spam rồi, ae quẩy thoải mái đi! 🎉"
                msg = f"{name}\n➜{rest_text}"
                styles = MultiMsgStyle([
                    MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                    MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
                ])
                self.client.replyMessage(
                    Message(text=msg, style=styles),
                    message_object, thread_id, thread_type, ttl=30000
                )
                self.client.sendReaction(message_object, "💨", thread_id, thread_type, reactionType=75)
        else:
            rest_text = f"Lệnh sai be bét rồi! Phải là {PREFIX}antisp on/off cơ mà 🤔"
            msg = f"{name}\n➜{rest_text}"
            styles = MultiMsgStyle([
                MessageStyle(offset=0, length=len(name), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=0, length=len(name), style="bold", auto_format=False),
            ])
            self.client.replyMessage(
                Message(text=msg, style=styles),
                message_object, thread_id, thread_type, ttl=30000
            )
            self.client.sendReaction(message_object, "❌", thread_id, thread_type, reactionType=75)

        self.client.save_spam_settings()

    # --- Hàm xử lý spam (MỚI) ---
    def check_and_handle_spam(self, message_object, thread_id, thread_type, author_id):
        
        # 1. Kiểm tra trạng thái Anti-Spam, Admin và Whitelist
        if not self.client.spam_enabled.get(thread_id, False) or \
           self.client.is_group_admin(thread_id, author_id) or \
           (str(thread_id) in self.client.whitelist and str(author_id) in self.client.whitelist.get(str(thread_id), [])):
            return False

        now = time.time()
        
        if thread_id not in self.spam_violations:
            self.spam_violations[thread_id] = {}
        
        # Lấy hoặc khởi tạo lịch sử tin nhắn của người dùng trong nhóm
        user_history = self.spam_violations[thread_id].get(author_id, {'timestamps': [], 'kicked': False})

        # 2. Xóa tin nhắn ngay cả khi đã bị kick
        if user_history['kicked']:
            try:
                msg_id, cli_msg_id = message_object.get('msgId'), message_object.get('cliMsgId')
                if msg_id: self.client.deleteGroupMsg(msg_id, author_id, cli_msg_id, thread_id)
            except:
                pass
            return True

        # 3. Lọc bỏ các tin nhắn cũ ngoài window và thêm tin nhắn hiện tại
        user_history['timestamps'] = [t for t in user_history['timestamps'] if now - t <= self.violation_window]
        user_history['timestamps'].append(now)
        current_count = len(user_history['timestamps'])
        
        self.spam_violations[thread_id][author_id] = user_history
        
        name = self.get_user_name(author_id)
        tag_author = f"{name}"
        msg = ""

        # 4. Kiểm tra ngưỡng và thực hiện hành động (1 phát xoá kick luôn)
        if current_count >= self.kick_threshold:
            # Lần đầu chạm ngưỡng Spam: Xóa + Kick/Block
            try:
                # Xóa tin nhắn bị coi là spam
                msg_id, cli_msg_id = message_object.get('msgId'), message_object.get('cliMsgId')
                if msg_id: self.client.deleteGroupMsg(msg_id, author_id, cli_msg_id, thread_id)
                
                # Thực hiện Block/Kick
                self.client.blockUsersInGroup(author_id, thread_id)
                
                # Cập nhật trạng thái đã kick
                user_history['kicked'] = True
                self.spam_violations[thread_id][author_id] = user_history
                
                rest_text = f"📣 {tag_author} đã bị chặn khỏi nhóm do gửi quá {self.kick_threshold} tin nhắn trong {self.violation_window} giây."
            except Exception as e:
                rest_text = f"Đã cố gắng chặn {tag_author} nhưng thất bại. Lỗi: {e}"
            
            msg = f"➜ [ANTI-SPAM]\n{tag_author}\n➜ {rest_text}"
        
        # 5. Phản hồi nếu có tin nhắn cảnh báo
        if msg:
            tag_offset = msg.find(tag_author)
            styles = MultiMsgStyle([
                MessageStyle(offset=len("➜ "), length=len("[ANTI-SPAM]"), style="color", color="#db342e", auto_format=False),
                MessageStyle(offset=len("➜ "), length=len("[ANTI-SPAM]"), style="bold", auto_format=False)
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
    'description': "Bật/Tắt chống spam tin nhắn liên tục",
    'power': "Admin"
}

def PTA():
    return {'antispam': AntiSpamHandler(None).handle_antispam_command}
