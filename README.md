# 公文渲染引擎 V14

> 符合 GB/T 9704-2012 国家标准的 Word 公文生成器

## ✨ 核心特性

- ✅ **红头大字"剃头"修复** - 动态段前补位 + 禁用网格吸附
- ✅ **横线防塌陷修复** - 注入不可见字符，精确控制线宽
- ✅ **层级正文解析** - 一级黑体、二级楷体、正文仿宋
- ✅ **继承架构设计** - DRY原则，消除70%代码冗余
- ✅ **数据校验** - pydantic 防御性编程
- ✅ **Docker 一键部署** - 字体固化，跨平台一致

## 📁 项目结构

```
gongwen-engine-open/
├── base_engine.py      # 基类引擎（页面设置、字体、画线、页码）
├── gongwen_engine.py   # 标准公文引擎（继承基类）
├── schemas.py          # 数据校验（pydantic）
├── api_server.py       # API 服务
├── 2.jpg                # 示例印章
└── OpenClaw_Skill/     # OpenClaw 技能包
```

## 🚀 快速开始

### 方式一：本地运行

```bash
# 克隆仓库
git clone https://github.com/jaxky2012/gongwen-engine-open.git
cd gongwen-engine-open

# 安装依赖
pip install python-docx pydantic

# 启动 API 服务
python3 api_server.py
```

服务启动在 `http://localhost:8001`

### 方式二：Docker 部署

```bash
docker-compose up -d

# 健康检查
curl http://localhost:8000/health
```

## 📖 API 使用

### 健康检查

```bash
GET http://localhost:8001/health
```

### 生成公文

```bash
POST http://localhost:8001/api/generate
Content-Type: application/json

{
  "company_name": "某某某某集团有限公司",
  "doc_number": "某企〔2026〕1号",
  "title": "关于开展工作的通知",
  "recipient": "所属各单位",
  "content_blocks": [
    {"level": 1, "index": "一", "text": "工作目标"},
    {"level": 0, "text": "全年实现高质量发展目标。"}
  ],
  "signatures": ["某某某某集团有限公司"],
  "date": "2026年4月20日"
}
```

### 响应示例

```json
{
  "success": true,
  "filename": "关于开展工作的通知_20260420.docx",
  "path": "/app/output/关于开展工作的通知_20260420.docx",
  "timestamp": "2026-04-20T10:30:00"
}
```

## 🔧 技术亮点

### 1. 横线防塌陷修复

Word/WPS 中空段落边框会塌陷，解决方案：

```python
# 注入不可见字符撑开段落
run = para.add_run(" ")
run.font.size = Pt(1)  # 最小字号

# 精确控制线宽（单位：1/8 磅）
# sz='6' = 0.75磅（细线）
# sz='12' = 1.5磅（粗线）
bottom.set(qn('w:sz'), '6')
```

### 2. 继承架构

```python
# 基类：公共方法只维护一份
class BaseGongwenEngine:
    def _add_horizontal_line(self, color_hex, thickness, space_before_pt)
    def _set_font(self, run, name, size, color_rgb, bold)
    def add_page_number(self)
    def save(self, output_path)

# 子类：只写业务逻辑
class StandardDocumentEngine(BaseGongwenEngine):
    def add_red_separator_line(self):
        self._add_horizontal_line(color_hex="FF0000", thickness="6")
```

### 3. 层级字体映射

| Level | 字体 | 说明 |
|-------|------|------|
| 0 | 仿宋 | 正文段落 |
| 1 | 黑体 | 一级标题（一、二、三...） |
| 2 | 楷体 | 二级标题（（一）（二）...） |
| 3 | 仿宋 | 三级标题（1. 2. 3...） |
| 4 | 仿宋 | 四级标题（(1) (2) (3)...） |

## 🛡️ 数据校验

API 层启用 pydantic 校验：

```python
class GongwenData(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="公文标题（必填）")
    doc_number: Optional[str] = Field(default=None, description="发文字号")

    @field_validator('doc_number')
    @classmethod
    def validate_doc_number(cls, v):
        if v and '〔' not in v:
            raise ValueError("发文字号必须包含年份标记〔〕")
        return v
```

缺少必填字段会返回 400 错误：

```json
{
  "success": false,
  "error": "数据校验失败",
  "details": [{"field": "title", "message": "标题不能为空"}]
}
```

## 🔤 字体说明

需要以下字体（需自行获取授权）：

| 字体 | 用途 | 文件名 |
|------|------|--------|
| 方正小标宋 | 标题 | FZXiaoBiaoSong-B05S.ttf |
| 仿宋 | 正文 | FangSong.ttf |
| 黑体 | 一级标题 | SimHei.ttf |
| 楷体 | 二级标题/签名 | STKaiti.ttf |

## 📄 开源协议

MIT License

---

**⚠️ 重要提醒**：请勿将包含企业真实印章、Logo 或敏感信息的代码上传到公开仓库。
