# 自定义分流规则

## Claude.list

用于将 Claude 相关目标交给独立策略组。包含 11 条域名规则和 2 条 IP 规则。规则不包含节点、凭据或具体出口；主配置负责选择策略。

```ini
RULE-SET,https://raw.githubusercontent.com/JoyceBupt/surge-resources/main/rules/Claude.list,Claude,no-resolve
```

将引用放在通用 AI 与海外流媒体规则之前。既有广告规则的优先级由主配置决定；此清单不要求全局放行遥测。

### 依据与限制

核对日期：2026-09-15。

- 核心域名 `anthropic.com`、`claude.ai`、`claude.com`、用户内容 `claudeusercontent.com` 及其子域名：参考 [Anthropic 网络要求](https://code.claude.com/docs/en/network-config)。
- 入站地址 `160.79.104.0/23`、`2607:6bc0::/48`：参考 [Anthropic IP 地址文档](https://platform.claude.com/docs/en/api/ip-addresses)。不将其对外请求的地址范围当作必需入站规则。
- `clau.de`、`claudemcpclient.com`、`claudemcpcontent.com`、Anthropic 专用 Auth0/CDN/Ghost 域名：保留自先前清单，线索来自 [Net.Coffee](https://ip.net.coffee/claude/site.html)。这些是补充候选，不代表全部经过官方确认或实际功能验证。
- 不包含通用 NTP、整站 Google Storage 或全局 Sentry/Datadog 关键词。

本清单不保证覆盖所有版本、第三方插件或 MCP 服务器；新增规则应记录公开依据，并验证实际匹配。`no-resolve` 避免规则主动触发 DNS 解析。
