# BZ Games Market

游戏市场索引仓库，为 [BZ Games](https://github.com/baozha2023/bz-games) 平台提供游戏下载目录。

## 文件结构

```
bz-games-market/
├── market.json          # 市场索引（唯一必需提交的配置文件）
├── get-zip-meta.py      # 工具脚本：获取 zip 的 sha256 和 size
├── .gitignore
├── .github/workflows/   # GitHub Actions：推送后自动同步到 OSS
└── README.md
```

## market.json 结构

### 顶层结构（市场目录）

`market.json` 位于仓库根目录，作为**市场目录文件**，描述可用的市场源列表，同时包含当前仓库自身的游戏列表。

```json
{
  "schemaVersion": "1.0.0",
  "marketId": "official",
  "marketName": "BZ Games Market",
  "generatedAt": "2026-05-22T04:21:02.000Z",
  "sources": [
    {
      "marketId": "official",
      "marketName": "BZ Games Market",
      "coverUrl": "http://cdn.bzgames.top/bz-games-market/cover.png",
      "generatedAt": "2026-05-22T04:21:02.000Z",
      "repository": "https://github.com/baozha2023/bz-games-market.git",
      "branch": "master",
      "featured": true,
      "visibility": "public"
    }
  ],
  "games": []
}
```

> **注意**：每次更新 `market.json` 后，需同步更新 `generatedAt` 为当前 UTC 时间。
>
> `sources` 数组和 `games` 数组**共存于同一文件**：平台通过 `MarketDirectorySchema` 解析 `sources` 展示市场列表（一级界面），通过 `MarketIndexSchema` 解析 `games` 展示该市场的游戏（二级界面）。

### 顶层字段

| 字段              | 类型          | 必填 | 说明                       |
|-----------------|-------------|----|--------------------------|
| `schemaVersion` | string      | 是  | 索引格式版本，如 `"1.0.0"`       |
| `marketId`      | string      | 是  | 当前市场的唯一标识（与 `sources[0].marketId` 一致） |
| `marketName`    | string      | 是  | 当前市场的显示名称                |
| `generatedAt`   | string      | 是  | 索引生成时间（ISO 8601），每次更新需刷新 |
| `sources`       | Source[]    | 是  | 市场源列表，至少 1 项             |
| `games`         | Game[]      | 是  | 游戏列表（与 `sources[0]` 对应）   |

### Source 字段（sources 数组元素）

每个 source 代表一个独立的市场仓库，平台一级界面展示所有 source。

| 字段            | 类型      | 必填 | 说明                                                                     |
|---------------|---------|----|------------------------------------------------------------------------|
| `marketId`    | string  | 是  | 市场唯一标识                                                                |
| `marketName`  | string  | 是  | 市场显示名称                                                                |
| `coverUrl`    | string  | 否  | 市场封面图远程地址，建议 HTTPS，用于一级界面卡片展示                                           |
| `generatedAt` | string  | 是  | 该市场索引的生成时间（ISO 8601）                                                   |
| `repository`  | string  | 是  | GitHub 仓库地址（仅支持 GitHub），如 `https://github.com/user/repo.git`             |
| `branch`      | string  | 是  | 仓库分支，如 `master` 或 `main`                                               |
| `featured`    | boolean | 否  | 是否在市场列表重点推荐                                                            |
| `visibility`  | string  | 否  | 可见性：`public` / `hidden`（默认 `public`，`hidden` 的 source 不在市场列表中展示）          |

### Game 字段

| 字段              | 类型        | 必填 | 说明                                                                   |
|-----------------|-----------|----|----------------------------------------------------------------------|
| `id`            | string    | 是  | 唯一标识，反向域名格式，如 `com.bz.gamename`。**必须与安装包内 `game.json.id` 完全一致**      |
| `name`          | string    | 是  | 游戏名称，最长 100 字符                                                       |
| `author`        | string    | 是  | 作者/工作室名称                                                             |
| `type`          | string    | 是  | 类型：`singleplayer` / `multiplayer` / `singlemultiple` / `networkgame` |
| `summary`       | string    | 是  | 简要介绍，最多 200 字符                                                       |
| `tags`          | string[]  | 否  | 标签列表，用于市场内搜索                                                         |
| `iconUrl`       | string    | 否  | 图标远程地址，建议 HTTPS                                                      |
| `coverUrl`      | string    | 否  | 封面远程地址，建议 16:9 比例                                                    |
| `screenshots`   | string[]  | 否  | 详情页截图 URL 列表                                                         |
| `featured`      | boolean   | 否  | 是否在市场首页重点推荐                                                          |
| `visibility`    | string    | 否  | 可见性：`public` / `hidden` / `deprecated`（默认 `public`）                  |
| `minPlayers`    | number    | 否  | 多人游戏最小人数（仅 `multiplayer` / `singlemultiple` 建议填写）                    |
| `maxPlayers`    | number    | 否  | 多人游戏最大人数                                                             |
| `latestVersion` | string    | 是  | 当前推荐展示/安装的最新稳定版本号（`X.Y.Z` 格式）                                        |
| `versions`      | Version[] | 是  | 版本列表，至少 1 项                                                          |

### Version 字段

| 字段                | 类型      | 必填 | 说明                                                  |
|-------------------|---------|----|-----------------------------------------------------|
| `version`         | string  | 是  | 版本号，格式 `X.Y.Z`。**必须与安装包内 `game.json.version` 完全一致** |
| `description`     | string  | 是  | 该版本描述（列表与详情页展示）                                     |
| `platformVersion` | string  | 是  | 平台兼容版本，使用 `semver` 语法，如 `>=1.9.4`                   |
| `downloadUrl`     | string  | 是  | 下载地址（支持 `.zip` 和 `.7z` 格式，平台根据后缀自动识别）                    |
| `sha256`          | string  | 是  | 文件 SHA-256 校验值（64 位 hex，大小写不敏感）                     |
| `size`            | number  | 是  | 文件大小（字节），用于展示下载体积与二次校验                              |
| `publishedAt`     | string  | 否  | 发布时间（ISO 8601），如 `"2024-01-15T08:00:00.000Z"`       |
| `releaseNotes`    | string  | 否  | 详细更新说明                                              |
| `isPrerelease`    | boolean | 否  | 是否为预发布版本；预发布版本不作为 `latestVersion`                   |
| `gameManifest`    | object  | 否  | 游戏的 `game.json` 清单覆盖配置，用于无 `game.json` 的第三方游戏适配（详见下方说明） |

## 平台校验规则

平台下载安装时会进行以下校验，**任一失败则拒绝安装**：

| 校验项            | 方式                                                                                               | 错误码                         |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------|
| 平台版本兼容         | 当前平台版本必须满足 `platformVersion`（`semver.satisfies`）                                                 | `platform_version_mismatch` |
| 本地已安装          | 检查本地 `gameRecord` 中是否已存在相同 `id + version`                                                        | `already_installed`         |
| 下载完整性          | 比对下载文件 `sha256` 与索引中的值                                                                           | `verify`                    |
| 文件大小           | 比对下载文件 `size` 与索引中的值                                                                             | `verify`                    |
| 解压结构           | 根目录或第一层单子目录中必须存在 `game.json`；若无，则需在对应版本的 `gameManifest` 字段中配置，平台将自动生成 `game.json` | `extract`                   |
| Manifest ID/版本 | `game.json.id`、`game.json.version` 必须与索引一致                                                       | `install`                   |
| Manifest 平台兼容  | `game.json.platformVersion` 使用 `semver` 做语义化兼容性检查（支持 string 和 tuple `[min, max]` 两种格式），不做字符串直接比对 | `install`                   |

## 安装包约束

- **格式**：支持 `.zip` 和 `.7z`，平台根据 `downloadUrl` 后缀自动识别。`.zip` 使用 `extract-zip`（纯 Node.js）解压，`.7z` 使用内置 `7za` 二进制解压
- **结构**：解压后根目录或第一层单子目录中应包含 `game.json`；平台会自动穿透单层嵌套目录。若无 `game.json`，可在对应版本的 `gameManifest` 字段中配置，平台将自动生成
- **安全**：压缩包内不得出现绝对路径、盘符路径或 `../` 路径穿越条目
- **目录命名**：压缩包解压后的目录结构应能直接作为普通"本地导入"的输入目录
- **幂等性**：若本地已存在相同 `id + version`，视为已安装，不重复覆盖

### 第三方游戏适配（无 `game.json`）

部分第三方游戏压缩包内不包含 `game.json` 文件。为适配此类游戏，可在对应版本的 `gameManifest` 字段中配置所需的清单信息，平台安装时会自动生成 `game.json`。

> **规则**：若解压后不存在 `game.json` 且对应版本的 `gameManifest` 也未配置，则安装失败，提示"该游戏异常，安装失败"，并自动清除下载的游戏文件。

`gameManifest` 包含 `game.json` 中除 `id`（由 Market Game 的 `id` 提供）和 `version`（由当前 Version 的 `version` 提供）之外的所有字段，**均为可选**。未配置的字段将按以下优先级自动回退：

| `gameManifest` 字段 | 回退来源（当未配置时）                    |
|-------------------|----------------------------------|
| `name`            | Market Game 的 `name`             |
| `author`          | Market Game 的 `author`           |
| `type`            | Market Game 的 `type`             |
| `description`     | Market Game 的 `summary`          |
| `platformVersion` | 当前 Version 的 `platformVersion`  |
| `entry`           | 无回退来源，自动检测目录中的入口文件；若无法检测则安装失败 |

`gameManifest` 完整字段列表（均为可选）：

| 字段                   | 类型               | 说明                       |
|----------------------|------------------|--------------------------|
| `name`               | string           | 游戏显示名称                   |
| `description`        | string           | 游戏描述                     |
| `author`             | string           | 作者/工作室名称                 |
| `platformVersion`    | string / [string, string] | 平台兼容版本范围     |
| `entry`              | string           | 启动入口文件或模式（如 `index.html`、`game.exe`、`serve`、`url`） |
| `web_url`            | string           | `entry=url` 时的远程网页地址      |
| `icon`               | string           | 图标文件路径（相对于游戏根目录）         |
| `cover`              | string           | 封面文件路径                   |
| `video`              | string           | 预览视频文件路径                 |
| `encryptLocalStorage`| boolean          | 是否加密本地存储                 |
| `type`               | string           | 游戏类型，同 Market Game 的 `type` |
| `statistics`         | array            | 统计指标列表                   |
| `multiplayer`        | object           | 多人游戏配置 `{minPlayers, maxPlayers}` |
| `args`               | string[]         | Native 游戏启动参数             |
| `env`                 | object           | Native 游戏环境变量             |
| `achievements`       | array            | 成就列表定义                   |

**示例**：一个没有 `game.json` 的第三方游戏版本配置：

```json
{
  "version": "1.0.0",
  "description": "经典消除游戏",
  "platformVersion": ">=1.0.0",
  "downloadUrl": "http://cdn.bzgames.top/bz-games-market/match3/v1.0.0/game.zip",
  "sha256": "a1b2c3d4e5f6...",
  "size": 5242880,
  "publishedAt": "2026-05-15T12:00:00.000Z",
  "gameManifest": {
    "entry": "index.html",
    "icon": "icon.png"
  }
}
```

> 此配置中，`name`、`author`、`type` 等字段将从 Market Game 层级自动继承，无需重复填写。

## 工作流程

### 1. 准备游戏包

将游戏目录打包为 zip 或 7z。压缩包内结构示例：

```
大海世界/
├── game.json      # 游戏清单文件（参考 BZ Games 开发者指南）
├── icon.png       # 图标（可选）
├── cover.png      # 封面（可选）
└── ...            # 其他游戏资源
```

> 也可以直接把 `game.json` 放在压缩包根目录（不加外层文件夹），平台会自动识别。

### 2. 获取文件元信息

```bash
python get-zip-meta.py /path/to/game.zip
```

> 也可用于 `.7z` 文件，将路径替换为 `.7z` 文件即可。

输出示例：

```json
{
  "sha256": "b8111136a43e2deaff137bcb1b095205c5788096f69800230fdc695061ef78e0",
  "size": 1100914
}
```

### 3. 上传到 OSS

将 zip 上传至阿里云 OSS，获取下载地址。建议路径结构：

```
bz-games-market/<游戏名>/v<版本>/<游戏名>.zip
bz-games-market/<游戏名>/icon.png
bz-games-market/<游戏名>/cover.png
```

### 4. 更新 market.json

在 `market.json` 中添加或更新游戏条目，填入上一步获取的 `downloadUrl`、`sha256` 和 `size`。

**重要核对清单**：

- [ ] `id` 与安装包内 `game.json.id` 完全一致
- [ ] `version` 与安装包内 `game.json.version` 完全一致
- [ ] `platformVersion` 使用 `semver` 语法（如 `>=1.9.4`）
- [ ] `sha256` 为 64 位 hex 字符串
- [ ] `size` 为精确字节数
- [ ] 更新 `generatedAt` 为当前 UTC 时间
- [ ] （第三方游戏）若安装包内无 `game.json`，需在对应版本中填写 `gameManifest` 字段

### 5. 提交到 GitHub

```bash
git add market.json
git commit -m "add game: <游戏名> v<版本>"
git push origin master
```

推送后，GitHub Actions 会自动将 `market.json` 同步到 OSS 作为备用源。

## 市场加载策略

平台采用**两级市场架构**：

### 一级：市场列表

平台启动后进入"游戏市场"页面时，加载顶层 `market.json` 解析 `sources` 数组，展示所有可用的市场源。用户点击任意市场进入其游戏列表。

### 二级：游戏列表

进入具体市场后，平台从该市场对应仓库的 `market.json` 拉取游戏索引。第 0 号 source（即顶层 `market.json` 自身）直接使用同文件的 `games` 字段。

### 主备双源

顶层 `market.json` 加载采用主备策略：

1. **主源**（优先级最高）：`https://raw.githubusercontent.com/baozha2023/bz-games-market/master/market.json`
2. **备用源**（主源失败时回退）：`https://web-bz.oss-cn-beijing.aliyuncs.com/market.json`

外部市场源的 `market.json` 从其仓库的 raw 地址直接加载（`https://raw.githubusercontent.com/{owner}/{repo}/{branch}/market.json`）。

### 缓存策略

- 顶层市场列表和市场索引均有 1 小时内存缓存
- 缓存不落盘，应用重启后自动失效
- 用户可点击"刷新"按钮强制拉取最新数据

## 游戏类型说明

| 类型               | 说明                                       |
|------------------|------------------------------------------|
| `singleplayer`   | 单人游戏，不支持联机                               |
| `multiplayer`    | 纯多人游戏，必须联机游玩                             |
| `singlemultiple` | 同时支持单人与联机模式                              |
| `networkgame`    | 网页游戏（`entry=url`），平台直接打开远程网页地址，不参与房间联机流程 |
