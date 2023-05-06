# CSGO-case-simulator-nonebot

## Preview
![screenshot](./screenshot/screenshot1.png)

## Usage
* `/open 数量 箱子` 开箱
* `/cases` 查看箱子
* `/s_search` 搜索皮肤
* `/storage` 查看仓库

## Tips
使用了[supabase]( https://supabase.io/ )作为数据库，需要自己注册账号创建项目, 并配置环境变量.

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run --reload` .

## Documentation

See [Docs](https://v2.nonebot.dev/)
