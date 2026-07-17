<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>筛出真正值得分享的 X 内容，生成可直接审核的中英双语卡片。</strong><br />
  <strong>Find the X posts worth sharing. Turn them into bilingual cards ready for review.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#真实创作者工作流">实测数据</a> ·
  <a href="#工作流程">工作流程</a>
</p>

<p align="center">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827" />
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img alt="隐私优先" src="https://img.shields.io/badge/privacy-no%20cookies-16A34A" />
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue" />
</p>

## 它能做什么

**X Insight Cards 是为中文创作者设计的 Codex Skill：自动筛选高价值 X 原帖，核验来源、评分去重，并生成中英双语卡片与极简配文。**

**X Insight Cards is a Codex Skill for Chinese creators who want a repeatable way to turn high-value X posts into source-verified, well-typeset English-Chinese cards.**

`发现 → 核验 → 排序 → 去重 → 翻译 → 排版 → 人工审核`

每次运行会得到：

- 最多 5 条真正达到质量线的内容；不足 5 条绝不凑数。
- 每条 1 张保留作者与来源的中英双语 PNG。
- 每张卡片 1 条可直接复制的极简中文配文。
- 1 份不进入公开交付目录的历史记录，用于去重和审计。

## 快速开始

```bash
git clone https://github.com/ljunnan24-hash/x-insight-cards.git
cd x-insight-cards
./scripts/install-skill.sh
```

然后在 Codex 中输入：

```text
Use $x-insight-cards 搜索今天关于注意力、习惯、自由和长期主义的优质内容，
核验来源后生成最多 5 张中英双语卡片，并为每张卡片写一条极简中文配文。
```

无需再拼装提示词。Skill 已包含完整工作流、评分标准、中文排版规则、渲染器和权限边界。

## 为什么值得用

| 常见问题 | X Insight Cards 的处理方式 |
| --- | --- |
| 热门内容很多，真正有认知增量的很少 | 按认知增量、表达、适配度、可信度、新鲜度和可读性评分 |
| 截图传播丢失作者与上下文 | 保留作者、账号、原帖链接、日期与英文原文 |
| 直译中文生硬，混排字体不协调 | 忠实保留语义和语气，并按简体中文原生规则排版 |
| 日更容易重复旧内容和旧选题 | 按规范化 URL 与正文哈希双重去重 |
| 自动化容易越过账号安全边界 | 只使用公开只读来源，默认停在人工审核 |

## 真实创作者工作流

这不是为了展示而虚构的增长项目，而是从真实中文内容账号的日常工作流中提炼出来的工具。

- **抖音：**一条使用本工作流制作的视频获得 **9,545 播放、358 赞、42 收藏**，并收到平台的 **5,990 额外浏览量奖励**。
- **小红书：**可见作品案例获得 **6,536、4,271、1,775、1,584、665 浏览**；可见点赞包括 **153、131、105 赞**，账号累计 **1,511 获赞与收藏**。
- **公开抖音号：**`51536643904`。

这些数据证明工作流经过真实使用，但不代表未来作品一定获得相同流量。选题、账号基础、发布时间和平台分发仍然会影响结果。

<details>
<summary><strong>Creator-tested evidence in English</strong></summary>

One Douyin video made with the workflow reached **9,545 plays, 358 likes, and 42 saves**, plus **5,990 bonus views**. Documented Xiaohongshu examples reached **6,536, 4,271, 1,775, 1,584, and 665 views**; visible likes include **153, 131, and 105**, while the account shows **1,511 total likes and saves**. These results demonstrate real-world use, not guaranteed future reach.

</details>

## 工作流程

1. 搜索最近 24 小时内容；不足时扩展到 72 小时，再不足时使用未采用过的常青内容。
2. 核验 URL、作者、账号、英文原文、日期和必要浏览量。
3. 排除政治争议、荐股、医疗建议、卖课、搬运和纯情绪鸡汤。
4. 对候选内容进行 100 分评分，低于 75 分直接淘汰。
5. 对照历史记录，排除重复 URL、重复正文和重复选题。
6. 忠实翻译，并让中文排版单向匹配英文原帖的视觉格式。
7. 渲染卡片、生成一至两句配文、完成质检，停在人工审核。

如果只有 3 条达到 75 分，就只交付 3 条。质量优先于数量。

## 评分标准

| 维度 | 分值 |
| --- | ---: |
| 认知增量 | 30 |
| 一句话表达清晰度 | 20 |
| 中文社媒适配度 | 20 |
| 作者与来源可信度 | 15 |
| 新鲜度 | 10 |
| 画面可读性 | 5 |

## 中文排版不是附加项

英文原帖是固定视觉基准。中文只单向匹配英文的视觉字号、笔画粗细、行距和颜色，不反向修改英文格式。

- 大陆简体中文横排标点使用字体原生的全角度量。
- 逗号、句号、分号、冒号、问号和叹号保持原生低位。
- 破折号与省略号居中；引号、括号、书名号保持成对字形。
- macOS 默认优先使用 **PingFang SC Regular** 作为中文正文字体。

可通过 `XIC_LATIN_FONT`、`XIC_CJK_FONT` 及对应字体索引变量覆盖默认字体。

## 不安装 Skill，只使用渲染器

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python skills/x-insight-cards/scripts/render_card.py \
  --input examples/demo-post.json \
  --output examples/demo-card.png
```

![虚构内容演示卡片](examples/demo-card.png)

演示作者和内容均为虚构，不包含第三方头像或真实原帖。

## 默认权限边界

- 不读取、导出或保存 Cookie、密码、Token 和会话数据。
- 不绕过登录墙、验证码、风控、速率限制或平台权限。
- 不自动打开发布页、创建草稿、上传或发布。
- 不附带真实 X 原帖、作者头像、平台截图或系统字体。
- 重排卡片必须标记为“重排渲染”，不得冒充原生截图。

发布永远是独立、明确、由用户决定的下一步。

## 贡献

欢迎提交 Issue 和 PR，尤其是 Windows/Linux 中文字体、中文换行、可访问性和评分证据方面的改进。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果它帮你省掉了重复搭建创作者工作流的时间，欢迎点一个 Star，让更多创作者找到它。

## 许可证

代码与原创文档采用 MIT License。详见 [LICENSE](LICENSE) 与 [NOTICE.md](NOTICE.md)。
