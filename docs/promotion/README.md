# 公文渲染引擎 V14 宣传图片

本目录包含项目宣传图片的HTML模板，可通过浏览器直接查看或截图使用。

## 包含的图片

### 1. 项目Banner
- 文件位置: promo-images.html (第一个卡片)
- 尺寸建议: 1400x400px
- 用途: GitHub README头部、项目首页

### 2. 红头效果对比图
- 文件位置: promo-images.html (第二个卡片)
- 尺寸建议: 1200x600px
- 用途: 展示修复效果、文档说明

### 3. 架构流程图
- 文件位置: promo-images.html (第三个卡片)
- 尺寸建议: 1200x500px
- 用途: 技术文档、架构说明

### 4. 公文样式示例
- 文件位置: promo-images.html (第四个卡片)
- 尺寸建议: 1200x700px
- 用途: 效果展示、用户文档

## 使用方法

### 方法一: 浏览器查看
直接在浏览器中打开 `promo-images.html` 文件，每个图片设计都在独立的卡片中展示。

### 方法二: 截图导出
1. 打开HTML文件
2. 使用浏览器开发者工具 (F12)
3. 选中需要导出的卡片元素
4. 右键选择"Capture node screenshot"（Chrome）或类似功能

### 方法三: Puppeteer脚本导出PNG
```bash
# 安装Puppeteer
npm install puppeteer

# 运行导出脚本
node export-images.js
```

### 方法四: 在线工具
使用在线HTML转图片工具，如:
- https://www.screely.com/
- https://carbon.now.sh/

## 配色方案

| 颜色 | 用途 | HEX |
|------|------|-----|
| 公文红 | 主色调 | #c41e3a |
| 深红 | 渐变 | #8b0000 |
| 背景 | 深色背景 | #0f1419 |
| 卡片背景 | 内容区 | #1a1f2e |
| 成功绿 | 正确状态 | #00cc66 |
| 错误红 | 错误状态 | #ff4444 |

## 修改建议

如需修改设计，直接编辑 `promo-images.html` 文件中的CSS样式即可：

- 修改颜色: 搜索 `#c41e3a` 替换为其他颜色
- 修改字体: 已引入 Google Fonts 的 Noto Sans SC
- 修改布局: 调整 `.promo-card` 和内部元素的CSS

## GitHub链接

项目地址: https://github.com/jaxky2012/gongwen-engine-open

---

**注意**: 建议在实际使用前在真实浏览器中预览效果，以确保渲染正确。
