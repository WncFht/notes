---
title: network Cheat Sheet
tags:
  - CheatSheet
categories: 
date: 2025-02-06T10:32:23+08:00
modify: 2025-02-06T10:32:23+08:00
dir: 
share: false
cdate: 2025-02-06
mdate: 2025-02-06
---

# network Cheat Sheet

## DNS

### 更改 DNS

```bash
>  sudo nvim /etc/resolv.conf

> resolvectl status
Global  
        Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported  
 resolv.conf mode: stub  
  
Link 2 (enp4s0)  
   Current Scopes: none  
        Protocols: -DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported  
  
Link 3 (wlp5s0)  
   Current Scopes: DNS  
        Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported  
Current DNS Server: 192.168.124.1  
      DNS Servers: 8.8.8.8 8.8.4.4 192.168.124.1  
  
Link 5 (docker0)  
   Current Scopes: none  
        Protocols: -DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupporte
```

## clash ver rev 全局配置脚本

还没修改

```js
/**
 * 代理规则配置
 * name: 规则名称
 * gfw: 是否被墙，如果为 true 则默认使用代理，如果为 true 则默认不使用代理,可手动切换节点。
 * urls: 规则集链接,可在这个仓库查找 https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Clash/README.md
 * payload: 规则集,如果使用 payload,则 urls 失效。
 * extraProxies: 额外代理,一般不需要,去广告可以加一个REJECT
 * 
 * ts类型,看得懂的可以看，看不懂的就算了。
 * {
 *   name: string,
 *   gfw?: boolean,
 *   urls?: string | string[],
 *   payload?: string | string[],
 *   extraProxies?: string | string[],
 * }[]
 */

/**
 * @type { {name: string,gfw?: boolean,urls?: string | string[],payload?: string | string[],extraProxies?: string | string[]}[] }
 */
const proxyGrepConfig = [
  { name: "广告拦截", gfw: false, extraProxies: "REJECT", urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/AdvertisingLite/AdvertisingLite_Classical.yaml" },
  { name: "linux.do", gfw: false, payload: "DOMAIN-SUFFIX,linux.do" },
  // { name: "linux.do", gfw: false, payload: ["DOMAIN-SUFFIX,linux.do","DOMAIN-SUFFIX,linux.do"] },//例子，多个规则可以用数组 
  { name: "GitHub", gfw: false, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/GitHub/GitHub.yaml" },
  {
    name: "YouTube", gfw: true, urls: [
      "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/YouTube/YouTube.yaml",
      "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/YouTubeMusic/YouTubeMusic.yaml"
    ]
  },
  { name: "Google", gfw: true, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/Google/Google.yaml" },
  { name: "openAi", gfw: true, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/OpenAI/OpenAI.yaml" },
  { name: "Netflix", gfw: true, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/Netflix/Netflix.yaml" },
  { name: "Twitter", gfw: true, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/Twitter/Twitter.yaml" },
  { name: "TikTok", gfw: true, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/TikTok/TikTok.yaml" },
  { name: "Facebook", gfw: true, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/Facebook/Facebook.yaml" },
  { name: "OneDrive", gfw: false, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/OneDrive/OneDrive.yaml" },
  { name: "Microsoft", gfw: false, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/Microsoft/Microsoft.yaml" },
  { name: "Steam", gfw: false, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@release/rule/Clash/Steam/Steam.yaml" },
  { name: "Cloudflare", gfw: false, urls: "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/Clash/Cloudflare/Cloudflare.yaml" },
]


function main(config) {
  // GPL3.0 license. origin https://linux.do/t/topic/328932 (请保留此注释, author 按需修改)
  // author : picpi https://linux.do/t/topic/328932


  const proxies = config.proxies;
  //创建域名规则组
  function createRuleProviderUrl(url) {
    return {
      "type": "http",
      "interval": 86400,
      "behavior": "classical",
      "format": "yaml",
      "url": url
    }
  }
  //创建payload对应的规则
  function createPayloadRules(payload, name) {
    const rules = [];
    const payloads = Array.isArray(payload) ? payload : [payload];
    for (const item of payloads) {
      const p = item.split(",");
      let pushIndex = p.length;
      if (p[p.length - 1].toLocaleLowerCase() == "no-resolve") {
        pushIndex--;
      }
      p.splice(pushIndex, 0, name.replaceAll(",", "-"));
      rules.push(p.join(","));
    }
    console.log(rules);
    return rules;
  }
  //被墙默认规则
  function createGfwProxyGrep(name, addProxies) {
    addProxies = addProxies ? (Array.isArray(addProxies) ? addProxies : [addProxies]) : [];
    return {
      "name": name,
      "type": "select",
      "proxies": [...addProxies, "自动选择(最低延迟)", "负载均衡", "DIRECT"],
      "include-all": true,
    }
  }
  //默认不被墙规则
  function createProxyGrep(name, addProxies) {
    addProxies = addProxies ? (Array.isArray(addProxies) ? addProxies : [addProxies]) : [];
    return {
      "name": name,
      "type": "select",
      "proxies": [...addProxies, "DIRECT", "自动选择(最低延迟)", "负载均衡"],
      "include-all": true,
    }
  }

  const proxyGroups = [];
  const proxyGfwGroups = [];
  const ruleProviders = {};
  const rules = [];
  for (const { name, gfw, urls, payload, extraProxies } of proxyGrepConfig) {
    if (gfw) {
      proxyGfwGroups.push(createGfwProxyGrep(name, extraProxies));
    } else {
      proxyGroups.push(createProxyGrep(name, extraProxies));
    }
    if (payload) {
      rules.push(...createPayloadRules(payload, name));
    } else {
      const urlList = urls ? (Array.isArray(urls) ? urls : [urls]) : [];
      for (const index in urlList) {
        const theUrl = urlList[index];
        const iName = `${name}-rule${index != 0 ? `-${index}` : ''}`;
        ruleProviders[iName] = createRuleProviderUrl(theUrl);
        rules.push(`RULE-SET,${iName},${name}`);
      }
    }
  }


  return {
    mode: "rule",
    "find-process-mode": "strict",
    "global-client-fingerprint": "chrome",
    "unified-delay": true, //更换延迟计算方式，去除握手等额外延迟
    "tcp-concurrent": true, //TCP 并发
    "geox-url": {
      geoip: "https://ghgo.xyz/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip-lite.dat",
      geosite: "https://ghgo.xyz/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geosite.dat",
    },
    dns: {
      enable: true,
      ipv6: true,
      "enhanced-mode": "fake-ip",
      "fake-ip-filter": [
        "*",
        "+.lan",
        "+.local"
      ],
      nameserver: [
        "system",
        "114.114.114.114",
        "223.5.5.5",
        "https://dns.alidns.com/dns-query",//阿里云
        "https://doh.pub/dns-query",//腾讯
      ],
      fallback: [
        "https://1.0.0.1/dns-query",//Cloudflare
        "https://sky.rethinkdns.com",//rethinkdns
        "https://dns.alidns.com/dns-query",//阿里云
        "https://doh.pub/dns-query",//腾讯
      ],
      "fallback-filter": {
        geoip: true,
        "geoip-code": "CN",
        geosite: ["gfw"],
        domain: [
          '+.google.com',
          '+.facebook.com',
          '+.youtube.com',
        ]
      }
    },
    //代理
    proxies: proxies,
    "proxy-groups": [
      {
        "name": "国内网站",
        "type": "select",
        "proxies": ["DIRECT", "自动选择(最低延迟)", "负载均衡"],
        "include-all": true,
        "url": "https://www.baidu.com/favicon.ico"
      },
      ...proxyGroups,
      {
        "name": "国外网站",
        "type": "select",
        "url": "https://www.bing.com/favicon.ico",
        "proxies": ["DIRECT", "自动选择(最低延迟)", "负载均衡"],
        "include-all": true,
      },
      ...proxyGfwGroups,
      {
        "name": "被墙网站",
        "type": "select",
        "proxies": ["自动选择(最低延迟)", "负载均衡", "DIRECT"],
        "include-all": true,
      },
      {
        "name": "自动选择(最低延迟)",
        "type": "url-test",
        "tolerance": 20,
        "include-all": true,
        "url": "https://play-lh.googleusercontent.com/1UF2WCBNl4918bNk8JsILadL9-agIjRtMpdjuPgx2ohsxnQyspdWDwYMquW1-r8mSQOSjSLOY4g=w720-rw",
      },
      {
        "name": "负载均衡",
        "type": "load-balance",
        "include-all": true,
        "hidden": true,
        "strategy": "sticky-sessions",
        "url": "https://play-lh.googleusercontent.com/1UF2WCBNl4918bNk8JsILadL9-agIjRtMpdjuPgx2ohsxnQyspdWDwYMquW1-r8mSQOSjSLOY4g=w720-rw",
      }
    ],
    "rule-providers": ruleProviders,
    rules: [
      ...rules,
      "GEOSITE,gfw,被墙网站",
      "GEOIP,CN,国内网站",
      "MATCH,国外网站"
    ]
  };
}
```

