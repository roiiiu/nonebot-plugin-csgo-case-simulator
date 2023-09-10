<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-csgo-case-simulator

_✨ NoneBot的CSGO开箱模拟器 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/roiiiu/nonebot-plugin-csgo-case-simulator.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-csgo-case-simulator">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-csgo-case-simulator.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

这是一个 NoneBot 的 CSGO 开箱模拟器插件，目前已支持的功能有：
* 武器箱
* 纪念包
* 多箱连开（最多20）
* 和游戏内完全相同的出货概率

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-csgo-case-simulator

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-csgo-case-simulator
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-csgo-case-simulator
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-csgo-case-simulator
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-csgo-case-simulator
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-plugin-csgo-case-simulator"]
</details>

## 🎉 使用
### 指令表
|        指令        |      别名      | 权限  | 需要@ | 范围  |      说明      |
| :----------------: | :------------: | :---: | :---: | :---: | :------------: |
| open [数量] [名称] |    csgo开箱    | 群员  |  否   | 群聊  |   开启武器箱   |
|       cases        | csgo武器箱列表 | 群员  |  否   | 群聊  | 查看所有武器箱 |
|        svs         | csgo纪念包列表 | 群员  |  否   | 群聊  | 查看所有纪念包 |
|  s_skins [皮肤名]  |  csgo皮肤搜索  | 群员  |  否   | 群聊  |    搜索皮肤    |
### 效果图
![效果图](./screenshot/screenshot.png)
