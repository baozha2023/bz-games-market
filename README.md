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

```json
{
  "schemaVersion": "1.0.0",
  "marketId": "official",
  "marketName": "BZ Games Market",
  "generatedAt": "2026-05-15T12:00:00.000Z",
  "source": {
    "repository": "https://github.com/baozha2023/bz-games-market.git",
    "branch": "master"
  },
  "games": []
}
```

> **注意**：每次更新 `market.json` 后，需同步更新 `generatedAt` 为当前 UTC 时间。

### 顶层字段

| 字段              | 类型     | 必填 | 说明                       |
|-----------------|--------|----|--------------------------|
| `schemaVersion` | string | 是  | 索引格式版本，如 `"1.0.0"`       |
| `marketId`      | string | 是  | 市场唯一标识                   |
| `marketName`    | string | 是  | 市场显示名称                   |
| `generatedAt`   | string | 是  | 索引生成时间（ISO 8601），每次更新需刷新 |
| `source`        | object | 否  | 索引来源仓库信息（诊断用途）           |
| `games`         | Game[] | 是  | 游戏列表                     |

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
| `downloadUrl`     | string  | 是  | 下载地址（当前仅支持 `.zip` 格式，平台根据后缀自动识别）                    |
| `sha256`          | string  | 是  | 文件 SHA-256 校验值（64 位 hex，大小写不敏感）                     |
| `size`            | number  | 是  | 文件大小（字节），用于展示下载体积与二次校验                              |
| `publishedAt`     | string  | 否  | 发布时间（ISO 8601），如 `"2024-01-15T08:00:00.000Z"`       |
| `releaseNotes`    | string  | 否  | 详细更新说明                                              |
| `isPrerelease`    | boolean | 否  | 是否为预发布版本；预发布版本不作为 `latestVersion`                   |

## 平台校验规则

平台下载安装时会进行以下校验，**任一失败则拒绝安装**：

| 校验项            | 方式                                                                                               | 错误码                         |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------|
| 平台版本兼容         | 当前平台版本必须满足 `platformVersion`（`semver.satisfies`）                                                 | `platform_version_mismatch` |
| 本地已安装          | 检查本地 `gameRecord` 中是否已存在相同 `id + version`                                                        | `already_installed`         |
| 下载完整性          | 比对下载文件 `sha256` 与索引中的值                                                                           | `verify`                    |
| 文件大小           | 比对下载文件 `size` 与索引中的值                                                                             | `verify`                    |
| 解压结构           | 根目录或第一层单子目录中必须存在 `game.json`                                                                     | `extract`                   |
| Manifest ID/版本 | `game.json.id`、`game.json.version` 必须与索引一致                                                       | `install`                   |
| Manifest 平台兼容  | `game.json.platformVersion` 使用 `semver` 做语义化兼容性检查（支持 string 和 tuple `[min, max]` 两种格式），不做字符串直接比对 | `install`                   |

## 安装包约束

- **格式**：当前仅支持 `.zip`，平台根据 `downloadUrl` 后缀自动识别
- **结构**：解压后根目录或第一层单子目录中必须包含 `game.json`
- **安全**：压缩包内不得出现绝对路径、盘符路径或 `../` 路径穿越条目
- **目录命名**：压缩包解压后的目录结构应能直接作为普通"本地导入"的输入目录
- **幂等性**：若本地已存在相同 `id + version`，视为已安装，不重复覆盖

## 工作流程

### 1. 准备游戏包

将游戏目录打包为 zip。压缩包内结构示例：

```
大海世界/
├── game.json      # 游戏清单文件（参考 BZ Games 开发者指南）
├── icon.png       # 图标（可选）
├── cover.png      # 封面（可选）
└── ...            # 其他游戏资源
```

### 2. 获取文件元信息

```bash
python get-zip-meta.py /path/to/game.zip
```

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

### 5. 提交到 GitHub

```bash
git add market.json
git commit -m "add game: <游戏名> v<版本>"
git push origin master
```

推送后，GitHub Actions 会自动将 `market.json` 同步到 OSS 作为备用源。

## 双源加载

平台加载 market.json 时采用主备双源策略：

1. **主源**（优先级最高）：`https://raw.githubusercontent.com/baozha2023/bz-games-market/master/market.json`
2. **备用源**（主源失败时回退）：`https://web-bz.oss-cn-beijing.aliyuncs.com/market.json`

平台每次进入"游戏市场"页面都会主动拉取最新索引（不依赖本地缓存），备用源由 GitHub Actions 在每次推送时自动同步。

## 游戏类型说明

| 类型               | 说明                                       |
|------------------|------------------------------------------|
| `singleplayer`   | 单人游戏，不支持联机                               |
| `multiplayer`    | 纯多人游戏，必须联机游玩                             |
| `singlemultiple` | 同时支持单人与联机模式                              |
| `networkgame`    | 网页游戏（`entry=url`），平台直接打开远程网页地址，不参与房间联机流程 |

## .gitignore 规则

```
.idea
*.zip
__pycache__/
```

如需提交新文件类型，先更新 `.gitignore`。
