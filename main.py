import json
import os
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
import logging
from flask import Flask
from threading import Thread

# ==================== FLASK ====================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Statix AI ishlayapti!"

@app.route('/ping')
def ping():
    return "PONG"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ==================== LOGGING ====================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== SOZLAMALAR ====================
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8306167935:AAEF7hOLTrDcXLLaUVQ8sGNVlw6ipJPt2Rs')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '8306639956'))
CARD = "4916 9903 1619 3280"
PRO_PRICE = "30.000 so'm"
AD_COST = 5
ADMIN_BALLS = 999999
DATA_FILE = "/tmp/data.json"

# ==================== TIL ====================
L = {
    "uz": {
        "start": "🤖 <b>STATIX AI</b>\n👋 {name}\n\n💎 {balls} ball | ⭐ {plan}\n\n📌 /add @kanal | /mychannels | /balls | /admin",
        "main": "🏠 Menyu", "add_ch": "➕ Kanal", "my_ch": "📋 Kanallar", "ad": "📢 Reklama",
        "set": "🌐 Til", "ai": "🤖 AI", "top": "🏆 TOP", "exp": "📤 Eksport",
        "sch": "📅 Reja", "goal": "🎯 Maqsad", "fb": "💬 Fikr", "help": "❓ Yordam",
        "back": "🔙", "del": "🗑", "check": "⏳ Tekshirilmoqda...",
        "no_admin": "❌ Bot admin emas!", "added": "✅ {title}\n👥 {members:,}\n💰 ~{price:,} so'm",
        "no_ch": "📭 Kanallar yo'q", "stats": "📊 {title}\n👥 {members:,} | 7kun: {week}\n✅ +{joined} ❌ -{left}\n💰 ~{price:,} so'm",
        "ad_menu": "📢 Reklama\n💎 {balls} | Narxi: {cost}\nOlish: {status}",
        "ad_ON": "✅ ON", "ad_OFF": "❌ OFF",
        "ad_send": "📤 Yuboring ({cost} ball):", "ad_sent": "✅ {count} kishiga!\n💎 Qoldi: {balls}",
        "ad_got": "💎 +1 ball! Jami: {balls}", "low": "❌ {balls}/{cost}",
        "ball": "💎 {balls} ball", "pro": "⭐ PRO — {price}\n💳 <code>{card}</code>",
        "pay": "💳 To'lov qildim", "pay_ok": "✅ Chek yuborildi!",
        "pro_ok": "🎉 PRO aktiv!", "fb_ok": "✅ Rahmat!",
        "ai_ask": "🤖 So'rang: o'stirish/narx/reklama",
        "lang_ok": "✅ Til: {lang}", "del_ask": "⚠️ O'chirilsinmi?", "del_ok": "✅ O'chirildi!",
        "goal_ask": "🎯 Necha a'zo? <code>5000</code>", "goal_set": "🎯 Maqsad: {target:,} a'zo",
        "sch_time": "📅 Vaqt (HH:MM):", "sch_text": "📝 Matn:", "sch_done": "✅ Rejalashtirildi!",
        "exp_ok": "✅ Eksport yuborildi!", "err": "❌ Xatolik",
        "notify_on": "🔔 Bildirish: ✅", "notify_off": "🔔 Bildirish: ❌",
    },
    "ru": {
        "start": "🤖 <b>STATIX AI</b>\n👋 {name}\n\n💎 {balls} | ⭐ {plan}\n\n📌 /add @канал | /mychannels | /balls | /admin",
        "main": "🏠 Меню", "add_ch": "➕ Канал", "my_ch": "📋 Каналы", "ad": "📢 Реклама",
        "set": "🌐 Язык", "ai": "🤖 AI", "top": "🏆 ТОП", "exp": "📤 Экспорт",
        "sch": "📅 План", "goal": "🎯 Цель", "fb": "💬 Отзыв", "help": "❓ Помощь",
        "back": "🔙", "del": "🗑", "check": "⏳ Проверка...",
        "no_admin": "❌ Бот не админ!", "added": "✅ {title}\n👥 {members:,}",
        "no_ch": "📭 Нет", "stats": "📊 {title}\n👥 {members:,} | 7д: {week}\n💰 ~{price:,} сум",
        "ad_menu": "📢 Реклама\n💎 {balls} | Цена: {cost}\nПрием: {status}",
        "ad_ON": "✅ ВКЛ", "ad_OFF": "❌ ВЫКЛ",
        "ad_send": "📤 Отправьте ({cost}):", "ad_sent": "✅ {count} людям!\n💎 {balls}",
        "ad_got": "💎 +1 балл! {balls}", "low": "❌ {balls}/{cost}",
        "ball": "💎 {balls}", "pro": "⭐ PRO — {price}\n💳 <code>{card}</code>",
        "pay": "💳 Оплатил", "pay_ok": "✅ Чек отправлен!",
        "pro_ok": "🎉 PRO актив!", "fb_ok": "✅ Спасибо!",
        "ai_ask": "🤖 рост/цена/реклама",
        "lang_ok": "✅ Язык: {lang}", "del_ask": "⚠️ Удалить?", "del_ok": "✅ Удалено!",
        "goal_ask": "🎯 Сколько? <code>5000</code>", "goal_set": "🎯 Цель: {target:,}",
        "sch_time": "📅 Время:", "sch_text": "📝 Текст:", "sch_done": "✅ Запланировано!",
        "exp_ok": "✅ Экспорт отправлен!", "err": "❌ Ошибка",
        "notify_on": "🔔 Увед: ✅", "notify_off": "🔔 Увед: ❌",
    },
    "en": {
        "start": "🤖 <b>STATIX AI</b>\n👋 {name}\n\n💎 {balls} | ⭐ {plan}\n\n📌 /add @channel | /mychannels | /balls | /admin",
        "main": "🏠 Menu", "add_ch": "➕ Channel", "my_ch": "📋 Channels", "ad": "📢 Ads",
        "set": "🌐 Language", "ai": "🤖 AI", "top": "🏆 TOP", "exp": "📤 Export",
        "sch": "📅 Schedule", "goal": "🎯 Goal", "fb": "💬 Feedback", "help": "❓ Help",
        "back": "🔙", "del": "🗑", "check": "⏳ Checking...",
        "no_admin": "❌ Bot not admin!", "added": "✅ {title}\n👥 {members:,}",
        "no_ch": "📭 None", "stats": "📊 {title}\n👥 {members:,} | 7d: {week}\n💰 ~{price:,} sum",
        "ad_menu": "📢 Ads\n💎 {balls} | Cost: {cost}\nReceive: {status}",
        "ad_ON": "✅ ON", "ad_OFF": "❌ OFF",
        "ad_send": "📤 Send ({cost}):", "ad_sent": "✅ {count} people!\n💎 {balls}",
        "ad_got": "💎 +1 ball! {balls}", "low": "❌ {balls}/{cost}",
        "ball": "💎 {balls}", "pro": "⭐ PRO — {price}\n💳 <code>{card}</code>",
        "pay": "💳 I paid", "pay_ok": "✅ Sent!",
        "pro_ok": "🎉 PRO active!", "fb_ok": "✅ Thanks!",
        "ai_ask": "🤖 growth/price/ads",
        "lang_ok": "✅ Language: {lang}", "del_ask": "⚠️ Delete?", "del_ok": "✅ Deleted!",
        "goal_ask": "🎯 How many? <code>5000</code>", "goal_set": "🎯 Goal: {target:,}",
        "sch_time": "📅 Time:", "sch_text": "📝 Text:", "sch_done": "✅ Scheduled!",
        "exp_ok": "✅ Export sent!", "err": "❌ Error",
        "notify_on": "🔔 Notify: ✅", "notify_off": "🔔 Notify: ❌",
    }
}

