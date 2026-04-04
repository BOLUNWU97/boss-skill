#!/usr/bin/env python3
"""
Boss Skill Doctor - 健康检查诊断工具
Claude Code /doctor 风格
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


class Doctor:
    """
    Boss Skill 健康检查诊断工具
    
    检查项目：
    - 文件完整性
    - 配置文件
    - 依赖项
    - 数据目录
    - 进化状态
    - 排行榜连接
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.results: List[Dict] = []
    
    def check_all(self) -> Tuple[int, int]:
        """运行所有检查，返回(通过数, 失败数)"""
        checks = [
            ("文件结构", self.check_file_structure),
            ("Boss示例", self.check_boss_examples),
            ("工具脚本", self.check_tools),
            ("进化系统", self.check_evolution_system),
            ("Prompt模板", self.check_prompts),
            ("依赖文件", self.check_dependencies),
            ("配置文件", self.check_config),
            ("数据目录", self.check_data_dirs),
        ]
        
        for name, check_fn in checks:
            result = check_fn()
            self.results.append({"name": name, "result": result})
        
        passed = sum(1 for r in self.results if r["result"]["status"] == "pass")
        failed = sum(1 for r in self.results if r["result"]["status"] == "fail")
        
        return passed, failed
    
    def check_file_structure(self) -> Dict:
        """检查文件结构"""
        required_files = [
            "SKILL.md",
            "README.md",
            "prompts/intake.md",
            "prompts/management_analyzer.md",
            "prompts/boss_persona_analyzer.md",
        ]
        
        missing = []
        for f in required_files:
            if not (self.base_dir / f).exists():
                missing.append(f)
        
        if missing:
            return {
                "status": "fail",
                "message": f"Missing files: {', '.join(missing)}"
            }
        
        return {"status": "pass", "message": "All required files present"}
    
    def check_boss_examples(self) -> Dict:
        """检查Boss示例"""
        bosses_dir = self.base_dir / "bosses"
        if not bosses_dir.exists():
            return {"status": "fail", "message": "bosses/ directory missing"}
        
        bosses = [d for d in bosses_dir.iterdir() if d.is_dir()]
        if not bosses:
            return {"status": "fail", "message": "No boss examples found"}
        
        # 检查每个boss是否有必需文件
        for boss in bosses:
            required = ["meta.json", "persona.md"]
            for f in required:
                if not (boss / f).exists():
                    return {
                        "status": "fail",
                        "message": f"{boss.name} missing {f}"
                    }
        
        return {
            "status": "pass",
            "message": f"{len(bosses)} boss examples: {', '.join(b.name for b in bosses)}"
        }
    
    def check_tools(self) -> Dict:
        """检查工具脚本"""
        tools_dir = self.base_dir / "tools"
        if not tools_dir.exists():
            return {"status": "fail", "message": "tools/ directory missing"}
        
        tools = list(tools_dir.glob("*.py"))
        if not tools:
            return {"status": "fail", "message": "No Python tools found"}
        
        # 检查关键工具
        required_tools = [
            "evolution_logger.py",
            "pattern_detector.py",
            "rl_feedback.py",
        ]
        
        missing = [t for t in required_tools if not (tools_dir / t).exists()]
        if missing:
            return {
                "status": "fail",
                "message": f"Missing tools: {', '.join(missing)}"
            }
        
        return {
            "status": "pass",
            "message": f"{len(tools)} tools: {', '.join(t.name for t in tools[:5])}..."
        }
    
    def check_evolution_system(self) -> Dict:
        """检查进化系统"""
        bosses_dir = self.base_dir / "bosses"
        if not bosses_dir.exists():
            return {"status": "fail", "message": "No bosses directory"}
        
        bosses = [d for d in bosses_dir.iterdir() if d.is_dir()]
        evolution_ok = 0
        
        for boss in bosses:
            evolutions_dir = boss / "evolutions"
            if evolutions_dir.exists():
                evolution_ok += 1
        
        if evolution_ok == 0:
            return {
                "status": "warn",
                "message": "No evolution directories found (may be first run)"
            }
        
        return {
            "status": "pass",
            "message": f"{evolution_ok}/{len(bosses)} bosses have evolution data"
        }
    
    def check_prompts(self) -> Dict:
        """检查Prompt模板"""
        prompts_dir = self.base_dir / "prompts"
        if not prompts_dir.exists():
            return {"status": "fail", "message": "prompts/ directory missing"}
        
        prompts = list(prompts_dir.glob("*.md"))
        if len(prompts) < 5:
            return {
                "status": "warn",
                "message": f"Only {len(prompts)} prompt templates found"
            }
        
        return {
            "status": "pass",
            "message": f"{len(prompts)} prompt templates"
        }
    
    def check_dependencies(self) -> Dict:
        """检查依赖文件"""
        required = ["requirements.txt", "package.json"]
        missing = [f for f in required if not (self.base_dir / f).exists()]
        
        if missing:
            return {
                "status": "warn",
                "message": f"Optional files missing: {', '.join(missing)}"
            }
        
        return {"status": "pass", "message": "All dependency files present"}
    
    def check_config(self) -> Dict:
        """检查配置文件"""
        configs = [
            ".github/workflows/validate.yml",
            "Dockerfile",
        ]
        
        missing = [f for f in configs if not (self.base_dir / f).exists()]
        
        if missing:
            return {
                "status": "warn",
                "message": f"Optional configs missing: {', '.join(missing)}"
            }
        
        return {"status": "pass", "message": "CI/CD configs present"}
    
    def check_data_dirs(self) -> Dict:
        """检查数据目录"""
        bosses_dir = self.base_dir / "bosses"
        if not bosses_dir.exists():
            return {"status": "fail", "message": "No data directory"}
        
        total_size = 0
        file_count = 0
        
        for f in bosses_dir.rglob("*"):
            if f.is_file():
                total_size += f.stat().st_size
                file_count += 1
        
        size_mb = total_size / 1024 / 1024
        
        return {
            "status": "pass",
            "message": f"{file_count} files, {size_mb:.2f}MB"
        }
    
    def print_report(self):
        """打印诊断报告"""
        passed, failed = self.check_all()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🩺  Boss Skill Doctor - 健康检查                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        
        print(f"检查时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
        
        for result in self.results:
            status_icon = {
                "pass": "✅",
                "warn": "⚠️",
                "fail": "❌"
            }.get(result["result"]["status"], "❓")
            
            print(f"{status_icon} {result['name']:<20} {result['result']['message']}")
        
        print(f"\n{'='*60}")
        print(f"\n📊 检查结果: ✅ {passed} passed", end="")
        if failed > 0:
            print(f", ❌ {failed} failed")
        else:
            print()
        
        if failed == 0:
            print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🎉 所有检查通过！你的 Boss Skill 正常运行中               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        else:
            print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ⚠️  有问题需要修复，请检查上面的 ❌ 项                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        
        # 返回退出码
        return 0 if failed == 0 else 1


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Boss Skill Doctor")
    parser.add_argument("--base-dir", default=".", help="Base directory")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    doctor = Doctor(args.base_dir)
    
    if args.json:
        passed, failed = doctor.check_all()
        output = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "passed": passed,
            "failed": failed,
            "results": doctor.results
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if failed == 0 else 1
    else:
        return doctor.print_report()


if __name__ == "__main__":
    sys.exit(main())
