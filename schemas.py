#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公文数据校验 Schema - 基于 Pydantic V2

严格执行 GB/T 9704-2012 规范的字段校验
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ContentBlock(BaseModel):
    """正文层级块"""
    level: int = Field(ge=0, le=4, description="层级：0=正文, 1=一级标题, 2=二级标题, 3=三级标题, 4=四级标题")
    text: str = Field(min_length=1, description="文本内容")
    index: Optional[str] = Field(default=None, description="序号（如：一、（一）、1.、(1)）")


class GongwenData(BaseModel):
    """公文数据模型"""
    company_name: str = Field(default="某某某某集团有限公司", max_length=50, description="发文机关名称")
    doc_number: Optional[str] = Field(default=None, description="发文字号")
    title: str = Field(min_length=2, max_length=50, description="公文标题（必填）")
    recipient: Optional[str] = Field(default=None, description="主送机关")
    content_blocks: List[ContentBlock] = Field(default_factory=list, description="正文层级列表")
    signatures: List[str] = Field(default_factory=list, description="落款机关列表")
    date: Optional[str] = Field(default=None, description="成文日期")
    issuer_name: Optional[str] = Field(default=None, description="签发人姓名（上行文专用）")
    copy_to: Optional[str] = Field(default=None, description="抄送机关")
    issuer: Optional[str] = Field(default=None, description="印发机关")
    issue_date: Optional[str] = Field(default=None, description="印发日期")
    seal_path: Optional[str] = Field(default=None, description="印章图片路径")

    @field_validator('doc_number')
    @classmethod
    def validate_doc_number(cls, v):
        """验证发文字号格式"""
        if v and '〔' not in v:
            raise ValueError("发文字号必须包含年份标记〔〕")
        return v

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """验证标题"""
        if not v.strip():
            raise ValueError("标题不能为空")
        return v.strip()


def validate_gongwen_data(data: dict) -> GongwenData:
    """
    校验公文数据

    Args:
        data: 原始数据字典

    Returns:
        GongwenData: 校验后的数据模型

    Raises:
        ValidationError: 数据校验失败时抛出
    """
    return GongwenData(**data)


# 用于 API 的错误响应格式
def format_validation_error(error) -> dict:
    """格式化校验错误为标准响应"""
    errors = []
    for err in error.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "type": err["type"]
        })
    return {
        "success": False,
        "error": "数据校验失败",
        "details": errors
    }