# ==================== DATABASE ====================
class DB:
    def __init__(self):
        self.d = {"ch": {}, "pro": [], "balls": {}, "ads": {}, "lang": {}, "goals": {}, "sch": [], "fb": [], "notify": {}}
        self.load()
        self.d["balls"][str(ADMIN_ID)] = ADMIN_BALLS
        self.save()
    
    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE) as f: self.d.update(json.load(f))
            except: pass
    
    def save(self):
        with open(DATA_FILE, 'w') as f: json.dump(self.d, f, ensure_ascii=False)
    
    def b(self, uid): return self.d["balls"].get(str(uid), 0)
    def ab(self, uid, a): self.d["balls"][str(uid)] = self.b(uid) + a; self.save()
    def sb(self, uid, a):
        if self.b(uid) >= a: self.ab(uid, -a); return True
        return False
    
    def ad(self, uid): return self.d["ads"].get(str(uid), False)
    def tad(self, uid): self.d["ads"][str(uid)] = not self.ad(uid); self.save(); return self.ad(uid)
    def ad_all(self): return [u for u, e in self.d["ads"].items() if e]
    
    def l(self, uid): return self.d["lang"].get(str(uid), "uz")
    def sl(self, uid, lang): self.d["lang"][str(uid)] = lang; self.save()
    
    def pro(self, uid): return str(uid) in self.d["pro"]
    def apro(self, uid):
        uid = str(uid)
        if uid not in self.d["pro"]: self.d["pro"].append(uid); self.save(); return True
        return False
    
    def notify(self, uid): return self.d["notify"].get(str(uid), False)
    def tnotify(self, uid): self.d["notify"][str(uid)] = not self.notify(uid); self.save(); return self.notify(uid)
    
    def add_ch(self, uid, cid, title, username, members):
        uid, cid = str(uid), str(cid)
        self.d["ch"].setdefault(uid, [])
        for c in self.d["ch"][uid]:
            if c["id"] == cid: return False
        self.d["ch"][uid].append({
            "id": cid, "title": title, "username": username, "member_count": members,
            "changes": [], "top": [],
            "stats": {"wj": 0, "wl": 0, "msg": 0, "fw": 0, "likes": 0}
        })
        self.save(); return True
    
    def rm_ch(self, uid, cid):
        uid, cid = str(uid), str(cid)
        if uid in self.d["ch"]:
            self.d["ch"][uid] = [c for c in self.d["ch"][uid] if c["id"] != cid]
            self.save(); return True
        return False
    
    def add_cng(self, cid, ct, desc, views=0, fw=0):
        for chs in self.d["ch"].values():
            for c in chs:
                if c["id"] == str(cid):
                    c["changes"].append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": ct, "text": desc, "views": views, "fw": fw
                    })
                    c["stats"]["msg"] += 1
                    if views > 0:
                        c["top"].append({"text": desc[:50], "views": views})
                        c["top"] = sorted(c["top"], key=lambda x: x["views"], reverse=True)[:10]
                    if fw > 0: c["stats"]["fw"] += fw
                    if len(c["changes"]) > 100: c["changes"] = c["changes"][-100:]
                    self.save(); return True
        return False
    
    def umc(self, cid, nc):
        for chs in self.d["ch"].values():
            for c in chs:
                if c["id"] == str(cid):
                    old = c["member_count"]; c["member_count"] = nc
                    if nc > old: c["stats"]["wj"] += (nc - old)
                    elif nc < old: c["stats"]["wl"] += (old - nc)
                    self.save(); return True
        return False
    
    def chs(self, uid): return self.d["ch"].get(str(uid), [])
    def ch(self, cid):
        for chs in self.d["ch"].values():
            for c in chs:
                if c["id"] == str(cid): return c
        return None
    
    def set_goal(self, uid, cid, target):
        self.d["goals"][f"{uid}_{cid}"] = {"target": target}
        self.save()
    
    def goal(self, uid, cid): return self.d["goals"].get(f"{uid}_{cid}")
    
    def add_sch(self, uid, cid, text, time_str):
        self.d["sch"].append({"uid": str(uid), "cid": str(cid), "text": text, "time": time_str})
        self.save()
    
    def add_fb(self, uid, text):
        self.d["fb"].append({"uid": str(uid), "text": text})
        self.save()
    
    def price(self, members):
        base = members * 50
        if members > 10000: base = members * 80
        elif members > 5000: base = members * 65
        elif members > 1000: base = members * 55
        return {"min": int(base*0.8), "avg": int(base), "max": int(base*1.2)}
    
    def admin_stats(self):
        return {
            "users": len(self.d.get("ch", {})),
            "pro": len(self.d.get("pro", [])),
            "channels": sum(len(chs) for chs in self.d.get("ch", {}).values()),
            "fb_count": len(self.d.get("fb", []))
        }

