# BZ Games Market

游戏市场索引仓库，为 [BZ Games](https://github.com/baozha2023/bz-games) 平台提供游戏下载目录。

## 文件结构

```
bz-games-market/
├── market.json          # 市场索引（唯一需提交的配置文件）
├── get-zip-meta.py      # 工具脚本：获取 zip 的 sha256 和 size
├── .gitignore           # 仅允许 market.json 提交
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

### Game 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 唯一标识，格式 `com.bz.gamename` |
| `name` | string | 是 | 游戏名称 |
| `author` | string | 是 | 作者 |
| `type` | string | 是 | 类型：`singleplayer` / `multiplayer` / `singlemultiple` / `networkgame` |
| `summary` | string | 是 | 简要介绍，最多 200 字 |
| `tags` | string[] | 否 | 标签列表 |
| `iconUrl` | string | 否 | 图标 URL |
| `coverUrl` | string | 否 | 封面 URL |
| `screenshots` | string[] | 否 | 截图 URL 列表 |
| `featured` | boolean | 否 | 是否为推荐游戏 |
| `visibility` | string | 否 | `public` / `hidden` / `deprecated` |
| `minPlayers` | number | 否 | 最小玩家数 |
| `maxPlayers` | number | 否 | 最大玩家数 |
| `latestVersion` | string | 是 | 最新版本号（语义化版本） |
| `versions` | Version[] | 是 | 版本列表，至少 1 个 |

### Version 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `version` | string | 是 | 版本号，格式 `X.Y.Z` |
| `description` | string | 是 | 版本描述 |
| `platformVersion` | string | 是 | 平台兼容版本，如 `>=1.0.0` |
| `downloadUrl` | string | 是 | 下载地址（仅支持 `.zip`） |
| `sha256` | string | 是 | 文件 SHA-256 校验值（64 位 hex） |
| `size` | number | 是 | 文件大小（字节） |
| `publishedAt` | string | 否 | 发布时间（ISO 8601） |
| `releaseNotes` | string | 否 | 发布说明 |
| `isPrerelease` | boolean | 否 | 是否为预发布版本 |

## 工作流程

### 1. 准备游戏包

将游戏目录打包为 zip：

```
游戏名称/
├── game.json      # 游戏清单文件
├── index.html     # 入口文件
└── ...            # 其他游戏资源
```

### 2. 获取文件元信息

```bash
python get-zip-meta.py /path/to/game.zip
```

输出示例：

```json
{"sha256": "b8111136a43e2deaff137bcb1b095205c5788096f69800230fdc695061ef78e0", "size": 1100914}
```

### 3. 上传到 OSS

将 zip 上传至阿里云 OSS，获取下载地址。

### 4. 更新 market.json

在 `market.json` 中添加或更新游戏条目，填入上一步获取的 `downloadUrl`、`sha256` 和 `size`。

### 5. 提交到 GitHub

```bash
git add market.json
git commit -m "update market.json"
git push origin master
```

推送后，GitHub Actions 会自动将 `market.json` 同步到 OSS 作为备用源。

## 双源加载

平台加载 market.json 时采用主备双源策略：

1. **主源**：`raw.githubusercontent.com/baozha2023/bz-games-market/master/market.json`
2. **备用源**：`web-bz.oss-cn-beijing.aliyuncs.com/market.json`

备用源由 GitHub Actions 在每次推送时自动同步。

## .gitignore 规则

仅允许 `market.json` 提交，其他文件（脚本、文档等）均被忽略：

```
get-zip-meta.py
.idea
```

如需提交其他文件，先更新 `.gitignore`。
