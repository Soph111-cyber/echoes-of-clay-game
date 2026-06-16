import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

try:
    import plotly.graph_objects as go
except Exception:
    go = None

BASE = Path(__file__).parent
DATA = BASE / "data"
ASSETS = BASE / "assets"

st.set_page_config(
    page_title="Echoes of Clay",
    page_icon="🏺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Data loading
# -------------------------
@st.cache_data
def load_json(name):
    with open(DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_csv(name):
    return pd.read_csv(DATA / name)

TEXT = load_json("game_text.json")
IDENTITIES = load_json("identities.json")
SHIP = load_csv("ship_clues.csv")
RECON = load_json("reconstruction_cases.json")

# -------------------------
# UI helpers
# -------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(circle at 10% 20%, #fff0d9 0, transparent 26%),
                radial-gradient(circle at 90% 10%, #f2e1ff 0, transparent 24%),
                linear-gradient(135deg, #fff9f0 0%, #fff3e8 46%, #f7f0ff 100%);
}
.hero {
    border-radius: 28px;
    padding: 30px 34px;
    background: linear-gradient(135deg, rgba(255,255,255,.92), rgba(255,242,219,.82));
    box-shadow: 0 18px 55px rgba(142, 88, 42, .15);
    border: 1px solid rgba(150, 95, 55, .15);
    margin-bottom: 18px;
}
.hero h1 {
    font-size: 48px;
    line-height: 1.05;
    margin-bottom: 8px;
    background: linear-gradient(90deg, #884b24, #b76e2a, #5f3dc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    border-radius: 24px;
    padding: 22px 24px;
    background: rgba(255,255,255,.86);
    border: 1px solid rgba(120, 80, 40, .12);
    box-shadow: 0 10px 30px rgba(90, 60, 30, .10);
    margin-bottom: 16px;
}
.module-title {
    font-size: 24px;
    font-weight: 800;
    color: #74431c;
}
.small-label {
    font-size: 13px;
    color: #8a6c55;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-weight: 700;
}
.score-box {
    text-align: center;
    padding: 16px;
    border-radius: 18px;
    background: linear-gradient(135deg, #fff8dd, #f1e6ff);
    border: 1px solid rgba(140, 90, 40, .16);
}
.big-score { font-size: 34px; font-weight: 850; color: #7a3f15; }
.anime-badge {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px 6px 4px 0;
    border-radius: 999px;
    background: #fff3d5;
    border: 1px solid #e9c88d;
    color: #74431c;
    font-weight: 700;
}
.footer-note {
    color: #6c5848;
    font-size: 14px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

LANG = st.sidebar.radio("Language / 语言", ["中文", "English"], horizontal=True)
ZH = LANG == "中文"

def t(zh, en):
    return zh if ZH else en

def add_points(key, amount):
    st.session_state[key] = st.session_state.get(key, 0) + amount

for k in ["create_score", "experience_score", "infer_score", "portfolio"]:
    if k not in st.session_state:
        st.session_state[k] = 0 if k != "portfolio" else []

# -------------------------
# Sidebar navigation
# -------------------------
st.sidebar.title("🏺 Echoes of Clay")
page = st.sidebar.radio(
    t("进入模块", "Enter Module"),
    [
        t("首页｜Project Overview", "Home | Project Overview"),
        t("模块一｜Kiln of Identity", "Module 1 | Kiln of Identity"),
        t("模块二｜Walk the Silk Road", "Module 2 | Walk the Silk Road"),
        t("模块三｜Ship of Clues", "Module 3 | Ship of Clues"),
        t("模块四｜Reconstruct the Past", "Module 4 | Reconstruct the Past"),
        t("模块五｜Flow of Culture", "Module 5 | Flow of Culture"),
        t("结尾档案｜Research Portfolio", "Final Archive | Research Portfolio"),
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(t("### 🎮 当前探索值", "### 🎮 Current Learning Scores"))
st.sidebar.metric(t("手：Create", "Hands: Create"), st.session_state.create_score)
st.sidebar.metric(t("感官：Experience", "Senses: Experience"), st.session_state.experience_score)
st.sidebar.metric(t("大脑：Infer", "Mind: Infer"), st.session_state.infer_score)

# -------------------------
# Home
# -------------------------
if "首页" in page or "Home" in page:
    st.markdown(
        f"""
        <div class='hero'>
        <h1>{t(TEXT['title_zh'], TEXT['title_en'])}</h1>
        <p style='font-size:20px; color:#5d4a3c; max-width:980px;'>{t(TEXT['tagline_zh'], TEXT['tagline_en'])}</p>
        <span class='anime-badge'>Create 制作</span>
        <span class='anime-badge'>Experience 体验</span>
        <span class='anime-badge'>Infer 推理</span>
        <span class='anime-badge'>Uncertainty 不确定性</span>
        <span class='anime-badge'>Cultural Reasoning 文化推理</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card'><div class='small-label'>Level 1</div><div class='module-title'>Create</div><p>手：制作唐三彩，把器型、釉色、纹样变成可解释的文化选择。</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><div class='small-label'>Level 2</div><div class='module-title'>Experience</div><p>感官：在丝路场景中做选择，理解文化传播的路径与摩擦。</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'><div class='small-label'>Level 3</div><div class='module-title'>Infer</div><p>大脑：用证据、概率和不确定性推断沉船、残片与文化来源。</p></div>", unsafe_allow_html=True)

    st.markdown("### 🌙 " + t("游戏模块", "Game Modules"))
    for m in TEXT["modules"]:
        st.markdown(f"<div class='card'><b>{t(m['zh'], m['en'])}</b><br>{t(m['desc_zh'], m['desc_en'])}</div>", unsafe_allow_html=True)

    st.info(t(
        "建议游玩顺序：先做唐三彩，再走丝路，之后进入沉船推理、残片复原和文化传播模拟。每一步都会进入最终研究档案。",
        "Suggested order: create Sancai first, walk the Silk Road, then infer ship origins, reconstruct shards, and simulate cultural diffusion. Every decision enters your final research archive."
    ))

# -------------------------
# Module 1: Kiln of Identity
# -------------------------
elif "Kiln" in page:
    st.markdown(f"<div class='hero'><h1>🔥 {t('Kiln of Identity｜窑中的身份','Kiln of Identity')}</h1><p>{t('你不是在做一个好看的工艺品，而是在为一个社会身份制作一件会被解释的物。','You are not merely making a beautiful object; you are making an interpretable object for a social identity.')}</p></div>", unsafe_allow_html=True)

    identities_display = {t(i["zh"], i["en"]): i for i in IDENTITIES}
    identity_name = st.selectbox(t("Step 1：选择身份", "Step 1: Choose an identity"), list(identities_display.keys()))
    identity = identities_display[identity_name]
    st.caption(t(identity["notes_zh"], identity["notes_en"]))

    forms = {
        "horse": t("马 Horse", "Horse"),
        "camel": t("骆驼 Camel", "Camel"),
        "female_figure": t("仕女俑 Noblewoman Figure", "Noblewoman Figure"),
        "envoy_figure": t("使节俑 Envoy Figure", "Envoy Figure"),
        "merchant_figure": t("商人俑 Merchant Figure", "Merchant Figure"),
        "guardian": t("镇墓兽 Guardian Beast", "Guardian Beast"),
        "vessel": t("器皿 Vessel", "Vessel"),
    }
    colors = {
        "amber": t("黄色/琥珀 Amber", "Amber"),
        "green": t("绿色 Green", "Green"),
        "white": t("白色 White", "White"),
        "brown": t("褐色 Brown", "Brown"),
        "cobalt": t("钴蓝 Cobalt Blue", "Cobalt Blue"),
        "pink": t("现代粉色 Modern Pink", "Modern Pink"),
    }
    patterns = {
        "lotus": t("莲花 Lotus", "Lotus"),
        "cloud": t("云纹 Cloud", "Cloud"),
        "floral": t("花草 Floral", "Floral"),
        "grapevine": t("葡萄卷草 Grapevine", "Grapevine"),
        "pearl_roundel": t("联珠纹 Pearl Roundel", "Pearl Roundel"),
        "animal": t("动物纹 Animal", "Animal"),
        "geometric": t("几何纹 Geometric", "Geometric"),
        "pixel_heart": t("像素爱心 Pixel Heart", "Pixel Heart"),
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        form = st.selectbox(t("Step 2：选择器型", "Step 2: Choose form"), list(forms.keys()), format_func=lambda x: forms[x])
    with col2:
        color = st.selectbox(t("Step 3：选择釉色", "Step 3: Choose glaze color"), list(colors.keys()), format_func=lambda x: colors[x])
    with col3:
        pattern = st.selectbox(t("Step 4：选择纹样", "Step 4: Choose motif"), list(patterns.keys()), format_func=lambda x: patterns[x])

    st.markdown("### 🔥 " + t("烧制参数：多变量函数映射", "Firing parameters: multivariable mapping"))
    k1, k2, k3 = st.columns(3)
    with k1:
        temp = st.slider(t("温度 Temperature °C", "Temperature °C"), 650, 1050, 860)
    with k2:
        time = st.slider(t("时间 Time hours", "Time hours"), 2, 12, 6)
    with k3:
        oxygen = st.slider(t("氧化气氛 Oxygen level", "Oxygen level"), 0.0, 1.0, 0.65)

    form_score = 25 if form in identity["preferred_forms"] else 10
    color_score = 25 if color in identity["preferred_colors"] else (5 if color in ["pink"] else 12)
    pattern_score = 25 if pattern in identity["preferred_patterns"] else (4 if pattern == "pixel_heart" else 12)
    firing_score = max(0, 25 - abs(temp - 860) / 18 - abs(time - 6) * 2.2 - abs(oxygen - .65) * 20)
    authenticity = round(form_score + color_score + pattern_score + firing_score, 1)

    visual_quality = round(40 + 35 * math.exp(-((temp-860)/130)**2) + 15 * math.exp(-((time-6)/4)**2) + 10 * oxygen, 1)
    cultural_fit = round((form_score + color_score + pattern_score) / 75 * 100, 1)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"<div class='score-box'><div class='small-label'>{t('真实性评分','Authenticity Score')}</div><div class='big-score'>{authenticity}</div></div>", unsafe_allow_html=True)
    with r2:
        st.markdown(f"<div class='score-box'><div class='small-label'>{t('视觉完成度','Visual Outcome')}</div><div class='big-score'>{visual_quality}</div></div>", unsafe_allow_html=True)
    with r3:
        st.markdown(f"<div class='score-box'><div class='small-label'>{t('身份匹配度','Identity Fit')}</div><div class='big-score'>{cultural_fit}%</div></div>", unsafe_allow_html=True)

    st.markdown("#### 🧠 " + t("模型解释", "Model interpretation"))
    st.write(t(
        "这里的数学本质是：你控制一个参数空间，再映射到结果空间。也就是 f(温度, 时间, 氧气, 器型, 釉色, 纹样) → 视觉结果 + 文化解释。",
        "Mathematically, you control a parameter space and map it into an outcome space: f(temperature, time, oxygen, form, glaze, motif) → visual outcome + cultural interpretation."
    ))

    if authenticity >= 85:
        result = t("👑 被贵族收藏：你的器型、釉色与纹样高度匹配身份。", "👑 Collected by nobility: your form, glaze, and motif strongly match the identity.")
    elif authenticity >= 65:
        result = t("🏺 用于陪葬：设计有文化逻辑，但仍保留混合与不确定性。", "🏺 Used as burial object: the design has cultural logic but includes hybridity and uncertainty.")
    elif authenticity >= 45:
        result = t("🌍 被商队带走：它更像跨文化流动中的混合物。", "🌍 Carried by traders: it resembles a hybrid object in cross-cultural movement.")
    else:
        result = t("❌ 暂无认领：文化线索冲突太强，需要重新解释。", "❌ Unclaimed: cultural clues conflict too strongly and need reinterpretation.")
    st.success(result)

    if st.button(t("保存到研究档案", "Save to Research Archive"), type="primary"):
        st.session_state.create_score += int(authenticity // 5)
        st.session_state.portfolio.append({
            "module": "Kiln of Identity",
            "identity": identity_name,
            "form": forms[form],
            "color": colors[color],
            "pattern": patterns[pattern],
            "authenticity": authenticity,
            "interpretation": result,
        })
        st.toast(t("已保存！", "Saved!"), icon="🏺")

# -------------------------
# Module 2: Walk the Silk Road
# -------------------------
elif "Silk" in page:
    st.markdown(f"<div class='hero'><h1>🧭 {t('Walk the Silk Road｜行走丝路','Walk the Silk Road')}</h1><p>{t('你成为商队随行者。每个选择都会改变文化传播路径。','You become a caravan companion. Every choice changes the route of cultural transmission.')}</p></div>", unsafe_allow_html=True)

    st.markdown("### " + t("选择你的丝路决策", "Choose your Silk Road decisions"))
    col1, col2, col3 = st.columns(3)
    with col1:
        market = st.radio(t("在长安市场，你优先交换：", "In Chang'an market, you prioritize:"),
                          [t("陶器与釉料", "Ceramics and glazes"), t("丝绸与织物", "Silk and textiles"), t("香料与药材", "Spices and medicines")])
    with col2:
        language = st.radio(t("遇到外来商人，你选择：", "Meeting foreign merchants, you:"),
                            [t("学习对方词汇", "Learn their words"), t("只用本地术语", "Use only local terms"), t("用图案和手势沟通", "Communicate with images and gestures")])
    with col3:
        attitude = st.radio(t("面对陌生纹样，你会：", "Facing unfamiliar motifs, you:"),
                            [t("吸收并改造", "Adapt and transform"), t("保持原样复制", "Copy unchanged"), t("拒绝使用", "Reject them")])

    base = np.array([0.40, 0.25, 0.20, 0.15])
    # Chang'an, Central Asia, Persia, Indian Ocean
    if "釉料" in market or "glazes" in market:
        base += np.array([0.08, 0.04, 0.04, -0.02])
    elif "丝绸" in market or "Silk" in market:
        base += np.array([0.05, 0.10, 0.00, -0.01])
    else:
        base += np.array([-0.02, 0.01, 0.06, 0.12])
    if "学习" in language or "Learn" in language:
        base += np.array([-0.02, 0.08, 0.06, 0.02])
    elif "图案" in language or "images" in language:
        base += np.array([0.02, 0.05, 0.05, 0.04])
    else:
        base += np.array([0.08, -0.03, -0.03, -0.02])
    if "吸收" in attitude or "Adapt" in attitude:
        base += np.array([-0.03, 0.08, 0.06, 0.03])
    elif "复制" in attitude or "Copy" in attitude:
        base += np.array([0.00, 0.03, 0.02, 0.01])
    else:
        base += np.array([0.10, -0.05, -0.04, -0.03])
    base = np.maximum(base, 0.02)
    probs = base / base.sum()

    regions = [t("长安", "Chang'an"), t("中亚", "Central Asia"), t("波斯", "Persia"), t("印度洋", "Indian Ocean")]
    df = pd.DataFrame({t("区域", "Region"): regions, t("文化影响概率", "Cultural transition probability"): probs})
    st.bar_chart(df.set_index(t("区域", "Region")))

    st.markdown("#### 🧠 " + t("深层模型", "Underlying model"))
    st.write(t(
        "这可以被写成一个简化 Markov Chain：你的选择改变从一个文化节点转移到另一个文化节点的概率。文化传播不是复制粘贴，而是在路径、语言和利益中被重新组合。",
        "This can be framed as a simplified Markov Chain: your choices alter transition probabilities between cultural nodes. Cultural transmission is not copy-paste; it is recombined through routes, language, and interests."
    ))

    if st.button(t("保存丝路路径", "Save Silk Road Path"), type="primary"):
        st.session_state.experience_score += int(max(probs) * 40)
        st.session_state.portfolio.append({
            "module": "Walk the Silk Road",
            "market_choice": market,
            "language_choice": language,
            "attitude_choice": attitude,
            "dominant_region": regions[int(np.argmax(probs))],
            "probability": round(float(max(probs)), 3),
        })
        st.toast(t("丝路路径已进入档案！", "Silk Road path saved!"), icon="🧭")

# -------------------------
# Module 3: Ship of Clues
# -------------------------
elif "Ship" in page:
    st.markdown(f"<div class='hero'><h1>⚓ {t('Ship of Clues｜沉船线索','Ship of Clues')}</h1><p>{t('你不是在捞宝物，而是在用物品关系推断船的身份。','You are not collecting treasure; you are inferring the ship’s identity from relationships among objects.')}</p></div>", unsafe_allow_html=True)

    st.dataframe(SHIP[["artifact", "form", "glaze", "motif", "context"]], use_container_width=True)
    selected = st.multiselect(
        t("选择你在沉船中记录到的证据", "Select the evidence you recorded in the shipwreck"),
        SHIP["artifact"].tolist(),
        default=["ceramic_shard", "blue_glaze_fragment", "camel_figurine"],
    )

    if selected:
        subset = SHIP[SHIP["artifact"].isin(selected)]
        weights = subset[["weight_china", "weight_central_asia", "weight_persia", "weight_indian_ocean"]].mean().values
        weights = weights / weights.sum()
        labels = [t("中国/长安生产网络", "Chinese/Chang'an production network"), t("中亚陆路贸易", "Central Asian overland trade"), t("波斯联系", "Persian connection"), t("印度洋贸易", "Indian Ocean trade")]
        posterior = pd.DataFrame({t("假设", "Hypothesis"): labels, t("后验概率", "Posterior probability"): weights})
        st.bar_chart(posterior.set_index(t("假设", "Hypothesis")))

        st.markdown("#### 🧩 " + t("证据解释", "Evidence explanations"))
        for _, row in subset.iterrows():
            st.markdown(f"- **{row['artifact']}**：{row['origin_hint']}")

        st.info(t(
            f"当前最可能解释：{labels[int(np.argmax(weights))]}，但概率不是100%。考古推理的高级之处正在于：它要诚实呈现不确定性。",
            f"Current most likely interpretation: {labels[int(np.argmax(weights))]}, but it is not 100%. The strength of archaeological reasoning lies in honestly presenting uncertainty."
        ))

        if st.button(t("保存沉船推理", "Save Ship Inference"), type="primary"):
            st.session_state.infer_score += int(max(weights) * 50)
            st.session_state.portfolio.append({
                "module": "Ship of Clues",
                "evidence": ", ".join(selected),
                "top_hypothesis": labels[int(np.argmax(weights))],
                "posterior_probability": round(float(max(weights)), 3),
            })
            st.toast(t("沉船推理已保存！", "Ship inference saved!"), icon="⚓")

# -------------------------
# Module 4: Reconstruct the Past
# -------------------------
elif "Reconstruct" in page:
    st.markdown(f"<div class='hero'><h1>🧩 {t('Reconstruct the Past｜复原残片','Reconstruct the Past')}</h1><p>{t('历史是不完整的。玩家要从残片中推测整体，同时说明自己有多不确定。','History is incomplete. You infer the whole from fragments while explaining uncertainty.')}</p></div>", unsafe_allow_html=True)

    case_display = {t(c["zh"], c["en"]): c for c in RECON}
    case_name = st.selectbox(t("选择一块残片", "Choose a shard"), list(case_display.keys()))
    case = case_display[case_name]
    st.markdown(f"<div class='card'><b>{t('可见线索','Visible clues')}：</b>{case['visible']}</div>", unsafe_allow_html=True)

    answer = st.radio(t("你判断缺失部分最可能是什么纹样？", "What motif is the missing part most likely to be?"), case["options"])
    confidence_user = st.slider(t("你的信心 Confidence", "Your confidence"), 0.0, 1.0, 0.60)

    if st.button(t("提交复原判断", "Submit reconstruction"), type="primary"):
        correct = answer == case["answer"]
        score = int((30 if correct else 10) + 20 * (1 - abs(confidence_user - case["confidence"])))
        st.session_state.infer_score += score
        if correct:
            st.success(t("判断正确！但更重要的是你保留了不确定性。", "Correct! More importantly, you preserved uncertainty."))
        else:
            st.warning(t("判断不完全匹配。考古复原不只是猜图案，而是要解释证据为什么支持/不支持某个假设。", "Not fully matched. Reconstruction is not just guessing motifs; it requires explaining why evidence supports or weakens a hypothesis."))
        st.write(t(case["explain_zh"], case["explain_en"]))
        st.session_state.portfolio.append({
            "module": "Reconstruct the Past",
            "case": case_name,
            "your_answer": answer,
            "model_answer": case["answer"],
            "model_confidence": case["confidence"],
            "your_confidence": confidence_user,
        })

# -------------------------
# Module 5: Flow of Culture
# -------------------------
elif "Flow" in page:
    st.markdown(f"<div class='hero'><h1>🌊 {t('Flow of Culture｜文化流动模拟器','Flow of Culture')}</h1><p>{t('你改变贸易、战争和政策参数，观察唐三彩风格如何扩散、变形或消失。','Adjust trade, conflict, and policy parameters to see how Sancai style spreads, transforms, or fades.')}</p></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        trade = st.slider(t("贸易强度 Trade intensity", "Trade intensity"), 0.0, 1.0, 0.70)
    with col2:
        conflict = st.slider(t("冲突阻碍 Conflict barrier", "Conflict barrier"), 0.0, 1.0, 0.20)
    with col3:
        policy = st.slider(t("开放政策 Openness policy", "Openness policy"), 0.0, 1.0, 0.65)

    nodes = ["Chang'an", "Dunhuang", "Samarkand", "Persia", "Indian Ocean"]
    x = [0, 1, 2, 3, 2.5]
    y = [0, .8, .4, .7, -0.6]
    influence = []
    current = 1.0
    for i in range(len(nodes)):
        if i == 0:
            influence.append(current)
        else:
            current = current * (0.55 + 0.55 * trade) * (1 - 0.55 * conflict) * (0.55 + 0.45 * policy)
            influence.append(current)
    influence = np.array(influence)
    influence = influence / influence.max()

    if go:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(width=2), hoverinfo="skip"))
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="markers+text",
            marker=dict(size=25 + influence * 55),
            text=nodes,
            textposition="top center",
            hovertemplate="%{text}<br>Influence=%{marker.size}<extra></extra>"
        ))
        fig.update_layout(height=420, showlegend=False, margin=dict(l=10, r=10, t=20, b=10),
                          xaxis=dict(visible=False), yaxis=dict(visible=False),
                          plot_bgcolor="rgba(255,255,255,0)", paper_bgcolor="rgba(255,255,255,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(pd.DataFrame({"influence": influence}, index=nodes))

    diffusion_index = round(float(influence.mean() * 100), 1)
    st.metric(t("文化扩散指数", "Cultural Diffusion Index"), diffusion_index)
    st.write(t(
        "几何意义：每个城市是网络中的节点，贸易/冲突/政策改变边的权重；风格不是沿直线前进，而是在网络上扩散。",
        "Geometric meaning: each city is a node in a network, and trade/conflict/policy change edge weights. Style does not move along a single line; it diffuses through a network."
    ))

    if st.button(t("保存传播模拟", "Save diffusion simulation"), type="primary"):
        st.session_state.experience_score += int(diffusion_index // 3)
        st.session_state.portfolio.append({
            "module": "Flow of Culture",
            "trade": trade,
            "conflict": conflict,
            "policy": policy,
            "diffusion_index": diffusion_index,
        })
        st.toast(t("文化流动模拟已保存！", "Diffusion simulation saved!"), icon="🌊")

# -------------------------
# Final portfolio
# -------------------------
elif "档案" in page or "Archive" in page:
    st.markdown(f"<div class='hero'><h1>📜 {t('研究档案｜Research Portfolio','Research Portfolio')}</h1><p>{t('这里把你的游戏选择转化为一份可展示的项目档案。','This page turns your gameplay decisions into a displayable project archive.')}</p></div>", unsafe_allow_html=True)

    total = st.session_state.create_score + st.session_state.experience_score + st.session_state.infer_score
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("Create", "Create"), st.session_state.create_score)
    c2.metric(t("Experience", "Experience"), st.session_state.experience_score)
    c3.metric(t("Infer", "Infer"), st.session_state.infer_score)
    c4.metric(t("Total", "Total"), total)

    st.markdown("### ✨ " + t("项目定位", "Project Positioning"))
    st.success(t(
        "I transform archaeology from static knowledge into interactive systems where users reconstruct history through decisions, uncertainty, and cultural reasoning.",
        "I transform archaeology from static knowledge into interactive systems where users reconstruct history through decisions, uncertainty, and cultural reasoning."
    ))

    if st.session_state.portfolio:
        df = pd.DataFrame(st.session_state.portfolio)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(t("下载研究档案 CSV", "Download Research Archive CSV"), csv, "echoes_of_clay_archive.csv", "text/csv")
    else:
        st.info(t("还没有保存任何模块结果。去前面的模块玩一轮，再回来生成档案！", "No module results saved yet. Play a module and come back to generate your archive!"))

    st.markdown("### 🧠 " + t("可以写进申请材料的一句话", "Application-ready framing"))
    st.markdown(
        f"<div class='card'>{t('如果历史是不完整的，人类如何通过图案、互动与解释重建真相？', 'If history is incomplete, how can humans reconstruct truth through patterns, interaction, and interpretation?')}</div>",
        unsafe_allow_html=True,
    )
