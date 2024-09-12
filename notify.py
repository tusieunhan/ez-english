import schedule
import time
import pync
import random
import json
import subprocess

def load_vocabulary(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Lỗi khi đọc file JSON: {file_path}")
        return []

# Đường dẫn đến file JSON chứa từ vựng
vocabulary_file = 'vocabulary.json'

# Tải từ vựng từ file JSON
vocabulary = load_vocabulary(vocabulary_file)

# Danh sách để theo dõi các từ đã sử dụng
used_words = []

def say_text(text):
    subprocess.run(['say', text])

def send_notification():
    global vocabulary, used_words
    
    if not vocabulary:
        print('Danh sách từ vựng trống.')
        return

    if len(used_words) == len(vocabulary):
        print("Đã sử dụng hết tất cả các từ. Bắt đầu lại từ đầu.")
        used_words.clear()

    # Chọn một từ chưa được sử dụng
    available_words = [word for word in vocabulary if word not in used_words]
    word = random.choice(available_words)
    used_words.append(word)

    title = f"{word['word']} - {word['mean']}".capitalize()
    message = f"{word['example']}"
    subtitle = f"{word['ipa']}"
    
    # Gửi thông báo
    pync.notify(
        title=title,
        message=message,
        subtitle=subtitle,
        sound=True,
        group='vocabulary',
        appIcon='icon.png',
        contentImage='icon.png',
    )

    # Đọc to từ và ví dụ
    say_text(f"{word['word']}. {word['example']}")

    print(f"Đã gửi thông báo: {word['word']} - {word['mean']}")
    print(f"{word['example']}")
    print(f"Đã sử dụng {len(used_words)}/{len(vocabulary)} từ")

# Lên lịch gửi thông báo mỗi 5 phút
schedule.every(5).minutes.do(send_notification)

if __name__ == "__main__":
    if not vocabulary:
        print("Không thể tiếp tục vì danh sách từ vựng trống.")
    else:
        print(f"Đã tải {len(vocabulary)} từ vựng. Bắt đầu gửi thông báo...")
        while True:
            schedule.run_pending()
            time.sleep(1)