### Reference

- [Clash-Verge-Rev最佳实践](https://bflome.com/archives/clash-verge-best-practice)

## 代理软件

| 软件和下载地址                                                                                                                                  | 支持系统                       | 备注                                                                   | WebDAV同步  | DNS防泄露                                                                                                    | 自定义分流                                                                                                     | 特点                 |
| ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------ |
| ![:star2:](https://linux.do/images/emoji/apple/star2.png?v=12 ":star2:")[V2rayN](https://github.com/2dust/v2rayN)                        | `Win/Mac/Linux`            | PC端强烈推荐                                                              | `💻:✅`    | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 支持测速、支持最新协议（Xhttp） |
| ![:star2:](https://linux.do/images/emoji/apple/star2.png?v=12 ":star2:")[Karing](https://github.com/KaringX/karing)                      | `Win/Mac/IOS/Android/TvOS` | 功能完善，不太美观，安卓有bug [教程](https://karing.app/)                           | 📱:✅      | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 内置DNS测速            |
| ![:star2:](https://linux.do/images/emoji/apple/star2.png?v=12 ":star2:")[mihomo-party](https://github.com/mihomo-party-org/mihomo-party) | `Win/Mac/Linux`            | 界面定制个性化 [教程](https://mihomo.party/)                                  | `💻:✅`    | 仅代理                                                                                                       | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 支持自定义DNS，全局扩展脚本    |
| ![:star2:](https://linux.do/images/emoji/apple/star2.png?v=12 ":star2:")[FlClash](https://github.com/chen08209/FlClash)                  | 全平台                        | 适合新手使用 ，有bug                                                         | `💻📱:✅✅` | 仅代理                                                                                                       | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 支持自定义DNS           |
| [Hiddify](https://github.com/hiddify/hiddify-next/releases)                                                                              | 全平台                        | 使用简单 [教程](https://hiddify.com/)                                      | `💻📱:❌❌` | 仅代理                                                                                                       | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | 内置WARP             |
| [Clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev/releases)                                                           | `Win/Mac/Linux`            | Clash家族用户排名第一 ，但有bug [教程](https://www.clashverge.dev/)               | `💻:❌`    | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | 支持全局扩展脚本           |
| [Pandora-Box](https://github.com/snakem982/Pandora-Box/)                                                                                 | `Win/Mac/Linux`            | 简约，但协议适配不完善                                                          | `💻:❌`    | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | 适合代理抓取             |
| [Nekoray](https://github.com/MatsuriDayo/nekoray)                                                                                        | `Win/Linux`                | 界面功能和v2rayN类似 [教程](https://matsuridayo.github.io/)                   | `💻:❌`    | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | 界面排版老旧             |
| [GUI.for.Clash](https://github.com/GUI-for-Cores/GUI.for.Clash)                                                                          | `Win/Mac/Linux`            | [GUI-for-Cores](https://github.com/GUI-for-Cores)作者维护，有bug，测试时无法正常启动 |           |                                                                                                           |                                                                                                           |                    |
| [GUI.for.Singbox](https://github.com/GUI-for-Cores/GUI.for.SingBox)                                                                      | `Win/Mac/Linux`            | [GUI-for-Cores](https://github.com/GUI-for-Cores)作者维护，仅GUI，内核需要外网下载  | `💻:❌`    | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 有各种小插件             |
| [V2rayNG](https://github.com/2dust/v2rayNG)                                                                                              | `Android`                  | 不是v2rayN子项目，不能共用WebDav                                               | `📱:❌`    | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 好用                 |
| [Nekobox](https://github.com/MatsuriDayo/NekoBoxForAndroid)                                                                              | `Android`                  | 安卓版nekoray，有bug，测试只能通过协议导入 [教程](https://matsuridayo.github.io/)      | `📱:❌`    | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") | 类似v2rayNG同款        |
| [Surfboard](https://github.com/getsurfboard/surfboard)                                                                                   | `Android`                  | 界面美观 [教程](https://manual.getsurfboard.com/)                          | `❌`       | ![:x:](https://linux.do/images/emoji/apple/x.png?v=12 ":x:")                                              | ![:white_check_mark:](https://linux.do/images/emoji/apple/white_check_mark.png?v=12 ":white_check_mark:") |                    |
| [Sing-box](https://sing-box.sagernet.org/)                                                                                               | 全平台                        | 仅内核                                                                  | `💻📱:❌❌` |                                                                                                           |                                                                                                           | 不适合新手              |
| [Surge](https://nssurge.com/)                                                                                                            | `IOS/Mac/Apple TV`         | 苹果系通用，付费版可授权5个设备                                                     |           |                                                                                                           |                                                                                                           |                    |
| [Shadowrocket](https://apps.apple.com/ae/app/shadowrocket/id932747118)                                                                   | `IOS/Mac/Apple TV`         | 最常见，更新最多                                                             |           |                                                                                                           |                                                                                                           |                    |
| [Stash](https://apps.apple.com/us/app/stash-rule-based-proxy/id1596063349)                                                               | `IOS/Apple TV`             | 暂无                                                                   |           |                                                                                                           |                                                                                                           |                    |
| [QuantumultX](https://apps.apple.com/us/app/quantumult-x/id1443988620)                                                                   | `IOS/Mac/Apple TV`         | 暂无                                                                   |           |                                                                                                           |                                                                                                           |                    |
| [Loon](https://apps.apple.com/in/app/loon/id1373567447)                                                                                  | `IOS/Mac/Apple TV`         | 暂无                                                                   |           |                                                                                                           |                                                                                                           |                    |
| [LanceX (小长矛)](https://apps.apple.com/us/app/lancex/id1536754048)                                                                        | `IOS/Mac`                  | 暂无                                                                   |           |                                                                                                           |                                                                                                           |                    |
| [V2rayU](https://github.com/yanue/V2rayU/tree/master)                                                                                    | `Mac`                      | 暂无                                                                   |           |                                                                                                           |                                                                                                           |                    |
| Passwall                                                                                                                                 | 路由器                        | openwrt内置                                                            |           |                                                                                                           |                                                                                                           |                    |
