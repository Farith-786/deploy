import streamlit as st
import streamlit.components.v1 as components
import random
import time
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="👶 Welcome Baby Boy 2026 💙",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS - Animations, Gradients, Cute Fonts
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Pacifico&family=Quicksand:wght@400;600&display=swap');

    .main {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 50%, #c2e9fb 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .title-text {
        font-family: 'Fredoka One', cursive;
        font-size: 4.5rem;
        background: linear-gradient(90deg, #ff6b9d, #4a90e2, #50c878, #ffb347);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 5s ease infinite, bounceIn 1.5s;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    @keyframes gradientShift {
        0%,100% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
    }
    @keyframes bounceIn {
        0% {transform: scale(0.3); opacity: 0;}
        50% {transform: scale(1.05); opacity: 1;}
        100% {transform: scale(1);}
    }

    .subtitle-text {
        font-family: 'Pacifico', cursive;
        font-size: 2rem;
        color: #4a90e2;
        text-align: center;
        animation: fadeInUp 2s;
    }
    @keyframes fadeInUp {
        from {opacity: 0; transform: translateY(30px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .welcome-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 20px 40px rgba(74, 144, 226, 0.3);
        border: 3px dashed #ffb6c1;
        text-align: center;
        animation: floatCard 4s ease-in-out infinite;
        margin: 1rem 0;
    }
    @keyframes floatCard {
        0%,100% {transform: translateY(0px);}
        50% {transform: translateY(-10px);}
    }

    .baby-name {
        font-family: 'Fredoka One', cursive;
        font-size: 3.5rem;
        color: #ff6b9d;
        text-shadow: 3px 3px 0 #ffe4ec, 6px 6px 0 rgba(0,0,0,0.1);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%,100% {transform: scale(1);}
        50% {transform: scale(1.05);}
    }

    .wish-box {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #333;
        padding: 1rem;
    }

    .emoji-rain {
        position: fixed;
        top: -50px;
        font-size: 2rem;
        animation: fall linear infinite;
        z-index: 1;
        pointer-events: none;
    }
    @keyframes fall {
        to {transform: translateY(110vh) rotate(360deg);}
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff6b9d, #4a90e2);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-family: 'Fredoka One', cursive;
        transition: all 0.3s;
        box-shadow: 0 10px 25px rgba(255,107,157,0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(74,144,226,0.6);
    }

    .milestone {
        background: linear-gradient(135deg, #fff5f7, #e6f3ff);
        border-left: 6px solid #ff6b9d;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        font-family: 'Quicksand', sans-serif;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# EMOJI RAIN BACKGROUND
# ============================================================
emoji_rain_html = """
<div id="emoji-rain-container"></div>
<script>
const emojis = ['👶','🍼','💙','🎈','⭐','🧸','🎀','☁️','🌈','✨','🍭','🦋'];
const container = document.getElementById('emoji-rain-container');
for (let i = 0; i < 30; i++) {
    const span = document.createElement('span');
    span.innerText = emojis[Math.floor(Math.random()*emojis.length)];
    span.style.position = 'fixed';
    span.style.left = Math.random()*100 + 'vw';
    span.style.top = '-50px';
    span.style.fontSize = (Math.random()*20 + 20) + 'px';
    span.style.animation = `fall ${Math.random()*8+8}s linear infinite`;
    span.style.animationDelay = Math.random()*10 + 's';
    span.style.opacity = 0.7;
    span.style.pointerEvents = 'none';
    span.style.zIndex = '9999';
    container.appendChild(span);
}
const style = document.createElement('style');
style.innerHTML = '@keyframes fall { to { transform: translateY(110vh) rotate(360deg); } }';
document.head.appendChild(style);
</script>
"""
components.html(emoji_rain_html, height=0)

# ============================================================
# BACKGROUND MUSIC (auto-loop, hidden iframe)
# ============================================================
def play_music():
    """Plays a lullaby-style melody via Web Audio API (no external file needed)."""
    music_html = """
    <!DOCTYPE html>
    <html>
    <body>
    <script>
    // Simple lullaby melody using Web Audio API (Twinkle Twinkle + Brahm's style notes)
    let audioCtx = null;
    let playing = false;

    function startMusic() {
        if (playing) return;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        playing = true;
        loopMelody();
    }

    const melody = [
        [523.25, 0.5], [523.25, 0.5], [783.99, 0.5], [783.99, 0.5],
        [880.00, 0.5], [880.00, 0.5], [783.99, 1.0],
        [698.46, 0.5], [698.46, 0.5], [659.25, 0.5], [659.25, 0.5],
        [587.33, 0.5], [587.33, 0.5], [523.25, 1.0],
        [783.99, 0.5], [783.99, 0.5], [698.46, 0.5], [698.46, 0.5],
        [659.25, 0.5], [659.25, 0.5], [587.33, 1.0],
        [783.99, 0.5], [783.99, 0.5], [698.46, 0.5], [698.46, 0.5],
        [659.25, 0.5], [659.25, 0.5], [587.33, 1.0],
        [523.25, 0.5], [523.25, 0.5], [783.99, 0.5], [783.99, 0.5],
        [880.00, 0.5], [880.00, 0.5], [783.99, 1.0],
        [698.46, 0.5], [698.46, 0.5], [659.25, 0.5], [659.25, 0.5],
        [587.33, 0.5], [587.33, 0.5], [523.25, 1.5],
    ];

    function playNote(freq, duration, startTime) {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0, startTime);
        gain.gain.linearRampToValueAtTime(0.15, startTime + 0.05);
        gain.gain.linearRampToValueAtTime(0, startTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(startTime);
        osc.stop(startTime + duration);
    }

    function loopMelody() {
        if (!playing) return;
        let t = audioCtx.currentTime + 0.1;
        let totalDur = 0;
        melody.forEach(([freq, dur]) => {
            playNote(freq, dur * 0.8, t);
            t += dur;
            totalDur += dur;
        });
        setTimeout(() => { if (playing) loopMelody(); }, totalDur * 1000);
    }

    // Autoplay attempt (browsers may require user interaction)
    window.addEventListener('load', () => {
        startMusic();
    });
    document.addEventListener('click', startMusic, { once: true });
    </script>
    </body>
    </html>
    """
    components.html(music_html, height=0)

play_music()

# ============================================================
# CONFETTI + FIREWORKS
# ============================================================
confetti_html = """
<canvas id="fxCanvas" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9998;"></canvas>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<script>
const colors = ['#ff6b9d','#4a90e2','#50c878','#ffb347','#ffd700','#a8edea','#c2e9fb'];

function fireConfetti() {
    confetti({ particleCount: 150, spread: 100, origin: { y: 0.6 }, colors: colors });
    setTimeout(() => confetti({ particleCount: 100, angle: 60, spread: 70, origin: { x: 0 }, colors: colors }), 250);
    setTimeout(() => confetti({ particleCount: 100, angle: 120, spread: 70, origin: { x: 1 }, colors: colors }), 400);
}

function fireworkBurst() {
    const x = Math.random();
    const y = Math.random() * 0.5;
    confetti({
        particleCount: 80,
        startVelocity: 35,
        spread: 360,
        origin: { x: x, y: y },
        colors: colors,
        shapes: ['circle','square'],
        scalar: 1.2
    });
}

fireConfetti();
setInterval(fireworkBurst, 1800);
setInterval(() => fireConfetti(), 6000);
</script>
"""
components.html(confetti_html, height=0)

# ============================================================
# SIDEBAR - Baby Details
# ============================================================
with st.sidebar:
    st.markdown("## 💙 Baby Info")
    baby_name = st.text_input("Baby's Name", value="Baby Boy 2026")
    birth_date = st.date_input("Date of Birth", value=datetime(2026, 1, 1))
    weight = st.text_input("Birth Weight", value="3.5 kg")
    height = st.text_input("Birth Height", value="50 cm")
    parents = st.text_input("Parents", value="Mom & Dad")

    st.markdown("---")
    st.markdown("### 🎵 Music & Effects")
    sound_on = st.checkbox("Background Lullaby", value=True)
    confetti_on = st.checkbox("Confetti & Fireworks", value=True)

    st.markdown("---")
    st.markdown("### 💌 Family Messages")
    st.markdown("Add your own wishes below 👇")
    custom_wish = st.text_area(
        "Your Message",
        value="May your life be filled with love, laughter, and endless blessings! 💙",
    )

# ============================================================
# MAIN HEADER
# ============================================================
st.markdown('<h1 class="title-text">🎉 Welcome to the World! 🎉</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">A Little Miracle Has Arrived in 2026 💙</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# MAIN WELCOME CARD
# ============================================================
st.markdown(f"""
<div class="welcome-card">
    <div style="font-size:5rem; animation: pulse 2s infinite;">👶</div>
    <div class="baby-name">{baby_name}</div>
    <p style="font-family:'Pacifico',cursive; font-size:1.6rem; color:#4a90e2; margin-top:1rem;">
        Born: {birth_date.strftime('%B %d, %Y')}
    </p>
    <hr style="border:none; border-top:2px dashed #ffb6c1; margin:1.5rem auto; width:60%;">
    <div class="wish-box">
        <h2 style="color:#ff6b9d; font-family:'Fredoka One',cursive;">
            ✨ Welcome to the world, little one! ✨
        </h2>
        <p style="font-size:1.4rem;">
            <b>Congratulations on your new baby boy!</b>
        </p>
        <p>
            Your arrival has filled our hearts with immeasurable joy.<br>
            From this day forward, the world has one more dreamer, one more laughter,<br>
            one more beautiful soul to cherish. 🌟
        </p>
        <p style="font-size:1.3rem; color:#4a90e2; font-family:'Pacifico',cursive;">
            — With all our love, {parents} 💙
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# STATS ROW
# ============================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎂 Birth Year", "2026")
with col2:
    st.metric("⚖️ Weight", weight)
with col3:
    st.metric("📏 Height", height)
with col4:
    days = (datetime.now() - datetime.combine(birth_date, datetime.min.time())).days
    st.metric("🌱 Days with Us", max(days, 0))

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS - Wishes, Milestones, Poem, Family Tree
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["💌 Heartfelt Wishes", "📅 Milestones Ahead", "📜 A Poem for You",
     "🌟 Blessings", "🎁 Surprise Button"]
)

with tab1:
    st.markdown("### 💌 Wishes from the Family")
    wishes = [
        ("💙", "Mom", "You are my heart walking outside my body. Welcome, my precious son!"),
        ("💚", "Dad", "I promise to be your hero, your guide, and your biggest fan. Welcome, champ!"),
        ("💖", "Grandma", "My arms have been waiting to hold you. You're already my favorite!"),
        ("💛", "Grandpa", "You've got big shoes to fill — but I know you'll fill them with joy!"),
        ("💜", "Thai Mama", """என் செல்ல மருமகனுக்கு, உன் தாய் மாமனின் அன்புப் பரிசு" ❤️👑

    💙 “மருமகனே…

நீ இந்த உலகத்துக்கு வரும்போது உன் கையைப் பிடித்து நடக்க வைக்க நான் இருப்பேன்… ஆனால், நீ வாழ்க்கையில் எத்தனை உயரம் சென்றாலும், உன் காலில் நீயே நின்று ஜெயிக்க வேண்டும் என்பதுதான் என் ஆசை!

உலகம் உன்னைப் பார்த்து சிரிக்கும் நாட்கள் வந்தாலும், உன் கனவுகளை மட்டும் ஒருபோதும் விட்டுவிடாதே. தோல்வி வந்தால் துவண்டு போகாதே; உன்னை யாரும் நம்பவில்லை என்றாலும், உன்னை நீ நம்புவதை மட்டும் நிறுத்தாதே!

பணம் சம்பாதிப்பதைவிடப் பெரியது நல்ல மனிதனாக வாழ்வது…
வெற்றி பெறுவதைவிடப் பெரியது விழுந்தாலும் மீண்டும் எழுவது…
உலகமே உன்னை மறந்தாலும், உன் அம்மாவின் தியாகத்தை மட்டும் மறந்துவிடாதே!

உன் வாழ்க்கையில் உனக்காகக் கதவுகள் திறக்கவில்லை என்றால், உன் உழைப்பால் புதிய கதவுகளை உருவாக்கு. யாருடைய நிழலிலும் வாழாதே; உன்னால் மற்றவர்களுக்கு நிழல் கிடைக்கும் அளவுக்கு உயர்ந்து நில்!

நான் உன் தாய் மாமன் மட்டுமல்ல… உன் கனவுகளுக்கு ஒரு ரசிகன், உன் கஷ்டங்களுக்கு ஒரு தோள், உன் தோல்விகளுக்கு ஒரு ஆறுதல், உன் வெற்றிகளுக்கு உன்னைவிட அதிகமாகச் சந்தோஷப்படும் ஒரு உறவு!

நீ எவ்வளவு உயரம் சென்றாலும், உன் வேர்களை மறக்காதே… எவ்வளவு கஷ்டம் வந்தாலும், உன் தைரியத்தை இழக்காதே… எவ்வளவு பெரிய ஆளானாலும், உன் மனிதத்தன்மையை இழக்காதே!

ஒருநாள் நீ பெரிய மனிதனாக வளர்ந்து இந்த உலகம் உன்னைப் பாராட்டும்போது, “என் தாய் மாமன் எனக்கு ஒரு வார்த்தை சொன்னார்… அதுதான் என் வாழ்க்கையை மாற்றியது” என்று பெருமையோடு சொல்ல வேண்டும் என்பதுதான் என் ஆசை.

உன் வாழ்க்கையில் நீ தோற்றாலும் உனக்காக நான் இருப்பேன்; நீ ஜெயித்தால் உன்னைப் பார்த்துப் பெருமைப்படும் முதல் ஆளாகவும் நான் இருப்பேன்!

இப்படிக்கு,
உன்னை உயிராக நேசிக்கும் உன் தாய் மாமன்! ❤️🫂👑"""),
    ]
    for emoji, name, msg in wishes:
        st.markdown(f"""
        <div class="milestone">
            <span style="font-size:1.8rem;">{emoji}</span>
            <b style="color:#ff6b9d; font-size:1.1rem;">{name}:</b>
            <span style="font-size:1.05rem;"> {msg}</span>
        </div>
        """, unsafe_allow_html=True)

    if custom_wish:
        st.markdown(f"""
        <div class="milestone" style="border-left-color:#4a90e2; background:linear-gradient(135deg,#e6f3ff,#fff5f7);">
            <span style="font-size:1.8rem;">💝</span>
            <b style="color:#4a90e2;">Your Custom Wish:</b>
            <span> {custom_wish}</span>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📅 Amazing Milestones Awaiting")
    milestones = [
        ("🍼", "First Smile", "~6 weeks", "That gummy smile will melt everyone's heart."),
        ("🦷", "First Tooth", "~6 months", "Tiny pearl, big milestone!"),
        ("🚼", "First Crawl", "~9 months", "Watch out — the world becomes his playground."),
        ("👣", "First Steps", "~12 months", "Wobbly, brave, and absolutely adorable."),
        ("🗣️", "First Word", "~12-15 months", "Probably 'Mama' or 'Dada' — but we're hoping 'Auntie'!"),
        ("🎒", "First Day of School", "~5 years", "Big backpack, bigger dreams."),
        ("🎂", "Sweet Sixteen", "~16 years", "Time flies — cherish every moment."),
        ("🎓", "Graduation", "~22 years", "Watch him walk across that stage proudly."),
    ]
    for emoji, title, when, desc in milestones:
        st.markdown(f"""
        <div class="milestone">
            <span style="font-size:1.6rem;">{emoji}</span>
            <b style="color:#4a90e2;">{title}</b>
            <span style="color:#ff6b9d; font-weight:600;"> ({when})</span><br>
            <span style="color:#555;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 📜 A Welcome Poem")
    poem = f"""
    <div class="welcome-card" style="text-align:left;">
    <pre style="font-family:'Quicksand',sans-serif; font-size:1.15rem; line-height:2; color:#333; white-space:pre-wrap;">
    Ten tiny fingers, ten tiny toes,
    A button nose, a baby that grows.
    Welcome dear {baby_name}, so precious and small,
    You've answered our heart's most beautiful call.

    The stars sang softly the night you arrived,
    The angels rejoiced, and the heavens smiled.
    A new chapter starts, a fresh page so bright,
    Filled with laughter, and love, and soft lullabies at night.

    May your days be sunny, your dreams be grand,
    May you walk with courage and hold love's hand.
    May you know you're cherished beyond all measure,
    You are our forever, our infinite treasure.

    💙 Welcome to the world, little one 💙
    Your journey has only just begun.
    </pre>
    </div>
    """
    st.markdown(poem, unsafe_allow_html=True)

with tab4:
    st.markdown("### 🌟 Blessings & Well Wishes")
    blessings = [
        "🌟 May you grow up healthy, happy, and strong.",
        "🌈 May you always find light even on the cloudiest days.",
        "💙 May you be surrounded by people who love you unconditionally.",
        "📚 May you never stop learning and wondering.",
        "😄 May your laughter be contagious and your joy endless.",
        "🤝 May you find true friendships that last a lifetime.",
        "💪 May you have the courage to chase every dream.",
        "🙏 May you be protected, guided, and forever blessed.",
        "🎯 May you find purpose and passion in all you do.",
        "🌻 May your kindness touch everyone you meet.",
    ]
    for b in blessings:
        st.markdown(f"""
        <div style="background:linear-gradient(90deg, #fff5f7, #e6f3ff);
                    padding:0.9rem 1.2rem; margin:0.5rem 0; border-radius:12px;
                    font-family:'Quicksand',sans-serif; font-size:1.1rem;
                    box-shadow:0 3px 10px rgba(0,0,0,0.08);">
            {b}
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.markdown("### 🎁 Click for a Surprise!")
    if st.button("🎊 Celebrate Baby 2026! 🎊"):
        st.balloons()
        st.snow()
        st.markdown("""
        <div class="welcome-card">
            <h2 style="color:#ff6b9d; font-family:'Fredoka One',cursive;">
                🎉 Hip Hip Hooray! 🎉
            </h2>
            <p style="font-size:1.5rem; font-family:'Pacifico',cursive; color:#4a90e2;">
                Welcome, sweet baby boy!<br>
                Your story starts today, and it's going to be magnificent!
            </p>
            <div style="font-size:4rem;">👶🎈💙🎀🧸🍼🌟</div>
        </div>
        """, unsafe_allow_html=True)
        # Extra confetti burst
        components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
        <script>
            confetti({ particleCount: 300, spread: 180, origin: { y: 0.5 } });
            for(let i=0;i<5;i++){
                setTimeout(()=> confetti({
                    particleCount: 100, angle: Math.random()*360, spread: 80,
                    origin: { x: Math.random(), y: Math.random() }
                }), i*300);
            }
        </script>
        """, height=0)

# ============================================================
# BABY FACTS - Fun with Columns
# ============================================================
st.markdown("---")
st.markdown("### 🍼 Did You Know? Fun Baby Facts")

facts = [
    "👶 Newborns can recognize their mother's voice at birth.",
    "💤 Babies spend about 16-17 hours a day sleeping.",
    "💙 A baby's heart beats around 120-160 times per minute.",
    "😊 Babies start smiling socially at around 6 weeks.",
    "🎵 Babies respond to music even before birth.",
    "👀 Newborns see best at a distance of 8-12 inches.",
    "🦷 Baby teeth begin forming before birth.",
    "🌙 Newborns don't have a circadian rhythm — day and night are the same to them!",
]
cols = st.columns(2)
for i, fact in enumerate(facts):
    with cols[i % 2]:
        st.markdown(f"""
        <div style="background:white; padding:1rem; border-radius:15px;
                    margin:0.5rem 0; box-shadow:0 5px 15px rgba(0,0,0,0.08);
                    font-family:'Quicksand',sans-serif; font-size:1.05rem;">
            {fact}
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# NURSERY RHYME PLAYER (Extra musical fun)
# ============================================================
st.markdown("---")
st.markdown("### 🎵 More Lullaby Tunes")
colA, colB, colC = st.columns(3)

with colA:
    if st.button("🌟 Twinkle Twinkle"):
        components.html("""
        <script>
        const ctx = new AudioContext();
        const notes = [[523,0.4],[523,0.4],[784,0.4],[784,0.4],[880,0.4],[880,0.4],[784,0.8],
                       [698,0.4],[698,0.4],[659,0.4],[659,0.4],[587,0.4],[587,0.4],[523,0.8]];
        let t = ctx.currentTime;
        notes.forEach(([f,d])=>{
            const o=ctx.createOscillator(), g=ctx.createGain();
            o.type='sine'; o.frequency.value=f;
            g.gain.setValueAtTime(0.2,t);
            g.gain.linearRampToValueAtTime(0,t+d);
            o.connect(g); g.connect(ctx.destination);
            o.start(t); o.stop(t+d); t+=d;
        });
        </script>
        """, height=0)
        st.success("🌟 Playing Twinkle Twinkle!")

with colB:
    if st.button("🎵 Happy Birthday"):
        components.html("""
        <script>
        const ctx = new AudioContext();
        const notes = [[264,0.3],[264,0.3],[297,0.6],[264,0.6],[352,0.6],[330,1.0],
                       [264,0.3],[264,0.3],[297,0.6],[264,0.6],[396,0.6],[352,1.0]];
        let t = ctx.currentTime;
        notes.forEach(([f,d])=>{
            const o=ctx.createOscillator(), g=ctx.createGain();
            o.type='triangle'; o.frequency.value=f;
            g.gain.setValueAtTime(0.2,t);
            g.gain.linearRampToValueAtTime(0,t+d);
            o.connect(g); g.connect(ctx.destination);
            o.start(t); o.stop(t+d); t+=d;
        });
        </script>
        """, height=0)
        st.success("🎵 Happy Birthday melody!")

with colC:
    if st.button("🎶 Brahm's Lullaby"):
        components.html("""
        <script>
        const ctx = new AudioContext();
        const notes = [[659,0.5],[659,0.5],[587,0.5],[659,0.5],[523,1.0],
                       [659,0.5],[659,0.5],[587,0.5],[659,0.5],[523,1.0]];
        let t = ctx.currentTime;
        notes.forEach(([f,d])=>{
            const o=ctx.createOscillator(), g=ctx.createGain();
            o.type='sine'; o.frequency.value=f;
            g.gain.setValueAtTime(0.15,t);
            g.gain.linearRampToValueAtTime(0,t+d);
            o.connect(g); g.connect(ctx.destination);
            o.start(t); o.stop(t+d); t+=d;
        });
        </script>
        """, height=0)
        st.success("🎶 Brahm's Lullaby playing!")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:2rem; font-family:'Quicksand',sans-serif;">
    <div style="font-size:3rem;">👶💙🎉</div>
    <h2 style="font-family:'Fredoka One',cursive; color:#ff6b9d;">
        Welcome to the World, {baby_name}!
    </h2>
    <p style="font-size:1.2rem; color:#4a90e2;">
        <b>Congratulations on your new baby boy!</b>
    </p>
    <p style="font-size:1rem; color:#888;">
        Made with 💙 by your loving Auntie | © 2026
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FINAL CONFETTI BURST ON LOAD
# ============================================================
components.html("""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
<script>
setTimeout(()=>{
    confetti({ particleCount: 400, spread: 200, origin: { y: 0.6 },
        colors: ['#ff6b9d','#4a90e2','#50c878','#ffb347','#ffd700'] });
}, 800);
</script>
""", height=0)
