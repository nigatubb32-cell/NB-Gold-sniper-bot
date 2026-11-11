import os
import time
from datetime import datetime
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# ==========================================
# 1. አድሚን እና ቦት ማስተካከያ (CONFIGURATION)
# ==========================================
TOKEN = 8786628566:AAHFJCH6OAC8e6PvhVP22cITV9scACqlF_U # <--- ከ BotFather የወሰድከውን ትክክለኛ Token እዚህ አስገባ
ADMIN_ID = 8564747317        # <--- የእርስዎን ትክክለኛ የቴሌግራም Admin ID እዚህ አስገባ

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# ==========================================
# 2. የሰርቨር እና Keep-Alive ዌብ (24/7 RUNNING)
# ==========================================
@app.route('/')
def home():
    return "NB Sniper Forex Bot is 100% active and running 24/7! 🎯"

def run_web():
    # Render የሚጠይቀውን ፖርት (Port 8080) እንጠቀማለን
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ==========================================
# 3. የገበያ ሁኔታ ማረጋገጫ (MARKET STATUS CHECKER)
# ==========================================
def check_market_status():
    """
    weekday(): 0=ሰኞ, 1=ማክሰኞ, 2=እሮብ, 3=ሐሙስ, 4=አርብ, 5=ቅዳሜ, 6=እሁድ
    ቅዳሜ እና እሁድ ማርኬቱ ዝግ መሆኑን በራሱ ይለያል።
    """
    current_weekday = datetime.now().weekday()
    
    if current_weekday == 5 or current_weekday == 6:
        return "🔴 **MARKET CLOSED (ማርኬት ተዘግቷል - Weekend Break)**"
    else:
        return "🟢 **MARKET OPEN (ማርኬት ክፍት ነው - Sniper Mode Active)**"

# ==========================================
# 4. ቦቱ ሲነሳ ወይም ዳታ ሲከፈት የሚደረግ ማሳሰቢያ
# ==========================================
def send_startup_notification():
    current_time = datetime.now().strftime('%Y-%m-%d | %H:%M:%S (ኢትዮጵያ ሰዓት)')
    market_status = check_market_status()
    
    startup_msg = (
        "🟢 **[SYSTEM ONLINE & SYNCED]** 🟢\n\n"
        f"⏱ **ዳታ የተከፈተበት ሰዓት:** `{current_time}`\n"
        f"📊 **የገበያ ሁኔታ:** {market_status}\n\n"
        "🎯 **የቅርብ ጊዜ የስናይፐር ሴታፕ:**\n"
        "• **Asset:** Gold (XAU/USD)\n"
        "• **Time Trigger:** ከቀኑ 3:30\n"
        "• **Precision Entry:** `4040.0`\n"
        "• **Stop Loss (SL):** `4035.0`\n"
        "• **Take Profit (TP):** `4080.0`\n\n"
        "🔥 *ቦቱ ያንዳች እረፍት ማርኬቱን እየተከታተለ ይገኛል!*"
    )
    try:
        bot.send_message(ADMIN_ID, startup_msg, parse_mode="Markdown")
    except Exception as e:
        print(f"Startup message error: {e}")

