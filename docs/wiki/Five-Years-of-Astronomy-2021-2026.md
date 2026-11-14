# Five Years of Astronomy (2021–2026): A Plain-Language Review

[English](#english) · [中文](#中文)

*Written November 2026. The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

---

## English

### 1. Why this page exists

[astrolab](https://github.com/sudoghut/astrolab) asks a simple question: with one laptop and a
coding agent, can you do real astronomy research? It works in three ways:

- **Ask questions, don't move data.** Modern sky surveys hold terabytes. Instead of downloading
  them, astrolab sends queries to the data centres, lets the servers filter and count, and keeps
  only megabyte-sized answers.
- **Grow by reproducing landmark results.** The [roadmap](https://github.com/sudoghut/astrolab/blob/main/ROADMAP.md)
  lists ten important results from 2022–2026. Reproducing each one forces the code to learn a new skill.
- **Grade every conclusion.** Each claim is labelled *established*, *tension*, *hint*,
  *contested* or *refuted*, and is checked by an automatic test.

This page is the background story: what happened in astronomy over the last five years, told
without equations, with the emphasis on the results astrolab is reproducing. Milestone labels
(M1, M4, ...) point to the roadmap.

### 2. New machines changed everything

Many of the breakthroughs since 2021 come from a set of new instruments that started delivering
data at about the same time:

| Instrument | What it does | In one picture |
|---|---|---|
| **James Webb Space Telescope (JWST)**, launched December 2021 | Sees the earliest galaxies in infrared light | Baby photos of the universe |
| **Gaia** satellite, Data Release 3 in 2022, Data Release 4 on 2 December 2026 | Measures positions and motions of almost two billion stars | A census of the Milky Way |
| **DESI** (Dark Energy Spectroscopic Instrument) | Measures distances to tens of millions of galaxies | A 3-D map of the universe |
| **LIGO, Virgo and KAGRA** gravitational-wave detectors | Catch the ripples in space-time sent out when black holes collide | Ears on the universe |
| **Pulsar timing arrays (PTAs)** | Use fast-spinning pulsars in our Galaxy as clocks | A gravitational-wave detector the size of the Galaxy |
| Euclid (launched 2023), the Vera C. Rubin Observatory (first images 2025) and others | Next-generation surveys, now starting to release data | |

Most of this data is **public** and can be queried online. That is what makes a laptop project
like astrolab possible.

### 3. From the whole universe down to single stars

astrolab arranges the universe in zoom levels, like an online map: L0 is the universe as a
whole, L4 is individual stars, and X is a cross-cutting theme (gravitational waves). We follow
the same order.

#### L0 · The universe as a whole: cracks in the standard model?

**Is dark energy changing? (M1, *hint*)**

The expansion of the universe is speeding up. Whatever drives it is called *dark energy*. In the
standard model of cosmology (ΛCDM), dark energy is a constant that never changes.

- DESI measures *baryon acoustic oscillations* (BAO): a pattern frozen into the distribution of
  galaxies in the early universe. It works as a standard ruler about 150 megaparsecs
  (roughly 500 million light-years) long.
- In 2024 and 2025, DESI found that when this ruler is combined with the cosmic microwave
  background and with supernovae, the data prefer a dark energy that **weakens over time**.
  The preference is 2.8–4.2σ, depending on which supernova sample is used.
- **In 2026 the signal weakened.** After a re-calibration of one supernova sample and a new DESI
  analysis of the Lyman-α forest, it sits at about 3σ.
- This is the most talked-about question in cosmology today. It may rewrite the textbooks, or it
  may turn out to be a calibration problem.
- Reproducing it needs only a kilobyte-sized table of distances. It is astrolab's next milestone.

**The Hubble tension (M2, *tension*)**

How fast is the universe expanding today? Two kinds of measurement disagree:

- Building a distance ladder from nearby Cepheid variable stars and supernovae gives about
  **73** km/s/Mpc.
- Working backwards from the cosmic microwave background (assuming ΛCDM) gives about **67–68**.
- The gap is more than 5σ. JWST re-checked the Hubble Space Telescope's Cepheid measurements and
  found no error.
- Another team (CCHP) measured distances using the tip of the red giant branch (TRGB) instead and
  got about **70**.

So part of the debate has moved from "is there new physics?" to "which galaxies should be used
for calibration?".

**The S8 tension is fading (M3, *contested*)**

S8 measures how strongly matter clumps together.

- Weak gravitational lensing surveys used to find a slightly lower value than the cosmic
  microwave background predicts.
- In 2025 the final KiDS analysis agreed with the microwave background. The Dark Energy Survey's
  Year 6 result is still about 2.6σ low.

This is a tension that is slowly going away — a reminder that systematic errors can look a lot
like new physics.

#### L1 · Cosmic dawn: JWST's surprise (M8)

- JWST has confirmed with spectra galaxies at redshift z ≈ 14: JADES-GS-z14-0 and MoM-z14
  (z = 14.44). We see them as they were about 300 million years after the Big Bang.
- The surprise is that there are **too many bright galaxies**. The early universe looks more
  "grown-up" than models predicted. The detection is *established*; the explanation is *contested*.
- Possible explanations include stars forming more efficiently, or galaxies flickering in
  brightness ("burstiness"), which makes them easier to catch while they are bright.
- Not on the roadmap, but just as hot: JWST found many compact red objects nicknamed
  **"Little Red Dots"**. They may be early black holes wrapped in dust or dense gas. Nobody is
  sure yet.

#### X · Gravitational-wave astronomy grows up

**A background hum at nanohertz frequencies (M9, *hint*)**

- In June 2023, four pulsar timing arrays — NANOGrav (North America), EPTA (Europe), PPTA
  (Australia) and CPTA (China) — announced the same thing: the arrival times of pulsar signals
  share a common slow "wobble".
- The way the wobble is correlated between pulsars follows the *Hellings–Downs curve*, the
  fingerprint of gravitational waves.
- The most likely source is the combined hum of supermassive black-hole pairs across the universe.
- The evidence is strong but has not yet reached the 5σ threshold for a discovery.

**A map of black-hole masses (M10)**

- The gravitational-wave catalogue GWTC-4.0, released in 2025, brought the total number of
  confident events to about two hundred.
- Black-hole masses are not spread evenly. There are pile-ups near 10 and 35 times the mass of
  the Sun, and the number drops sharply above 35.
- One event, GW231123, involves black holes in a mass range that ordinary stars are thought to be
  unable to produce (the *pair-instability gap*). They may be the products of earlier mergers.

#### L3 · Archaeology of the Milky Way

**Is the Milky Way lighter than we thought? (M6, *contested*)**

- Using Gaia data, astronomers measured how fast stars orbit in the outer Milky Way. The speed
  drops by about 30 km/s between 19.5 and 26.5 kiloparsecs from the centre.
- Taken at face value, this gives a total Galaxy mass of only about 2×10¹¹ Suns, much less than
  earlier estimates.
- Other methods, such as stellar streams and satellite galaxies, still favour a heavier dark
  matter halo. The question is open.

**The Milky Way grew up early (M5, *established*)**

- In 2022, Xiang & Rix (Nature) measured precise ages for about 250,000 subgiant stars by
  combining China's LAMOST spectroscopic survey with Gaia.
- They found that the Galaxy's thick disk started forming about **13 billion years ago** — much
  earlier than many had thought.

**The Radcliffe Wave (candidate M11)**

Near the Sun lies a wave-shaped chain of star-forming gas clouds about 9,000 light-years long.
In 2024 astronomers found that it is also oscillating, like a wave moving through the Galaxy.

#### L4 · Stars: Gaia reveals what cannot be seen

**Dormant black holes (M4, *established*; astrolab has finished the DR3 part)**

- Almost all stellar-mass black holes known before 2022 were feeding on a companion star and
  glowing in X-rays.
- Theory says most black holes in the Milky Way should be quiet: not feeding, not glowing.
- Gaia's trick is to measure the **tiny ellipse a normal star traces on the sky**. If the orbit is
  large but the companion is invisible, the companion may well be a black hole.
- Three have been found this way:

| Object | Found | Mass | Note |
|---|---|---|---|
| Gaia BH1 | 2022 | about 9.6 Suns | About 1,600 light-years away, the nearest known black hole |
| Gaia BH2 | 2023 | about 8.9 Suns | |
| Gaia BH3 | 2024 | about 33 Suns | The most massive stellar black hole known in the Milky Way; its companion is an old, metal-poor star |

- astrolab, using only Gaia DR3's public orbits:
  - gets 8.5 Suns for BH2, in agreement with the paper;
  - gets 13.3 Suns for BH1, in agreement with the paper's *astrometry-only* solution (12.8).
    The paper's 9.6 also uses ground-based radial-velocity measurements, which tighten the result;
  - recovers all 21 neutron-star candidates of El-Badry et al. (2024) with a server-side screen.
- **Gaia DR4 will contain many more orbits.** astrolab's screen is ready to run on release day,
  2 December 2026 — a rare case where a single researcher can be as fast as a large team.

**Wide binaries as a test of gravity (M7, *contested*, leaning Newtonian)**

- In pairs of stars thousands of astronomical units apart, the pull between them is extremely
  weak. MOND (Modified Newtonian Dynamics) predicts that gravity should then be stronger than
  Newton's law says.
- In 2023 one group reported a boost of about 1.4 times. Other groups, using cleaner samples,
  ruled MOND out with high significance.
- The fight is about **contamination**: a hidden third star, or two unrelated stars that just
  happen to line up, can make a pair look like it moves too fast.
- Gaia DR4's individual measurements over time (*epoch astrometry*) can expose hidden companions
  and may settle the question.

### 4. Other highlights outside the roadmap

These are summarised from general knowledge and have **not** gone through astrolab's
literature-verification process.

- **Event Horizon Telescope**: in 2022, the first image of Sagittarius A\*, the black hole at the
  centre of the Milky Way.
- **Exoplanet atmospheres**: JWST clearly detected carbon dioxide and other molecules in the air of
  planets around other stars. A 2025 claim of a possible sign of life on K2-18b caused a stir; most
  follow-up studies find the evidence weak.
- **Asteroid samples**: NASA's OSIRIS-REx returned material from asteroid Bennu in 2023. It
  contains amino acids and other building blocks of life.
- **Interstellar visitors**: in 2025 the third known interstellar object, comet 3I/ATLAS, was discovered.
- **The loudest black-hole merger yet**: GW250114, detected in January 2025, was clear enough to
  test Hawking's area theorem.
- **Chinese facilities**: LHAASO found many sources of cosmic rays at peta-electron-volt (PeV)
  energies; the Einstein Probe X-ray satellite, launched in 2024, catches short-lived X-ray
  flashes; the FAST radio telescope contributes to pulsar timing.

### 5. The common thread

The biggest change of these five years is not only that we see farther. **Data and tools have
become open to everyone:**

- Survey data is public, with online query services (TAP/ADQL).
- Large collaborations publish compact data products: distance tables, likelihoods, summary
  posteriors.
- So many frontier questions — is dark energy changing, where are the hidden black holes, does
  gravity still follow Newton at the weakest accelerations — can be re-checked, and even pushed
  forward, on a laptop.

That is astrolab's starting point. The next chance is Gaia DR4, on 2 December 2026.

### Further reading

- [ROADMAP.md](https://github.com/sudoghut/astrolab/blob/main/ROADMAP.md): every milestone, with
  verified references and numbers.
- [Claims registry](https://github.com/sudoghut/astrolab/tree/main/atlas/claims): one file per
  graded conclusion.
- [Study 001 · Gaia dormant black holes](https://github.com/sudoghut/astrolab/tree/main/studies/001-m04-gaia-dormant-black-holes):
  the first completed reproduction.

---

## 中文

### 1. 为什么写这一页

[astrolab](https://github.com/sudoghut/astrolab) 想回答一个简单的问题：只用一台笔记本电脑和一个编程智能体（coding agent），能不能做真正的天文学研究？它的做法有三点：

- **不搬数据，只问问题。** 现代巡天数据动辄 TB 级，电脑装不下。astrolab 把查询发到数据中心，筛选和统计都在服务器上做（server-side computation），本地只拿回 MB 级的结果。
- **用复现带动建设。** [路线图（roadmap）](https://github.com/sudoghut/astrolab/blob/main/ROADMAP.md)挑了 10 个 2022–2026 年的代表性成果。复现每一个，都会逼出代码需要的一种新能力。
- **结论分等级。** 每条结论（claim）标明是"已坐实（established）""有张力（tension）""初步迹象（hint）""有争议（contested）"还是"被否定（refuted）"，并由自动测试检查。

这一页是背景故事：不用公式，讲讲近五年天文学发生了什么，重点放在 astrolab 正在复现的成果上。文中的里程碑（milestone）编号（M1、M4……）对应路线图。

### 2. 几台新机器改变了一切

2021 年以来的很多突破，都来自一批几乎同时投入使用的新设备：

| 设备 | 作用 | 打个比方 |
|---|---|---|
| **詹姆斯·韦布空间望远镜（JWST, James Webb Space Telescope）**，2021 年 12 月发射 | 在红外波段看最早的星系 | 看宇宙的"婴儿照" |
| **Gaia 卫星**，2022 年发布第三次数据（DR3），2026 年 12 月 2 日发布第四次数据（DR4） | 测量近二十亿颗恒星的位置和运动 | 给银河系做"人口普查" |
| **DESI 暗能量光谱仪（Dark Energy Spectroscopic Instrument）** | 测量几千万个星系的距离 | 绘制宇宙的三维地图 |
| **LIGO、Virgo、KAGRA 引力波探测器** | 接收黑洞碰撞时发出的时空涟漪 | 用"耳朵"听宇宙 |
| **脉冲星计时阵（PTA, Pulsar Timing Array）** | 把银河系里高速自转的脉冲星当作钟 | 一台和银河系一样大的引力波探测器 |
| 欧几里得卫星（Euclid，2023 年发射）、鲁宾天文台（Vera C. Rubin Observatory，2025 年发布首批图像）等 | 新一代巡天，正陆续开始发布数据 | |

这些数据大多**公开**，而且能在线查询。正因为如此，astrolab 这样的笔记本项目才有可能。

### 3. 从整个宇宙到单颗恒星

astrolab 像在线地图一样把宇宙分成几个缩放级别：L0 是整个宇宙，L4 是单颗恒星，X 是横跨各尺度的主题（引力波）。下面也按这个顺序讲。

#### L0 · 整个宇宙：标准模型出现裂缝？

**暗能量在变化吗？（M1，初步迹象）**

宇宙在加速膨胀，推动它的东西被叫作"暗能量（dark energy）"。在宇宙学标准模型（ΛCDM）中，暗能量是一个永远不变的常数。

- DESI 测量的是重子声学振荡（BAO, Baryon Acoustic Oscillations）：早期宇宙在星系分布中"冻结"下来的一种图案。它可以当作一把标准尺，长约 150 百万秒差距（megaparsec），也就是大约 5 亿光年。
- 2024 至 2025 年，DESI 发现：把这把尺子和宇宙微波背景（CMB, Cosmic Microwave Background）、超新星数据放在一起，结果更倾向于暗能量**随时间减弱**。偏好程度为 2.8–4.2σ，取决于用哪一组超新星数据。
- **2026 年这个信号变弱了。** 一组超新星数据重新校准、DESI 对莱曼 α 森林（Lyman-α forest）做了新的分析之后，降到约 3σ。
- 这是当今宇宙学最受关注的问题：可能改写教科书，也可能最终只是校准问题。
- 复现它只需要一张 kB 级的距离表。这是 astrolab 的下一个里程碑。

**哈勃张力（M2，张力）**

宇宙今天膨胀得有多快？两类测量给出的答案不一样：

- 从附近的造父变星（Cepheid variable）和超新星出发，一级一级搭起距离阶梯（distance ladder），得到约 **73** km/s/Mpc。
- 从宇宙微波背景反推（假设 ΛCDM 成立），得到约 **67–68**。
- 两者相差超过 5σ。JWST 复查了哈勃空间望远镜对造父变星的测量，没有发现错误。
- 另一个团队（CCHP）改用红巨星支顶端（TRGB, Tip of the Red Giant Branch）测距，得到约 **70**。

所以争论的一部分，已经从"有没有新物理"转到了"应该用哪些星系来校准"。

**S8 张力在消退（M3，有争议）**

S8 描述物质"抱团"的程度。

- 过去，弱引力透镜（weak gravitational lensing）巡天测得的值，一直比宇宙微波背景的预测略低。
- 2025 年 KiDS 的最终分析与微波背景一致；暗能量巡天（DES, Dark Energy Survey）第六年的结果仍偏低约 2.6σ。

这是一个正在慢慢消失的张力，提醒人们：系统误差（systematic error）常常看起来很像新物理。

#### L1 · 宇宙黎明：JWST 的惊喜（M8）

- JWST 用光谱确认了红移（redshift）z ≈ 14 的星系：JADES-GS-z14-0 和 MoM-z14（z = 14.44）。我们看到的是它们在宇宙大爆炸后约 3 亿年时的样子。
- 意外的是，**亮星系太多了**，早期宇宙比模型预测的更"早熟"。探测本身已坐实，解释仍有争议。
- 可能的解释包括：恒星形成效率更高；或者星系亮度忽明忽暗（burstiness），让我们更容易在它们最亮的时候看到它们。
- 不在路线图里但同样热门：JWST 发现了大量致密的红色天体，被称为**"小红点（Little Red Dots）"**。它们可能是被尘埃或稠密气体包裹的早期黑洞，目前还没有定论。

#### X · 引力波天文学走向成熟

**纳赫兹频段的背景"嗡嗡声"（M9，初步迹象）**

- 2023 年 6 月，四个脉冲星计时阵——北美的 NANOGrav、欧洲的 EPTA、澳大利亚的 PPTA 和中国的 CPTA——同时宣布：脉冲星信号的到达时间存在一种共同的缓慢"抖动"。
- 不同脉冲星之间抖动的关联方式，符合引力波特有的"指纹"：Hellings–Downs 曲线。
- 最可能的来源，是全宇宙超大质量黑洞双星（supermassive black-hole binaries）共同发出的"嗡嗡声"。
- 证据很强，但还没有达到 5σ 的发现标准。

**黑洞的"质量分布图"（M10）**

- 2025 年发布的引力波瞬变源目录 GWTC-4.0，使可信事件的总数达到约两百个。
- 黑洞的质量并不均匀分布：在约 10 倍和 35 倍太阳质量处有"扎堆"，35 倍以上数量迅速下降。
- 其中 GW231123 事件中的黑洞，质量落在普通恒星被认为"造不出来"的区间，即对不稳定性间隙（pair-instability gap）。它们可能是更早一次并合的产物。

#### L3 · 银河系考古

**银河系比想象的轻？（M6，有争议）**

- 天文学家用 Gaia 数据测量银河系外围恒星的转速，发现在距银心 19.5 到 26.5 千秒差距（kpc）之间，转速下降了约 30 km/s。
- 如果照字面理解，银河系的总质量只有约 2×10¹¹ 个太阳，比以往的估计少很多。
- 但用星流（stellar streams）和卫星星系（satellite galaxies）等其他方法，仍然支持更重的暗物质晕（dark matter halo）。问题尚无定论。

**银河系"早熟"（M5，已坐实）**

- 2022 年，Xiang 和 Rix 在 Nature 发表研究：结合中国 LAMOST 光谱巡天和 Gaia，测出约 25 万颗亚巨星（subgiant）的精确年龄。
- 他们发现，银河系厚盘（thick disk）约在 **130 亿年前**就开始形成，比很多人以为的早得多。

**Radcliffe 波（Radcliffe Wave，候选 M11）**

太阳附近有一条波浪形的恒星形成气体云带，长约 9000 光年。2024 年，天文学家发现它还在振荡，就像一道在银河系中传播的波。

#### L4 · 恒星：Gaia 让看不见的东西现形

**休眠黑洞（M4，已坐实；astrolab 已完成 DR3 部分）**

- 2022 年以前发现的恒星级黑洞，几乎都在吞噬伴星、发出 X 射线。
- 但理论认为，银河系里大多数黑洞应该是"安静的"：不吃东西，也不发光。
- Gaia 的办法是：精确测量一颗普通恒星**在天上画出的小椭圆**。如果轨道很大，伴星却看不见，那么伴星很可能是黑洞。
- 用这个办法找到了三个：

| 天体 | 发现年份 | 质量 | 备注 |
|---|---|---|---|
| Gaia BH1 | 2022 | 约 9.6 倍太阳质量 | 距离约 1600 光年，是已知最近的黑洞 |
| Gaia BH2 | 2023 | 约 8.9 倍太阳质量 | |
| Gaia BH3 | 2024 | 约 33 倍太阳质量 | 银河系内已知最重的恒星级黑洞；伴星是一颗古老的贫金属恒星 |

- astrolab 只用 Gaia DR3 的公开轨道数据：
  - BH2 算出 8.5 倍太阳质量，与论文一致；
  - BH1 算出 13.3 倍太阳质量，与论文中"只用天体测量（astrometry-only）"的解（12.8）一致。论文的 9.6 还用了地面视向速度（radial velocity）观测，使结果更精确；
  - 通过服务器端筛选，找回了 El-Badry 等人（2024）的全部 21 个中子星（neutron star）候选体。
- **Gaia DR4 会包含多得多的轨道。** astrolab 的筛选程序已经准备好，可以在 2026 年 12 月 2 日发布当天运行。这是个人研究者少有的、能和大团队一样快的机会。

**用宽双星检验引力（M7，有争议，趋向牛顿引力）**

- 相隔几千个天文单位的双星，彼此之间的引力极弱。修正牛顿动力学（MOND, Modified Newtonian Dynamics）预言：这时的引力会比牛顿定律算出的更强。
- 2023 年，有团队报告了约 1.4 倍的增强；其他团队用更干净的样本，以很高的显著性排除了 MOND。
- 争论的核心在**样本污染**：隐藏的第三颗星，或者两颗毫无关系、只是恰好排在一起的恒星，都会让一对双星看起来"转得太快"。
- Gaia DR4 的逐次观测数据（epoch astrometry）可以揭示隐藏的伴星，有望给这场争论画上句号。

### 4. 路线图之外的其他亮点

这一节根据一般知识概括，**没有**经过 astrolab 的文献核实流程。

- **事件视界望远镜（EHT, Event Horizon Telescope）**：2022 年拍到银河系中心黑洞人马座 A\*（Sagittarius A\*）的第一张照片。
- **系外行星大气**：JWST 清楚地测出其他恒星的行星大气中的二氧化碳等分子。2025 年有研究称在 K2-18b 上发现了可能的生命迹象，引起轰动；多数后续研究认为证据不足。
- **小行星样本**：NASA 的 OSIRIS-REx 于 2023 年带回小行星贝努（Bennu）的样本，其中含有氨基酸等生命的基本原料。
- **星际访客**：2025 年发现第三个已知的星际天体，彗星 3I/ATLAS。
- **迄今最"响亮"的黑洞并合**：2025 年 1 月探测到的 GW250114 信号非常清晰，足以检验霍金面积定理（Hawking's area theorem）。
- **中国设备**：高海拔宇宙线观测站（LHAASO）发现了大量拍电子伏特（PeV）能量的宇宙线源；2024 年发射的爱因斯坦探针（Einstein Probe）X 射线卫星专门捕捉短暂的 X 射线闪光；FAST 射电望远镜参与了脉冲星计时。

### 5. 一条贯穿的线索

这五年最大的变化，不只是看得更远，还有**数据和工具向所有人开放**：

- 巡天数据公开，并配有在线查询服务（TAP/ADQL）。
- 大型合作组主动发布紧凑的数据产品：距离表、似然函数（likelihood）、汇总后验（summary posterior）。
- 因此很多前沿问题——暗能量是否在变化、黑洞藏在哪里、引力在最弱处是否还遵守牛顿定律——都可以在笔记本电脑上复查，甚至向前推进。

这正是 astrolab 的出发点。下一个机会，就是 2026 年 12 月 2 日发布的 Gaia DR4。

### 延伸阅读

- [ROADMAP.md](https://github.com/sudoghut/astrolab/blob/main/ROADMAP.md)：全部里程碑，附已核实的文献和数值。
- [结论登记表（claims registry）](https://github.com/sudoghut/astrolab/tree/main/atlas/claims)：每条带等级的结论一个文件。
- [研究 001 · Gaia 休眠黑洞](https://github.com/sudoghut/astrolab/tree/main/studies/001-m04-gaia-dormant-black-holes)：第一个完成的复现。
