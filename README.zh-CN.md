<p align="center">
  <img src="assets/hero.svg" alt="X Insight Cards" width="100%" />
</p>

<p align="center">
  <strong>自动搜集 X 优质帖子，并转化为抖音、小红书图文素材的 Codex Skill。</strong><br />
  <strong>A Codex Skill that finds high-quality X posts and turns them into content for Douyin and Xiaohongshu.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#workflow-demo">观看演示</a> ·
  <a href="#creator-tested">实测数据</a> ·
  <a href="https://github.com/ljunnan24-hash/x-insight-cards/releases/latest">最新版本</a>
</p>

<p align="center">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827" />
  <a href="https://github.com/ljunnan24-hash/x-insight-cards/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/ljunnan24-hash/x-insight-cards" /></a>
  <a href="https://github.com/ljunnan24-hash/x-insight-cards/actions/workflows/ci.yml"><img alt="持续集成" src="https://github.com/ljunnan24-hash/x-insight-cards/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://skills.sh/ljunnan24-hash/x-insight-cards/x-insight-cards"><img alt="skills.sh 安装量" src="https://skills.sh/b/ljunnan24-hash/x-insight-cards" /></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
  <img alt="隐私优先" src="https://img.shields.io/badge/privacy-no%20cookies-16A34A" />
  <img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue" />
</p>

<a id="快速开始"></a>

## 安装一次，每天自动运行 · Install once, run every day

**这是一个可安装的 Codex Skill，不是需要自己拼装脚本的模板。** 复制这一条命令：

```bash
npx skills add ljunnan24-hash/x-insight-cards --skill x-insight-cards --agent codex --global --copy --yes
```

把下面这段提示词加入每日 Codex 自动任务；演示采用本地时间 12:00：

```text
使用 $x-insight-cards 寻找今天最好的 X 原帖，生成最多 5 组
可直接审核的抖音、小红书图片与极简中文配文。质检完成后标记为
READY_FOR_REVIEW 并结束；不要打开微信或发送任何消息。微信私有交付
稍后由固定机器人触发。不得自动发布到任何内容平台。
```

安装一次、设置一次定时任务，之后每天自动运行；同时仍支持手动调用。无需 X API Key、无需导出 Cookie、无需自己拼提示词。可选的固定 iLink 审核机器人能够在后台把素材传到手机，不依赖微信桌面端；内容平台发布始终由你手动决定。

<a id="workflow-demo"></a>

## 每日准备，手机触发微信交付 · Daily preparation, phone-triggered WeChat review

![从每日定时准备到微信私有审核的 X Insight Cards 动态工作流](assets/demo-workflow.gif)

