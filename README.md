# nonebot-plugin-csgo-case-simulator

## Update
* 2023-5-8
  * 支持纪念包开箱
  * 替换json为离线数据
  * 修复了open不带参数可以开箱的bug
  * 新的随机算法

## Preview
![screenshot](./screenshot/screenshot.png)

## Usage
* `/open 数量 箱子` 开箱（最多20）
* `/cases` 查看全部箱子
* `/svs` 查看所有纪念包
* `/s_skin 皮肤名` 搜索皮肤
* `/help` 帮助

## Install
  ```shell
  nb plugin install nonebot-plugin-csgo-case-simulator
  ```
  或者
  ```
 pip install nonebot-plugin-csgo-case-simulator
  ```
 然后在`poetry.toml`中的`plugins`列表中添加`nonebot-plugin-csgo-case-simulator`

## Documentation

See [Docs](https://v2.nonebot.dev/)
