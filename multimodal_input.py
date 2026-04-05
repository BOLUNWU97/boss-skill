#!/usr/bin/env python3
"""
多模态输入处理器 - Multimodal Input Processor
支持图片、截图、PPT等非文本输入
"""

import base64
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import hashlib

class MultimodalProcessor:
    """
    多模态输入处理器
    支持：
    - 图片 (PNG, JPG, etc.)
    - 截图解析
    - 文档图片化
    """
    
    SUPPORTED_TYPES = ["png", "jpg", "jpeg", "gif", "webp", "bmp"]
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.upload_dir = self.base_dir / ".boss" / "uploads"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 历史记录
        self.history_file = self.upload_dir / "multimodal_history.json"
        self.history = self._load_history()
    
    def _load_history(self) -> dict:
        if self.history_file.exists():
            return json.loads(self.history_file.read_text())
        return {"items": []}
    
    def _save_history(self):
        self.history_file.write_text(json.dumps(self.history, indent=2, ensure_ascii=False))
    
    def process_image(self, image_data: str, source: str = "chat") -> dict:
        """
        处理图片输入
        image_data: 可以是：
        - base64编码的图片
        - 图片URL
        - 本地文件路径
        """
        result = {
            "id": self._generate_id(),
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "type": "image",
            "status": "received",
        }
        
        # 解析图片数据
        if image_data.startswith("data:"):
            # data URI格式
            mime_type = image_data.split(";")[0].replace("data:", "")
            actual_data = image_data.split(",")[1]
            result["mime_type"] = mime_type
            
            # 保存到本地
            file_path = self._save_image(base64.b64decode(actual_data), result["id"], mime_type)
            result["file_path"] = str(file_path)
            result["size"] = os.path.getsize(file_path)
        
        elif image_data.startswith("http"):
            # URL格式
            result["url"] = image_data
            result["status"] = "need_download"
        
        elif os.path.exists(image_data):
            # 本地文件
            with open(image_data, "rb") as f:
                data = f.read()
            file_path = self._save_image(data, result["id"])
            result["file_path"] = str(file_path)
            result["size"] = os.path.getsize(file_path)
        
        else:
            # 假设是base64字符串
            try:
                decoded = base64.b64decode(image_data)
                file_path = self._save_image(decoded, result["id"])
                result["file_path"] = str(file_path)
                result["size"] = os.path.getsize(file_path)
            except Exception as e:
                result["status"] = "error"
                result["error"] = str(e)
                return result
        
        # 添加到历史
        self.history["items"].append(result)
        self._save_history()
        
        return result
    
    def _save_image(self, data: bytes, file_id: str, mime_type: str = None) -> Path:
        """保存图片到本地"""
        # 猜测文件扩展名
        if mime_type:
            ext = mime_type.split("/")[-1]
        else:
            ext = "png"
        
        file_path = self.upload_dir / f"{file_id}.{ext}"
        file_path.write_bytes(data)
        return file_path
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        content = f"{datetime.now().isoformat()}{len(self.history['items'])}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def describe_image(self, image_path: str) -> str:
        """
        生成图片描述
        注意：这个只是模拟，实际需要调用图像识别API
        """
        return f"[图片描述工具] 请使用 image() 函数获取图片详细内容"
    
    def get_history(self, limit: int = 10) -> List[dict]:
        """获取历史记录"""
        return self.history["items"][-limit:]
    
    def get_status(self) -> str:
        """获取状态"""
        total = len(self.history["items"])
        
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║               🖼️  多模态输入状态                           ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║ 已处理项目：{total:<45}║",
            f"║ 存储目录：{str(self.upload_dir):<45}║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║ 支持格式：PNG, JPG, GIF, WebP, BMP                           ║",
            "║ 用途：截图、PPT、文档、邮件图片等                            ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║ 使用方式：                                                    ║",
            "║   直接发送图片即可，老板会'看到'并评论                       ║",
            "║   截图给老板看，让他审阅                                     ║",
            "╚══════════════════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="多模态输入处理器")
    parser.add_argument("--base-dir", default=".", help="基础目录")
    parser.add_argument("--action", choices=["status", "history", "describe"], required=True)
    parser.add_argument("--image")
    parser.add_argument("--limit", type=int, default=10)
    
    args = parser.parse_args()
    processor = MultimodalProcessor(args.base_dir)
    
    if args.action == "status":
        print(processor.get_status())
    
    elif args.action == "history":
        items = processor.get_history(args.limit)
        print(f"📋 最近 {len(items)} 个项目：")
        for item in items:
            print(f"  [{item['id']}] {item['type']} - {item['timestamp'][:19]}")
    
    elif args.action == "describe":
        if args.image:
            desc = processor.describe_image(args.image)
            print(desc)
        else:
            print("请提供图片路径")


if __name__ == "__main__":
    main()
