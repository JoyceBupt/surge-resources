# Surge Resources

集中托管 Surge 自定义图标与分流规则。资源公开读取，无需登录或携带 Token。

## Claude 规则

```ini
RULE-SET,https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/rules/Claude.list,Claude,no-resolve
```

详见 [规则来源与覆盖说明](rules/README.md)。仅托管可公开的资源；节点、订阅密钥、证书私钥及完整个人配置不进入此仓库。

## 图标预览

| BoilCloud | KDDI | AT&T | FxTransit |
| --- | --- | --- | --- |
| <img src="icons/boil.png" width="80" alt="BoilCloud"> | <img src="icons/kddi.png" width="120" alt="KDDI"> | <img src="icons/att.png" width="80" alt="AT&T"> | <img src="icons/fxtransit.png" width="80" alt="FxTransit"> |

## 使用

在 Surge 图标选择器支持的图标集导入入口添加：

```text
https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/surge-icons.json
```

也可以直接修改策略组的 `icon-url`。以下片段只展示图标参数，请保留已有组类型、成员和其他设置：

```ini
icon-url=https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/icons/boil.png
icon-url=https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/icons/kddi.png
icon-url=https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/icons/att.png
icon-url=https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/icons/fxtransit.png
```

## 文件结构

```text
icons/                 可直接使用的 PNG
sources/               下载的原始素材
rules/                 自定义规则及来源说明
manifest.json          来源、尺寸、处理方式与 SHA-256
surge-icons.json       图标集订阅
scripts/validate.py    本地与在线校验
.github/workflows/     GitHub Actions 自动校验
THIRD_PARTY_NOTICES.md 品牌与素材来源
LICENSE                原创代码及文档的许可范围
```

原始 PNG 保留其尺寸与比例；FxTransit 从官网 SVG 渲染为 512×512 PNG。KDDI 为横版标识，未拉伸为方形。

## 校验与维护

使用 Python 3 标准库，无第三方依赖：

```sh
python3 scripts/validate.py
python3 scripts/validate_rules.py
python3 scripts/validate.py --remote
python3 scripts/validate_rules.py --remote
```

更新图标时，同步更新原始素材、manifest 中的尺寸及 SHA-256，并运行校验。`main` 链接随更新变化；需要固定版本时，将 URL 中的 `main` 替换为完整提交 SHA。客户端可能缓存旧图标，更新后可重新加载图标或使用提交 SHA 链接。

## 来源与权利

参见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本项目不隶属于相关品牌，也不表示获得品牌背书。仓库仅存放图标和维护文件，不包含代理配置、证书或账户凭据。