这段 13 秒演示从每天 12:00 的 Codex 定时任务开始，以一条真实公开的 [James Clear 帖子](https://x.com/JamesClear/status/2045205241885323635) 为例，依次展示来源核验、评分、去重、卡片生成和私有审核交付。当前首选流程会让定时任务停在 `READY_FOR_REVIEW`；创作者之后在手机上向固定 iLink 机器人发送 `发今日素材`，后台便会发送 PNG 与配文，全程不打开微信桌面端。它不会自动发布到抖音或小红书。

运行 `make demo-gif` 可在本地重新生成这段演示。

### 固定微信 iLink 机器人的无界面交付

首选交付器在配置时固定唯一收件人，发送时不接受临时目标覆盖。后台长轮询只接受该用户发来的精确指令 `发今日素材`，在推进同步游标前先持久记录请求，确认当天审核素材已经完成，再逐组发送图片和配文。稳定消息 ID 与检查点支持断点续传；当天收据会阻止重复发送整批素材。

账号凭据、会话上下文、私有清单、检查点和收据都保存在用户自己的 `~/.weclaw` 私有目录中，不进入 Git。监听器可由 macOS `launchd` 或其他进程守护器持续运行；它不会打开、识别或控制微信桌面端。

```bash
# 一次性固定账号文件和收件人
node skills/x-insight-cards/scripts/wechat_ilink_delivery.mjs configure \
  --credentials /absolute/path/to/account.json \
  --sync /absolute/path/to/account.sync.json \
  --recipient 'fixed-user-id@im.wechat'

# 固定用户先给机器人发消息，然后捕获并预检新鲜上下文
node skills/x-insight-cards/scripts/wechat_ilink_delivery.mjs capture-context
node skills/x-insight-cards/scripts/wechat_ilink_delivery.mjs preflight

# 持续运行；无人值守时交给进程守护器
node skills/x-insight-cards/scripts/wechat_ilink_listener.mjs \
  --history /absolute/path/to/history.jsonl
```

macOS 微信集成主窗口的“文件传输助手”交付器仍作为单独配置、失败即停止的回退方案保留。详见 [`private-delivery.md`](skills/x-insight-cards/references/private-delivery.md)。

## 直接看结果 · See the output

![Skill 生成的中英双语 X 洞察卡片](examples/demo-card.png)

每次定时运行都会得到保留作者与来源的卡片，以及等待创作者审核的极简中文配文。此示例使用真实公开原帖和重排渲染，并以姓名首字母代替第三方头像。

## 它能做什么

**X Insight Cards 自动完成发布前的素材准备：寻找优质 X 原帖、核验来源、评分去重、按需翻译排版，最终生成适合抖音和小红书的图片与极简配文。**

**X Insight Cards automates the work before publishing: it finds strong X posts, verifies and ranks them, removes duplicates, translates when needed, and produces source-attributed images plus concise Chinese captions for Douyin and Xiaohongshu.**

`定时触发 → 发现 → 核验 → 排序 → 去重 → 翻译 → 排版 → READY → 手机指令 → 微信审核`

每次运行会得到：

- 自动发现并排序近期值得做成内容的优质 X 原帖。
- 最多 5 组抖音、小红书素材；不足 5 条绝不凑数。
- 每组包含 1 张保留作者与来源的 PNG，以及 1 条可直接复制的极简中文配文。
- 可选无界面发送到已固定的微信 iLink 审核机器人。
- 1 份不进入公开交付目录的历史记录，用于去重和审计。

<a id="creator-tested"></a>

## 抖音、小红书真实账号实测

这套工作流已经用于真实创作者账号。用户提供的原始截图显示：

| 平台 | 实测数据 |
| --- | --- |
| **抖音账号** | **12 条作品**，累计 **1,591 获赞** |
| **抖音可见作品** | **1.1 万、9,635、1,148、1,063、703、676 播放** |
| **小红书账号** | 累计 **1.7 万获赞与收藏** |
| **小红书可见作品** | **96,225 浏览 / 8,877 赞、13,804 / 1,067、1,907 / 167、1,700 / 141** |

公开账号：抖音号 `51536643904` · 小红书号 `3876991164`。

### 抖音账号与作品表现 · Douyin creator results

<a href="assets/proof/douyin-creator-results.png"><img src="assets/proof/douyin-creator-results-preview.webp" alt="抖音创作者主页与可见作品数据" width="100%" /></a>

抖音号：`51536643904` · README 加载轻量 WebP 预览；点击图片查看原始 PNG。

### 小红书账号与作品表现 · Xiaohongshu creator results

<a href="assets/proof/xiaohongshu-creator-results.png"><img src="assets/proof/xiaohongshu-creator-results-preview.webp" alt="小红书创作者主页与可见作品数据" width="100%" /></a>

小红书号：`3876991164` · README 加载轻量 WebP 预览；点击图片查看原始 PNG。

**English summary:** The Douyin profile shows **12 posts and 1,591 total likes**, with visible posts reaching up to **11K plays**. The Xiaohongshu profile shows **17K total likes and saves**, including a visible post with **96,225 views and 8,877 likes**.

这两张截图已获创作者授权公开，用于证明工作流产出的素材经过真实账号使用，但不代表未来作品一定获得相同流量。点击图片可查看原始分辨率；选题、账号基础、发布时间和平台分发仍然会影响结果。

## 为什么值得用

| 常见问题 | X Insight Cards 的处理方式 |
| --- | --- |
| 每天寻找优质内容素材很耗时 | 自动发现近期 X 原帖，并按认知增量和中文创作适配度评分 |
| 截图传播丢失作者与上下文 | 保留作者、账号、原帖链接、日期与英文原文 |
| 直译中文生硬，混排字体不协调 | 忠实保留语义和语气，并按简体中文原生规则排版 |
| 日更容易重复旧内容和旧选题 | 按规范化 URL 与正文哈希双重去重 |
| 自动化容易越过账号安全边界 | 只使用公开只读来源、固定唯一私有收件人，并且绝不自动发布 |

## 工作流程

1. 从每日 Codex 定时任务开始，也可手动运行。
2. 搜索最近 24 小时内容；不足时扩展到 72 小时，再不足时使用未采用过的常青内容。
3. 核验 URL、作者、账号、英文原文、日期和必要浏览量。
4. 排除政治争议、荐股、医疗建议、卖课、搬运和纯情绪鸡汤。
5. 对候选内容进行 100 分评分，低于 75 分直接淘汰，并对照历史记录去重。
6. 忠实翻译、排版、生成极简配文并完成视觉质检。
7. 启用私有交付时停在 `READY_FOR_REVIEW`；之后由手机发送精确指令，触发后台向固定审核机器人交付。

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

README 顶部使用一条真实公开的 [James Clear 帖子](https://x.com/JamesClear/status/2045205241885323635) 进行重排演示，不包含第三方头像。

## 默认权限边界

- 不读取、导出或保存 Cookie、密码、Token 和会话数据。
- 不绕过登录墙、验证码、风控、速率限制或平台权限。
- 不自动打开发布页、创建草稿、上传或发布。
- 微信交付只允许发送到已核对的“文件传输助手”，并遵守发送前必要确认。
- `assets/proof/` 中两张创作者授权的结果截图仅用于项目说明；仓库不包含账号凭据、私密账号数据或系统字体。
- 重排卡片必须标记为“重排渲染”，不得冒充原生截图。

私下传到手机可自动执行到必要的发送确认；平台发布永远是独立、由用户决定的下一步。

## 贡献

欢迎提交 Issue 和 PR，尤其是 Windows/Linux 中文字体、中文换行、可访问性和评分证据方面的改进。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

如果它帮你省掉了重复搭建创作者工作流的时间，欢迎点一个 Star，让更多创作者找到它。

## 许可证

代码与原创文档采用 MIT License。详见 [LICENSE](LICENSE) 与 [NOTICE.md](NOTICE.md)。