db = DB()

# ==================== YORDAMCHI ====================
def t(uid, key, **kw):
    lang = db.l(uid)
    text = L.get(lang, L["uz"]).get(key, key)
    return text.format(**kw) if kw else text

# ==================== MENYU ====================
def menu(uid):
    lang = db.l(uid); pro = db.pro(uid); balls = db.b(uid); notify = db.notify(uid)
    kb = [
        [InlineKeyboardButton(L[lang]["add_ch"], callback_data="add")],
        [InlineKeyboardButton(L[lang]["my_ch"], callback_data="mylist")],
        [InlineKeyboardButton(L[lang]["ad"], callback_data="ad_menu")],
        [InlineKeyboardButton(L[lang]["set"], callback_data="settings")],
    ]
    if pro:
        kb.append([InlineKeyboardButton(L[lang]["ai"], callback_data="ai_chat")])
        kb.append([InlineKeyboardButton(L[lang]["top"], callback_data="top_posts")])
        kb.append([InlineKeyboardButton(L[lang]["exp"], callback_data="export")])
        kb.append([InlineKeyboardButton(L[lang]["sch"], callback_data="schedule")])
        kb.append([InlineKeyboardButton(L[lang]["goal"], callback_data="goal_menu")])
        kb.append([InlineKeyboardButton(L[lang]["notify_on"] if notify else L[lang]["notify_off"], callback_data="toggle_notify")])
    else:
        kb.append([InlineKeyboardButton(f"⭐ PRO - {PRO_PRICE}", callback_data="pro_info")])
    kb.append([InlineKeyboardButton(L[lang]["fb"], callback_data="feedback")])
    kb.append([InlineKeyboardButton(L[lang]["ball"].format(balls=balls), callback_data="balls_info")])
    kb.append([InlineKeyboardButton(L[lang]["help"], callback_data="help")])
    return InlineKeyboardMarkup(kb)

