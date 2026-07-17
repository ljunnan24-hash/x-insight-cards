<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>把 X 上真正有认知增量的内容，变成来源可核验、中文排版准确的双语卡片。</strong><br />
  <strong>Turn high-signal X posts into verified, well-typeset bilingual creator assets.</strong>
</p>

<p align="center"><a href="README.md">English</a></p>

## 创作者实测 · Creator-tested result

| **9,545 播放 · plays** | **358 赞 · likes** | **42 收藏 · saves** | **+5,990 额外浏览奖励 · bonus views** |
| ---: | ---: | ---: | ---: |

一条使用本工作流制作的抖音视频获得以上数据。公开抖音号：**51536643904**。

One Douyin video made with this workflow achieved the results above. Public Douyin ID: **51536643904**.

> 真实使用结果仅用于证明工作流经过实践，不构成流量承诺。Observed results demonstrate real-world use, not guaranteed future reach.

### 更多创作者实测数据 · More documented creator results

| 平台 · Platform | 截图可核验数据 · Screenshot-verified evidence |
| --- | --- |
| **抖音 · Douyin** | **9,545 播放、358 赞、42 收藏、5,990 额外浏览奖励** · **9,545 plays, 358 likes, 42 saves, 5,990 bonus views** |
| **小红书 · Xiaohongshu** | 五条可见作品案例：**6,536 · 4,271 · 1,775 · 1,584 · 665 浏览** · Five visible post examples: **6,536 · 4,271 · 1,775 · 1,584 · 665 views** |
| **小红书 · Xiaohongshu** | 可见作品含 **153、131、105 赞**；账号累计 **1,511 获赞与收藏** · Visible post likes include **153, 131 and 105**; **1,511 total likes & saves** on the account |

## 一句话介绍 · One-line introduction

**X Insight Cards 是一个经过真实创作者验证的 Codex Skill：从 X 筛选高认知内容，完成来源核验、评分、去重、翻译和中文排版，最终生成可审核的双语卡片与极简配文。**

**X Insight Cards is a creator-tested Codex Skill that discovers high-signal X posts, verifies, scores and deduplicates them, then produces faithful bilingual cards and concise captions for human review.**

## 它解决什么问题

多数内容自动化只追求“多”和“快”，却忽略四件更重要的事：内容是否值得转发、来源是否可靠、中文是否自然、自动化是否越权。

X Insight Cards 提供一条可审计流程：

`发现 → 核验 → 去重 → 评分 → 翻译 → 渲染 → 人工审核`

## 核心卖点

- **不是热度搬运器**：100 分评分，只选达到 75 分的内容，不够 5 条就少发。
- **来源可追溯**：核验链接、作者、账号、英文原文、日期和必要浏览量。
- **中文排版专业**：英文原帖格式不动，中文单向匹配；点号、引号、破折号和省略号遵循简体中文横排规则。
- **默认保护账号**：不读取 Cookie，不绕过验证码，不自动上传或发布。
- **Skill + 脚本双入口**：Codex 用户直接调用，普通用户也能运行 Python 渲染器。
- **真实创作者验证**：抖音单条作品达到 9,545 播放、358 赞、42 收藏，并获得 5,990 额外浏览奖励；小红书另有五条可见作品取得 6,536、4,271、1,775、1,584、665 浏览，账号累计 1,511 获赞与收藏。公开抖音号 51536643904；数据仅作使用证明，不承诺流量。

## 安装 Skill

```bash
git clone https://github.com/ljunnan24-hash/x-insight-cards.git
cd x-insight-cards
./scripts/install-skill.sh
```

在 Codex 中输入：

```text
Use $x-insight-cards 搜索今天关于注意力、习惯、自由和长期主义的优质内容，
核验来源后生成得分最高的 5 张中英双语卡片和简短配文。
```

## 只运行渲染器

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python skills/x-insight-cards/scripts/render_card.py \
  --input examples/demo-post.json \
  --output examples/demo-card.png
```

![虚构内容演示卡片](examples/demo-card.png)

演示作者和内容均为虚构，不包含第三方头像或原帖。

## 评分标准

| 维度 | 分值 |
| --- | ---: |
| 认知增量 | 30 |
| 一句话表达清晰度 | 20 |
| 中文社媒适配度 | 20 |
| 作者与来源可信度 | 15 |
| 新鲜度 | 10 |
| 画面可读性 | 5 |

## 权限边界

- 不内置或导出 Cookie、密码、Token。
- 不绕过登录、验证码、风控或速率限制。
- 不自动打开发布页、创建草稿或发布。
- 不附带第三方原帖、作者头像、平台截图或系统字体。
- 重排卡片必须标记为“重排渲染”，不得冒充原生截图。

## 贡献

欢迎提交 Issue 和 PR，尤其是 Windows/Linux 中文字体适配、中文换行、排版质检和评分方法改进。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果它帮你省掉了重复搭工作流的时间，欢迎点一个 Star，让更多中文创作者看到一种更安全、更重质量的内容自动化方式。

## 许可证

代码与原创文档采用 MIT License。详见 [LICENSE](LICENSE) 与 [NOTICE.md](NOTICE.md)。
