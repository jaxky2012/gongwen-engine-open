---
name: gongwen-engine
description: 公文排版引擎 - 输入JSON数据，输出符合GB/T 9704-2012标准的Word公文。
version: 15.0.0
author: 开源社区
scope: global
api_endpoint: http://localhost:8001/api/generate
trigger:
- "生成公文"
- "红头文件"
- "公文排版"
- "发文"
---

# 公文渲染引擎

## 使用前必须部署

本技能需要本地部署 API 服务。请在终端执行：

```bash
git clone https://github.com/jaxky2012/gongwen-engine-open.git
cd gongwen-engine-open
pip install python-docx
python3 api_server.py
```

服务将在 `http://localhost:8001` 启动。

## 输入示例

```json
{
  "company_name": "某某集团有限公司",
  "doc_number": "某企〔2026〕1号",
  "title": "关于开展工作的通知",
  "recipient": "所属各单位",
  "content_blocks": [
    {"level": 1, "index": "一", "text": "工作目标"},
    {"level": 0, "text": "全年实现高质量发展目标。"}
  ],
  "signatures": ["某某集团有限公司"],
  "date": "2026年4月20日"
}
```

## 输出

Word 文档（.docx），符合 GB/T 9704-2012 国家标准。

## 开源协议

MIT License