# ==================== HANDLERLAR ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user; uid = user.id
    text = t(uid, "start", name=user.first_name, balls=db.b(uid), plan="PRO" if db.pro(uid) else "FREE")
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=menu(uid))

async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not context.args: await update.message.reply_text("📌 /add @username", parse_mode='HTML'); return
    ci = context.args[0]; msg = await update.message.reply_text(t(uid, "check"))
    try:
        chat = await context.bot.get_chat(ci)
        if (await chat.get_member(context.bot.id)).status not in ['administrator', 'creator']:
            await msg.edit_text(t(uid, "no_admin"), parse_mode='HTML'); return
        members = await chat.get_member_count()
        if db.add_ch(uid, chat.id, chat.title, chat.username or "", members):
            p = db.price(members)
            await msg.edit_text(t(uid, "added", title=chat.title, members=members, price=p['avg']), parse_mode='HTML')
        else: await msg.edit_text("⚠️ Allaqachon qo'shilgan!")
    except Exception as e: await msg.edit_text(t(uid, "err"))

async def my_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id; chs = db.chs(uid)
    if not chs: await update.message.reply_text(t(uid, "no_ch")); return
    text = "📋 <b>Kanallarim:</b>\n\n"; kb = []
    for c in chs:
        text += f"📢 {c['title']} | 👥 {c.get('member_count',0):,}\n"
        kb.append([InlineKeyboardButton(f"📊 {c['title'][:20]}", callback_data=f"stats_{c['id']}"),
                   InlineKeyboardButton(t(uid, "del"), callback_data=f"delete_{c['id']}")])
    kb.append([InlineKeyboardButton(t(uid, "back"), callback_data="main_menu")])
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))

