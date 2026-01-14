import streamlit as st
import random
import base64

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Amazon Jungle Adventure",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# DARK THEME + ANIMATION CSS
# =====================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0e1117;
    color: #e6e6e6;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #4ade80;
    text-align: center;
}
.card {
    background: #161b22;
    padding: 1rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 14px rgba(0,0,0,0.6);
}
.stButton button {
    width: 100%;
    height: 3.2rem;
    border-radius: 14px;
    font-size: 1.05rem;
    font-weight: 600;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: black;
    border: none;
}
[data-testid="metric-container"] {
    background: #161b22;
    border-radius: 14px;
    padding: 0.6rem;
}
.map-cell {
    text-align: center;
    font-size: 1.8rem;
}
.log {
    background: #020617;
    padding: 0.6rem;
    border-radius: 10px;
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}

/* ===== Animations ===== */
@keyframes shake {
  0% { transform: translate(0); }
  25% { transform: translate(-5px,0); }
  50% { transform: translate(5px,0); }
  75% { transform: translate(-5px,0); }
  100% { transform: translate(0); }
}
@keyframes flash-red {
  0% { background-color: #7f1d1d; }
  100% { background-color: #161b22; }
}
@keyframes glow-green {
  0% { box-shadow: 0 0 12px #22c55e; }
  100% { box-shadow: none; }
}
.anim-attack { animation: shake 0.3s, flash-red 0.3s; }
.anim-defend { animation: glow-green 0.4s; }
.anim-win { animation: glow-green 0.8s; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================
st.title("🌴 Amazon Jungle Adventure")
st.caption("Dark UI • Mobile Ready • RPG Survival")

# =====================================================
# INIT GAME
# =====================================================
def init_game():
    st.session_state.update({
        "mode": "explore",
        "hp": 100,
        "max_hp": 100,
        "food": 60,
        "water": 60,
        "gold": 0,
        "day": 1,
        "level": 1,
        "exp": 0,
        "skill_combat": 0,
        "skill_survival": 0,
        "skill_explore": 0,
        "x": 1,
        "y": 1,
        "enemy_name": "",
        "enemy_hp": 0,
        "enemy_max_hp": 0,
        "anim": "",
        "log": [],
        "music_on": False
    })

if "hp" not in st.session_state:
    init_game()

def log(txt):
    st.session_state.log.insert(0, f"🗓 Ngày {st.session_state.day}: {txt}")

# =====================================================
# BACKGROUND MUSIC
# =====================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎵 Âm thanh")

c1, c2 = st.columns(2)
if c1.button("🔊 Bật nhạc"):
    st.session_state.music_on = True
if c2.button("🔇 Tắt nhạc"):
    st.session_state.music_on = False

if st.session_state.music_on:
    try:
        with open("jungle.mp3", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <audio autoplay loop>
            <source src="data:audio/mp3;base64,{data}">
            </audio>
            """,
            unsafe_allow_html=True
        )
    except:
        st.warning("⚠️ Không tìm thấy jungle.mp3")
st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# GAME OVER
# =====================================================
if st.session_state.hp <= 0:
    st.error("💀 Bạn đã bỏ mạng trong rừng Amazon!")
    st.write(f"⭐ Level: {st.session_state.level}")
    st.write(f"💰 Vàng: {st.session_state.gold}")
    if st.button("🔄 Chơi lại"):
        st.session_state.clear()
    st.stop()

# =====================================================
# STATUS
# =====================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("❤️ HP", f"{st.session_state.hp}/{st.session_state.max_hp}")
c2.metric("🍖 Food", st.session_state.food)
c3.metric("💧 Water", st.session_state.water)

c4, c5, c6 = st.columns(3)
c4.metric("⭐ Lv", st.session_state.level)
c5.metric("🧠 EXP", st.session_state.exp)
c6.metric("💰 Gold", st.session_state.gold)
st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# COMBAT SCREEN
# =====================================================
if st.session_state.mode == "combat":
    anim = st.session_state.anim
    anim_class = (
        "anim-attack" if anim == "attack"
        else "anim-defend" if anim == "defend"
        else "anim-win" if anim == "win"
        else ""
    )

    st.markdown(f"<div class='card {anim_class}'>", unsafe_allow_html=True)
    st.subheader("⚔️ Chiến đấu!")

    st.progress(st.session_state.hp / st.session_state.max_hp, text="❤️ HP của bạn")
    st.progress(
        st.session_state.enemy_hp / st.session_state.enemy_max_hp,
        text=f"{st.session_state.enemy_name}"
    )

    a1, a2, a3 = st.columns(3)

    if a1.button("⚔️ Đánh"):
        dmg = random.randint(15, 30) + st.session_state.skill_combat * 4
        st.session_state.enemy_hp -= dmg
        st.session_state.anim = "attack"
        log(f"Bạn đánh {st.session_state.enemy_name} (-{dmg})")

    if a2.button("🛡 Phòng thủ"):
        dmg = random.randint(5, 10)
        st.session_state.hp -= dmg
        st.session_state.anim = "defend"
        log("Bạn phòng thủ")

    if a3.button("🏃 Chạy"):
        if random.random() < 0.5:
            log("Chạy thoát!")
            st.session_state.mode = "explore"
        else:
            dmg = random.randint(10, 15)
            st.session_state.hp -= dmg
            log("Không chạy kịp!")

    if st.session_state.enemy_hp > 0:
        edmg = random.randint(8, 18)
        st.session_state.hp -= edmg
        log(f"{st.session_state.enemy_name} phản công (-{edmg})")

    if st.session_state.enemy_hp <= 0:
        st.session_state.gold += 30
        st.session_state.exp += 25
        st.session_state.anim = "win"
        st.session_state.mode = "explore"
        log("🎉 Chiến thắng!")

    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.anim = ""
    st.stop()

# =====================================================
# MAP
# =====================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🗺 Bản đồ")
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        icon = "🧍‍♂️" if (i, j) == (st.session_state.x, st.session_state.y) else "🌲"
        cols[j].markdown(f"<div class='map-cell'>{icon}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# MOVE & EXPLORE
# =====================================================
def start_combat():
    st.session_state.mode = "combat"
    st.session_state.enemy_name = random.choice(["🐍 Rắn độc", "🐗 Lợn rừng", "🕷 Nhện khổng lồ"])
    st.session_state.enemy_max_hp = random.randint(40, 70)
    st.session_state.enemy_hp = st.session_state.enemy_max_hp
    log(f"Gặp {st.session_state.enemy_name}")

def explore():
    r = random.randint(1, 100)
    if r <= 30:
        start_combat()
    elif r <= 55:
        g = random.randint(15, 40)
        st.session_state.gold += g
        log(f"Tìm thấy {g} vàng")
    elif r <= 70:
        skill = random.choice(["skill_combat", "skill_survival", "skill_explore"])
        st.session_state[skill] += 1
        log("Học được kỹ năng mới")
    else:
        log("Rừng yên tĩnh")

def move(dx, dy):
    nx, ny = st.session_state.x + dx, st.session_state.y + dy
    if 0 <= nx <= 2 and 0 <= ny <= 2:
        st.session_state.x, st.session_state.y = nx, ny
        st.session_state.day += 1
        st.session_state.food -= 5
        st.session_state.water -= 5
        explore()

# =====================================================
# D-PAD
# =====================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧭 Di chuyển")

up = st.button("⬆️ Bắc")
l, r = st.columns(2)
left = l.button("⬅️ Tây")
right = r.button("➡️ Đông")
down = st.button("⬇️ Nam")

if up: move(-1, 0)
if down: move(1, 0)
if left: move(0, -1)
if right: move(0, 1)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# LEVEL UP
# =====================================================
if st.session_state.exp >= st.session_state.level * 100:
    st.session_state.exp = 0
    st.session_state.level += 1
    st.session_state.max_hp += 20
    st.session_state.hp = st.session_state.max_hp
    log("🎉 LÊN LEVEL!")

# =====================================================
# LOG
# =====================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📜 Nhật ký")
for l in st.session_state.log[:10]:
    st.markdown(f"<div class='log'>{l}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.caption("🌴 Amazon Jungle Adventure – Streamlit Cloud Ready")