# ==========================================
# 5. የቴሌግራም ቦት ትዕዛዞች እና መስተጋብር (HANDLERS)
# ==========================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    market_status = check_market_status()
    
    welcome_text = (
        f"ሰላም **{user_name}**! 🎯\n\n"
        f"የአሁኑ የገበያ ሁኔታ፦ {market_status}\n\n"
        "ወደ **NB Sniper Forex Bot** በደህና መጡ። ይህ ስማርት ሲስተም ማርኬቱ ክፍት ሲሆን ዒላማውን ይጠብቃል፤ ዝግ ሲሆን ደግሞ እረፍት ያደርጋል።\n\n"
        "ከታች ካሉት አማራጮች ውስጥ የሚፈልጉትን ይምረጡ፡"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_sniper = types.InlineKeyboardButton("🎯 የዛሬው የ Sniper XAU/USD Setup", callback_data="sniper_setup")
    btn_mindset = types.InlineKeyboardButton("🧠 የ Sniper ትሬደር ስነ-ልቦና", callback_data="sniper_mindset")
    btn_contact = types.InlineKeyboardButton("👨‍💻 ዋና አበልጻጊውን ማነጋገር", url="https://t.me/YOUR_USERNAME")
    
    markup.add(btn_sniper, btn_mindset, btn_contact)
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    market_status = check_market_status()
    
    if call.data == "sniper_setup":
        if "CLOSED" in market_status:
            sniper_text = (
                "🔴 **[MARKET CLOSED - WEEKEND BREAK]** 🔴\n\n"
                "• **Status:** የፎርክስ ገበያ (XAU/USD) ቅዳሜ እና እሁድ ዝግ ነው።\n"
                "• **Action:** አሁን ቻርት ላይ ምንም ዓይነት ትሬድ አይከፈትም። ዘና ይበሉ፣ ትንተናዎን ሰንበትበት አድርገው ከሰኞ ጀምሮ አብረን እንጠብቃለን!\n\n"
                "📌 *ስናይፐር በሰዓቱ አያርፍም ግን ማርኬቱ ዝግ ሲሆን አላስፈላጊ ጥይት አያባክንም!*"
            )
        else:
            sniper_text = (
                "🎯 **[ACTIVE LIVE SNIPER SETUP]** 🎯\n\n"
                "• **Asset:** Gold (XAU/USD)\n"
                "• **Precision Entry Zone:** `4040.0`\n"
                "• **Stop Loss (SL):** `4035.0`\n"
                "• **Take Profit (TP):** `4080.0`\n\n"
                "📌 **የስናይፐር መርህ፦** ቆሻሻ ዞኖች ላይ አይተኮስም፤ ቻርቱ እስኪደርስ በትዕግስት ይጠብቃል!\n\n"
                "⚠️ *ማሳሰቢያ፦ የራስዎን ሪስክ ማኔጅመንት ሁልጊዜ ቅድሚያ ይስጡ።*"
            )
            
        bot.answer_callback_query(call.id, "የገበያ ሁኔታ እና ሴታፕ ተጭኗል! 🎯")
        bot.send_message(call.message.chat.id, sniper_text, parse_mode="Markdown")

    elif call.data == "sniper_mindset":
        mindset_text = (
            "🧠 **የ Sniper Trader ህግጋቶች፦**\n\n"
            "1. **ትዕግስት (Patience):** ስናይፐር ትክክለኛውን ዞን እስኪነካ ድረስ ቻርቱ ፊት በትዕግስት ይጠብቃል።\n"
            "2. **አነስተኛ ሪስክ (Low Risk):** ሎት ሳይዝህን በቁጥጥር ስር አውልለው።\n"
            "3. **ምንም ጸጸት የለም (No FOMO):** ማርኬቱ ሁልጊዜ አለ።"
        )
        bot.answer_callback_query(call.id, "የስናይፐር አስተሳሰብ ተጭኗል!")
        bot.send_message(call.message.chat.id, mindset_text, parse_mode="Markdown")

# አድሚኑ (አንተ) አዲስ ሲግናል በሰዓቱ እና በዋጋው በቀጥታ መላኪያ ትዕዛዝ
@bot.message_handler(commands=['send_signal'])
def admin_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ ይቅርታ! ይህንን ትዕዛዝ መጠቀም የሚችለው ዋናው አበልጻጊ (አድሚን) ብቻ ነው።")
        return
    
    command_text = message.text
    parts = command_text.split(' ', 1)
    
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ ትክክለኛውን ትዕዛዝ ያስገቡ።\nአጠቃቀም፦ `/send_signal 3:30 ላይ Entry 4040 | SL 4035 | TP 4080`", parse_mode="Markdown")
        return
    
    signal_content = parts[1]
    broadcast_msg = f"🚨 **VIP SNIPER TIMED ALERT** 🚨\n\n{signal_content}\n\n🔥 *በ NB Sniper Bot የተላከ*"
    
    bot.reply_to(message, "✅ ሴታፕ ሰዓቱ ተጠብቆ ተልኳል!")
    bot.send_message(message.chat.id, broadcast_msg, parse_mode="Markdown")

# ==========================================
# 6. ቦቱን ማስጀመር (MAIN EXECUTION)
# ==========================================
if __name__ == '__main__':
    # ሰርቨሩን ማስነሳት
    keep_alive()
    print("NB Sniper Forex Bot በሙሉ ዝግጅት እና ጥራት በመስራት ላይ ይገኛል...")
    
    # ቦቱ ሲነሳ የመጀመሪያውን ሪፖርት መላክ
    time.sleep(2)
    send_startup_notification()
    
    # ቦቱን ሁልጊዜ ነቅቶ እንዲቆይ ማድረግ
    bot.infinity_polling()