async def channel_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    c = db.ch(q.data.replace("stats_", ""))
    if not c: return
    s = c["stats"]; m = c["member_count"]; chs = c["changes"]
    w = len([x for x in chs if datetime.strptime(x["date"],"%Y-%m-%d") > datetime.now()-timedelta(days=7)])
    p = db.price(m)
    goal = db.goal(uid, c['id'])
    gt = f"\n🎯 Maqsad: {goal['target']:,}" if goal else ""
    text = t(uid, "stats", title=c['title'], members=m, week=w, joined=s['wj'], left=s['wl'], price=p['avg']) + gt
    for x in chs[-5:]:
        em = {'new_message':'📝','photo':'🖼','new_member':'✅','left_member':'❌'}.get(x['type'],'📌')
        text += f"\n{em} {x['text'][:60]}"
    kb = [[InlineKeyboardButton(t(uid,"back"), callback_data="mylist")]]
    await q.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))

# ==================== REKLAMA ====================
async def ad_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    ad = db.ad(uid); balls = db.b(uid)
    text = t(uid, "ad_menu", balls=balls, cost=AD_COST, status=t(uid,"ad_ON") if ad else t(uid,"ad_OFF"))
    kb = [
        [InlineKeyboardButton(f"📢 Olish: {'✅' if ad else '❌'}", callback_data="ad_toggle")],
        [InlineKeyboardButton(f"📤 Berish ({AD_COST} ball)", callback_data="ad_send")],
        [InlineKeyboardButton(t(uid,"back"), callback_data="main_menu")]
    ]
    await q.edit_message_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))

async def ad_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    status = db.tad(uid)
    await q.answer("✅ Yoqildi!" if status else "❌ O'chirildi!", show_alert=True)
    await ad_menu_handler(update, context)

async def ad_send_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    if db.b(uid) < AD_COST:
        await q.answer(t(uid,"low",balls=db.b(uid),cost=AD_COST), show_alert=True); return
    context.user_data['sending_ad'] = True
    await q.edit_message_text(t(uid,"ad_send",cost=AD_COST), parse_mode='HTML')

async def handle_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('sending_ad'): return
    user = update.effective_user; uid = user.id; msg = update.message
    if not db.sb(uid, AD_COST):
        await update.message.reply_text(t(uid,"low",balls=db.b(uid),cost=AD_COST)); context.user_data['sending_ad']=False; return
    
    users = db.ad_all(); hdr = "📢 <b>REKLAMA</b>\n\n"; ftr = f"\n\n— @{user.username or user.first_name}"
    sent = 0
    for tuid in users:
        if tuid == str(uid): continue
        try:
            if msg.text: await context.bot.send_message(int(tuid), hdr+msg.text+ftr, parse_mode='HTML')
            elif msg.photo: await context.bot.send_photo(int(tuid), msg.photo[-1].file_id, caption=hdr+(msg.caption or "")+ftr, parse_mode='HTML')
            db.ab(tuid, 1)
            sent += 1; await asyncio.sleep(0.3)
        except: pass
    await update.message.reply_text(t(uid,"ad_sent",count=sent,balls=db.b(uid)), parse_mode='HTML')
    context.user_data['sending_ad'] = False

# ==================== AI ====================
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    if not db.pro(q.from_user.id): await q.answer("❌ PRO kerak!", show_alert=True); return
    context.user_data['ai_mode'] = True
    await q.edit_message_text(t(q.from_user.id,"ai_ask"), parse_mode='HTML')

