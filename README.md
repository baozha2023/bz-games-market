# BZ Games Market

BZ-Games 官方游戏市场索引仓库，为 [BZ-Games](https://github.com/baozha2023/bz-games) 客户端提供官方市场、外部市场目录和游戏下载元数据。

客户端只接受严格数值 `schemaVersion: 2`。Schema 1.x、字符串版本、缺失版本或包含旧字段结构的索引均不会被兼容解析。

## 文件结构

```text
bz-games-market/
├─ market.json          # 官方目录与官方市场索引
├─ get-zip-meta.py      # 计算安装包 SHA-256 和字节数
├─ .github/workflows/   # 推送后同步 market.json 到 OSS
└─ README.md
```

## 官方市场的语言政策

官方市场目前只维护默认简体中文：

```json
{
  "defaultLocale": "zh-CN",
  "localizations": {
    "zh-CN": {
      "name": "示例游戏",
      "summary": "中文简介",
      "tags": ["单人"]
    }
  }
}
```

不要在官方市场中添加空的、机器占位的其他语言包。第三方市场和 GitHub Release 市场维护完整的五种语言：`zh-CN`、`zh-TW`、`en-US`、`ja-JP`、`de-DE`。

客户端请求的语言未在某个游戏中声明时，会把游戏名称、摘要、标签、版本描述和更新说明整体回退到该游戏的 `defaultLocale`，不会逐字段混合语言。

## 顶层结构

官方 `market.json` 是唯一同时包含市场目录 `sources` 和官方游戏索引 `games` 的文档：

```json
{
  "schemaVersion": 2,
  "marketId": "official",
  "marketName": "BZ Games Market",
  "generatedAt": "2026-05-15T12:00:00Z",
  "updatedAt": "2026-08-26T13:31:41.932Z",
  "repository": "https://github.com/baozha2023/bz-games-market.git",
  "author": "baozha2023",
  "sources": [
    {
      "marketId": "official",
      "marketName": "BZ Games Market",
      "generatedAt": "2026-05-15T12:00:00Z",
      "repository": "https://github.com/baozha2023/bz-games-market.git",
      "branch": "master",
      "featured": true,
      "visibility": "public"
    }
  ],
  "games": []
}
```

| 字段            | 类型             | 必填 | 说明                                                          |
| :-------------- | :--------------- | :--- | :------------------------------------------------------------ |
| `schemaVersion` | number           | 是   | 必须精确为数值 `2`                                            |
| `marketId`      | string           | 是   | 官方市场稳定 ID，必须与 `sources` 中恰好一个同 ID source 关联 |
| `marketName`    | string           | 是   | 市场显示名称，不参与本地化                                    |
| `generatedAt`   | ISO-8601 string  | 是   | 市场首次生成时间，普通内容更新时保持不变                      |
| `updatedAt`     | ISO-8601 string  | 是   | 本次索引内容更新时间，修改游戏或版本后更新为当前 UTC 时间     |
| `repository`    | HTTPS GitHub URL | 否   | 当前市场仓库地址                                              |
| `author`        | string           | 否   | 市场维护者                                                    |
| `sources`       | Source[]         | 是   | 市场目录，至少包含官方市场且 `marketId` 全局唯一              |
| `games`         | Game[]           | 是   | 官方市场游戏列表                                              |

更新规则：只更新 `updatedAt`；不要因为编辑游戏、版本或 source 而修改 `generatedAt`。

## Source 结构

```json
{
  "marketId": "third-party",
  "marketName": "Third-party-market",
  "coverUrl": "http://cdn.bzgames.top/bz-games-third-party-market/cover.png",
  "generatedAt": "2026-05-27T08:00:00Z",
  "repository": "https://github.com/baozha2023/bz-games-third-party-market.git",
  "branch": "master",
  "featured": true,
  "visibility": "public"
}
```

| 字段          | 类型                 | 必填 | 说明                                                           |
| :------------ | :------------------- | :--- | :------------------------------------------------------------- |
| `marketId`    | string               | 是   | 稳定市场 ID；路由、IPC、安装任务、任务恢复和论坛引用均使用此值 |
| `marketName`  | string               | 是   | 市场显示名称，不参与本地化                                     |
| `coverUrl`    | URL                  | 否   | 市场封面                                                       |
| `generatedAt` | ISO-8601 string      | 是   | 该市场首次生成时间                                             |
| `repository`  | HTTPS GitHub URL     | 是   | 只接受规范的 GitHub 仓库地址                                   |
| `branch`      | string               | 是   | Git 分支名                                                     |
| `featured`    | boolean              | 否   | 是否重点展示                                                   |
| `visibility`  | `public` \| `hidden` | 否   | source 可见性                                                  |

禁止使用数组下标识别市场，也不存在 `sourceIdx` 兼容逻辑。`marketId` 必须唯一且长期稳定。

## Game Schema 2

```json
{
  "id": "com.bz.example",
  "defaultLocale": "zh-CN",
  "localizations": {
    "zh-CN": {
      "name": "示例游戏",
      "summary": "游戏简介",
      "tags": ["益智", "单人"]
    }
  },
  "author": "BZ-Games Team",
  "author_url": "https://github.com/baozha2023",
  "type": "singleplayer",
  "iconUrl": "https://example.com/icon.png",
  "coverUrl": "https://example.com/cover.png",
  "screenshots": ["https://example.com/screenshot.png"],
  "featured": false,
  "visibility": "public",
  "latestVersion": "1.0.0",
  "versions": []
}
```

| 字段                        | 必填 | 说明                                                             |
| :-------------------------- | :--- | :--------------------------------------------------------------- |
| `id`                        | 是   | 反向域名格式的稳定游戏 ID，必须与安装后 Manifest 一致            |
| `defaultLocale`             | 是   | 默认语言，必须存在于 `localizations`                             |
| `localizations`             | 是   | 游戏语言包；每种语言必须完整提供 `name`、`summary`、`tags`       |
| `author`                    | 是   | 作者或工作室，不参与本地化                                       |
| `author_url`                | 否   | 作者主页                                                         |
| `type`                      | 是   | `singleplayer`、`multiplayer`、`singlemultiple` 或 `networkgame` |
| `iconUrl` / `coverUrl`      | 否   | HTTP(S) 或平台托管资源地址                                       |
| `screenshots`               | 否   | HTTPS 截图列表                                                   |
| `featured`                  | 否   | 是否重点展示                                                     |
| `visibility`                | 否   | `public`、`hidden` 或 `deprecated`                               |
| `minPlayers` / `maxPlayers` | 否   | 多人游戏人数范围                                                 |
| `latestVersion`             | 是   | 必须引用 `versions` 中存在的稳定版本                             |
| `versions`                  | 是   | 至少一个版本                                                     |

`name`、`summary` 和 `tags` 不允许继续出现在 Game 顶层。标签也是本地化内容，市场展示与搜索使用当前语言投影后的标签。

## Version Schema 2

```json
{
  "version": "1.0.0",
  "platformVersion": ">=4.0.0",
  "downloadUrl": "https://example.com/game.zip",
  "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "size": 123456,
  "publishedAt": "2026-08-26T00:00:00.000Z",
  "localizations": {
    "zh-CN": {
      "description": "首个版本",
      "releaseNotes": "首次发布"
    }
  },
  "isPrerelease": false
}
```

| 字段              | 必填   | 说明                                                                                      |
| :---------------- | :----- | :---------------------------------------------------------------------------------------- |
| `version`         | 是     | SemVer 版本，必须与最终 Manifest 一致                                                     |
| `platformVersion` | 是     | 客户端 SemVer 范围                                                                        |
| `downloadUrl`     | 通常是 | HTTP(S) 或平台托管安装包地址；仅 manifest-only 网络游戏可省略                             |
| `sha256`          | 否     | 64 位十六进制 SHA-256，强烈建议填写                                                       |
| `size`            | 是     | 安装包字节数；GitHub Release 直链可由平台解析                                             |
| `publishedAt`     | 否     | 发布时间                                                                                  |
| `localizations`   | 是     | 必须与所属 Game 使用完全相同的语言集合；每种语言提供 `description`，可提供 `releaseNotes` |
| `isPrerelease`    | 否     | 预发布标记                                                                                |
| `gameManifest`    | 否     | 从市场数据重新生成 `game.json` 的 Manifest override                                       |

`description` 和 `releaseNotes` 不允许继续出现在 Version 顶层。

## Game Manifest V1/V2

未填写 `gameManifest` 时，平台读取安装包中原有的 `game.json`：

- 精确数值 `manifestVersion: 2` 按 Manifest V2 严格解析。
- 未声明或不等于数值 2 时按长期保留的 Manifest V1 解析。

填写 `gameManifest` 时，平台不会覆盖或合并安装包中的旧文件，而是：

1. 删除解压暂存目录内原有的 `game.json`；
2. 根据市场 Game、Version 和 `gameManifest` 从零构造新 Manifest；
3. 使用完整 Manifest Schema 校验；
4. 加密新 `game.json` 后导入游戏库。

平台解析层允许 V1/V2 override；本仓库新增 override 时统一使用 Manifest V2，并显式填写：

```json
{
  "manifestVersion": 2,
  "entry": "index.html"
}
```

V2 override 自动从市场 `localizations` 注入每种语言的游戏名和简介。若声明成就或统计，还必须在 override 的每种语言包中完整提供对应稳定 ID 的显示文本。

```json
{
  "manifestVersion": 2,
  "entry": "game.exe",
  "statistics": [{ "id": "score", "mode": "full" }],
  "achievements": [
    { "id": "first_win", "icon": "first-win.png", "hidden": true }
  ],
  "localizations": {
    "zh-CN": {
      "statistics": { "score": "得分" },
      "achievements": {
        "first_win": {
          "title": "初次胜利",
          "description": "完成第一局游戏"
        }
      }
    }
  }
}
```

V2 成就定义可声明可选布尔字段 `hidden`，省略时默认为 `false`。`hidden: true` 的成就在解锁前由平台显示默认奖杯，并按本地化标题和描述的 Unicode 字素簇逐个替换为问号（保留空白，Emoji 与组合字符各计一个）；解锁后再显示真实文案与可选图标。隐藏成就仍计入总数和进度，官方市场管理端提供“隐藏成就”开关，Relay 会拒绝非布尔值。

## 安装包与校验

- 安装包使用 `.zip` 或 `.7z`。
- 未填写 `gameManifest` 时，压缩包根目录或唯一第一层目录必须包含合法的 V1/V2 `game.json`。
- 填写 `gameManifest` 时，原有 `game.json` 会被删除，不会透传未声明字段。
- Manifest 的 `id`、`version` 和 `platformVersion` 必须与市场元数据及当前客户端匹配。
- 安装前校验大小和可用的 SHA-256；解压时拒绝绝对路径、盘符路径和路径穿越。
- 同一 `id + version` 已安装时拒绝重复安装；`networkgame` 同一 ID 只能安装一个版本。

可使用工具生成完整性元数据：

```powershell
python get-zip-meta.py <安装包路径>
```

## 市场加载与隐藏规则

- 客户端优先从 OSS 获取官方 `market.json`，失败后整体切换到 GitHub；不会混用两个来源的目录和官方索引。
- 官方目录和官方索引来自同一次响应，并按索引 `marketId` 查找同 ID source；目录顺序不承载业务身份。
- 外部市场通过 source 的 `repository + branch` 获取 `market.json`，但业务身份始终是稳定 `marketId`。
- 可达但 `schemaVersion !== 2`、结构无效或 `marketId` 不匹配的外部市场会被隐藏。
- 网络失败或超时不会被当成旧协议，source 保留并允许用户重试。
- 原始市场索引按稳定 source 身份缓存；客户端切换语言时只重新生成本地化投影，不重新下载市场。

## 提交前检查

- `schemaVersion` 是数值 `2`。
- `generatedAt` 保持首次生成时间，只刷新 `updatedAt`。
- 所有 `marketId` 唯一，且存在与官方索引同 ID 的 source；不得依赖 source 数组顺序。
- 官方游戏只声明完整 `zh-CN`；每个版本使用相同语言集合。
- Game 顶层没有 `name`、`summary`、`tags`；Version 顶层没有 `description`、`releaseNotes`。
- `latestVersion` 指向实际版本，下载地址、SHA-256 和 size 与文件一致。
- 新增 `gameManifest` override 使用精确数值 `manifestVersion: 2`。
- 隐藏成就仅在 V2 稳定定义中使用布尔字段 `hidden`，不放入语言包。
- 不修改游戏安装包内既有的 Manifest V1；平台仍会正常解析。