async def ai_resp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('ai_mode'): return
    m = update.message.text.lower()
    r = "🤖 So'rang: o'stirish, narx, reklama"
    if "o's" in m: r = "📈 Kuniga 3-5 post, reklama, giveaway"
    elif "narx" in m: r = "💰 1 a'zo ≈ 50-80 so'm"
    elif "reklama" in m: r = "📢 Target reklama eng samarali"
    await update.message.reply_text(r)

# ==================== TOP POSTLAR ====================
async def top_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    chs = db.chs(uid); all_posts = []
    for c in chs:
        for p in c.get("top", []): p["channel"] = c['title']; all_posts.append(p)
    all_posts = sorted(all_posts, key=lambda x: x.get("views",0), reverse=True)[:10]
    text = "🏆 <b>TOP Postlar</b>\n\n"
    if all_posts:
        for i, p in enumerate(all_posts, 1): text += f"{i}. 👁 {p['views']} | {p['text'][:40]}\n"
    else: text = "📭 Hali post yo'q"
    await q.edit_message_text(text, parse_mode='HTML')

# ==================== EKSPORT ====================
async def export_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    chs = db.chs(uid)
    if not chs: await q.edit_message_text("📭"); return
    text = "📤 Statistika\n\n"
    for c in chs: text += f"{c['title']}: {c.get('member_count',0):,} a'zo\n"
    fname = f"/tmp/export_{uid}.txt"
    with open(fname, 'w') as f: f.write(text)
    try:
        with open(fname, 'rb') as f: await context.bot.send_document(uid, f, filename="statistika.txt")
        await q.edit_message_text(t(uid,"exp_ok"))
    except: pass
    if os.path.exists(fname): os.remove(fname)

# ==================== REJALASHTIRISH ====================
async def schedule_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    chs = db.chs(uid)
    if not chs: await q.edit_message_text("📭"); return
    kb = [[InlineKeyboardButton(c['title'][:30], callback_data=f"sch_{c['id']}")] for c in chs]
    kb.append([InlineKeyboardButton(t(uid,"back"), callback_data="main_menu")])
    await q.edit_message_text("📅 Kanalni tanlang:", reply_markup=InlineKeyboardMarkup(kb))

async def schedule_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    context.user_data['sch_cid'] = q.data.replace("sch_","")
    context.user_data['scheduling'] = 'time'
    await q.edit_message_text(t(uid,"sch_time"), parse_mode='HTML')

async def schedule_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if context.user_data.get('scheduling') == 'time':
        context.user_data['sch_time'] = update.message.text.strip()
        context.user_data['scheduling'] = 'text'
        await update.message.reply_text(t(uid,"sch_text"))
    elif context.user_data.get('scheduling') == 'text':
        db.add_sch(uid, context.user_data['sch_cid'], update.message.text, context.user_data['sch_time'])
        await update.message.reply_text(t(uid,"sch_done"))
        context.user_data['scheduling'] = None

# ==================== MAQSAD ====================
async def goal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    chs = db.chs(uid)
    if not chs: await q.edit_message_text("📭"); return
    kb = [[InlineKeyboardButton(c['title'][:30], callback_data=f"goal_{c['id']}")] for c in chs]
    kb.append([InlineKeyboardButton(t(uid,"back"), callback_data="main_menu")])
    await q.edit_message_text("🎯 Kanalni tanlang:", reply_markup=InlineKeyboardMarkup(kb))

async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    context.user_data['goal_cid'] = q.data.replace("goal_","")
    context.user_data['setting_goal'] = True
    await q.edit_message_text(t(uid,"goal_ask"), parse_mode='HTML')

async def goal_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('setting_goal'): return
    uid = update.effective_user.id
    try:
        target = int(update.message.text.strip())
        db.set_goal(uid, context.user_data['goal_cid'], target)
        await update.message.reply_text(t(uid,"goal_set",target=target), parse_mode='HTML')
        context.user_data['setting_goal'] = False
    except: await update.message.reply_text("❌ Raqam kiriting!")

# ==================== FEEDBACK ====================
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    context.user_data['giving_fb'] = True
    await q.edit_message_text("💬 Fikringizni yozing:")

async def fb_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('giving_fb'): return
    uid = update.effective_user.id
    db.add_fb(uid, update.message.text)
    await update.message.reply_text(t(uid,"fb_ok"))
    context.user_data['giving_fb'] = False

# ==================== PRO ====================
async def pro_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    kb = [[InlineKeyboardButton(t(uid,"pay"), callback_data="payment")],[InlineKeyboardButton(t(uid,"back"), callback_data="main_menu")]]
    await q.edit_message_text(t(uid,"pro",price=PRO_PRICE,card=CARD), parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    context.user_data['waiting_check'] = True
    await q.edit_message_text("📸 Chek rasmini yuboring:")

async def handle_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('waiting_check'): return
    user = update.effective_user; photo = update.message.photo[-1]
    kb = [[InlineKeyboardButton("✅", callback_data=f"app_{user.id}"), InlineKeyboardButton("❌", callback_data=f"rej_{user.id}")]]
    await context.bot.send_photo(ADMIN_ID, photo.file_id, f"PRO so'rov\n👤 {user.first_name}\n🆔 {user.id}", reply_markup=InlineKeyboardMarkup(kb))
    await update.message.reply_text(t(user.id,"pay_ok"))
    context.user_data['waiting_check'] = False

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if q.from_user.id != ADMIN_ID: return
    await q.answer(); uid = q.data.replace("app_","")
    db.apro(uid)
    try: await context.bot.send_message(int(uid), t(int(uid),"pro_ok"), parse_mode='HTML')
    except: pass
    await q.edit_message_caption(caption=f"{q.message.caption}\n\n✅ TASDIQLANDI!", parse_mode='HTML')

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    if q.from_user.id != ADMIN_ID: return
    await q.answer()
    await q.edit_message_caption(caption=f"{q.message.caption}\n\n❌ RAD", parse_mode='HTML')

# ==================== BILDIRISH ====================
async def toggle_notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    status = db.tnotify(uid)
    await q.edit_message_text(t(uid,"notify_on") if status else t(uid,"notify_off"), reply_markup=menu(uid))

# ==================== TIL ====================
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    kb = [
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"), InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(t(uid,"back"), callback_data="main_menu")]
    ]
    await q.edit_message_text("🌐 Til tanlang:", reply_markup=InlineKeyboardMarkup(kb))

async def change_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    lang = q.data.replace("lang_",""); db.sl(q.from_user.id, lang)
    await q.edit_message_text(t(q.from_user.id,"lang_ok",lang=lang.upper()), reply_markup=menu(q.from_user.id))

# ==================== BALLS ====================
async def balls_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); uid = q.from_user.id
    await q.edit_message_text(t(uid,"ball",balls=db.b(uid)), parse_mode='HTML')

async def balls_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💎 {db.b(update.effective_user.id)} ball")

# ==================== ADMIN ====================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    s = db.admin_stats()
    await update.message.reply_text(f"👑 Admin\n👥 {s['users']} | ⭐ {s['pro']} | 📢 {s['channels']}", parse_mode='HTML')

# ==================== KANAL MONITORING ====================
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.channel_post
    if not msg: return
    cid = str(msg.chat.id); views = getattr(msg,'views',0) or 0
    fw = 1 if (msg.forward_from_chat or msg.forward_from_message_id) else 0
    if msg.text: desc, ct = f"Matn: {msg.text[:100]}", 'new_message'
    elif msg.photo: desc, ct = "Rasm", 'photo'
    elif msg.video: desc, ct = "Video", 'video'
    else: desc, ct = f"#{msg.message_id}", 'new_message'
    db.add_cng(cid, ct, desc, views, fw)

async def member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cm = update.chat_member; cid = str(cm.chat.id); user = cm.new_chat_member.user
    old, new = cm.old_chat_member.status, cm.new_chat_member.status
    name = user.first_name + (f" (@{user.username})" if user.username else "")
    if new == 'member' and old not in ['member','administrator','creator']:
        db.add_cng(cid, 'new_member', f"{name} qo'shildi")
        try: db.umc(cid, await cm.chat.get_member_count())
        except: pass
    elif new in ['left','kicked'] and old == 'member':
        db.add_cng(cid, 'left_member', f"{name} chiqdi")
        try: db.umc(cid, await cm.chat.get_member_count())
        except: pass

# ==================== BUTTON ====================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer(); d = q.data; uid = q.from_user.id
    
    if d == "add": await q.edit_message_text("📌 /add @username", parse_mode='HTML')
    elif d == "mylist": await my_channels(update, context)
    elif d.startswith("stats_"): await channel_stats(update, context)
    elif d.startswith("delete_"):
        cid = d.replace("delete_","")
        kb = [[InlineKeyboardButton("✅ Ha", callback_data=f"confirm_delete_{cid}"), InlineKeyboardButton("❌ Yo'q", callback_data="mylist")]]
        await q.edit_message_text(t(uid,"del_ask"), reply_markup=InlineKeyboardMarkup(kb))
    elif d.startswith("confirm_delete_"):
        if db.rm_ch(uid, d.replace("confirm_delete_","")): await q.edit_message_text(t(uid,"del_ok"))
    elif d == "ad_menu": await ad_menu_handler(update, context)
    elif d == "ad_toggle": await ad_toggle(update, context)
    elif d == "ad_send": await ad_send_prompt(update, context)
    elif d == "balls_info": await balls_info(update, context)
    elif d == "pro_info": await pro_info(update, context)
    elif d == "payment": await payment(update, context)
    elif d.startswith("app_"): await approve(update, context)
    elif d.startswith("rej_"): await reject(update, context)
    elif d == "ai_chat": await ai_chat(update, context)
    elif d == "top_posts": await top_posts(update, context)
    elif d == "export": await export_stats(update, context)
    elif d == "schedule": await schedule_menu(update, context)
    elif d.startswith("sch_"): await schedule_channel(update, context)
    elif d == "goal_menu": await goal_menu(update, context)
    elif d.startswith("goal_"): await set_goal(update, context)
    elif d == "toggle_notify": await toggle_notify(update, context)
    elif d == "feedback": await feedback(update, context)
    elif d == "settings": await settings(update, context)
    elif d.startswith("lang_"): await change_lang(update, context)
    elif d == "help": await q.edit_message_text("❓ /start /add /mychannels /balls /admin")
    elif d == "main_menu": await q.edit_message_text(t(uid,"main"), reply_markup=menu(uid))

# ==================== MAIN ====================
def main():
    Thread(target=run_flask).start()
    print("🤖 STATIX AI ishga tushmoqda...")
    
    app_bot = Application.builder().token(BOT_TOKEN).build()
    
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("add", add_channel))
    app_bot.add_handler(CommandHandler("mychannels", my_channels))
    app_bot.add_handler(CommandHandler("balls", balls_cmd))
    app_bot.add_handler(CommandHandler("admin", admin_panel))
    app_bot.add_handler(CommandHandler("help", start))
    
    app_bot.add_handler(MessageHandler(filters.PHOTO & ~filters.ChatType.CHANNEL, handle_check))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.ChatType.CHANNEL, handle_ad))
    app_bot.add_handler(MessageHandler(filters.PHOTO & ~filters.ChatType.CHANNEL, handle_ad))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.ChatType.CHANNEL, ai_resp))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.ChatType.CHANNEL, schedule_text_handler))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.ChatType.CHANNEL, goal_number))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.ChatType.CHANNEL, fb_text))
    
    app_bot.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post))
    app_bot.add_handler(ChatMemberHandler(member_update, ChatMemberHandler.CHAT_MEMBER))
    app_bot.add_handler(CallbackQueryHandler(button))
    
    print("✅ Bot ishga tushdi!")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()