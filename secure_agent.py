#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SecureAgent - 通用安全测试 Agent
================================

用法:
    python secure_agent.py --plugin <plugin> --target <target> [options]
    
示例:
    # LLM 安全测试
    python secure_agent.py --plugin llm_security --target "openai:gpt-4"
    
    # Web 安全扫描
    python secure_agent.py --plugin web_security --target "https://example.com"
    
    # 列出所有插件
    python secure_agent.py --list
"""

import argparse
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core import Scanner


def main():
    parser = argparse.ArgumentParser(
        description="SecureAgent - 通用安全测试 Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--list", "-l", action="store_true",
                       help="列出所有可用插件")
    
    parser.add_argument("--info", "-i", metavar="PLUGIN",
                       help="显示插件详细信息")
    
    parser.add_argument("--plugin", "-p", 
                       help="指定插件名称")
    
    parser.add_argument("--target", "-t",
                       help="扫描目标")
    
    parser.add_argument("--config", "-c", 
                       help="配置文件路径")
    
    parser.add_argument("--output", "-o", default="reports",
                       help="报告输出目录")
    
    parser.add_argument("--format", "-f", 
                       choices=["json", "markdown"],
                       default="json",
                       help="报告格式")
    
    parser.add_argument("--rules", nargs="+",
                       help="指定要执行的规则")
    
    args = parser.parse_args()
    
    # 初始化扫描器
    scanner = Scanner(config_path=args.config)
    
    # 列出插件
    if args.list:
        print("\n" + "="*60)
        print("🔌 SecureAgent 可用插件")
        print("="*60)
        
        plugins = scanner.list_plugins()
        for p in plugins:
            print(f"\n📦 {p['name']} v{p['version']}")
            print(f"   {p['description']}")
            print(f"   规则数: {p['rules_count']}")
            print(f"   作者: {p['author']}")
        
        print("\n" + "="*60)
        return
    
    # 显示插件信息
    if args.info:
        plugin = scanner.get_plugin(args.info)
        if plugin:
            print(f"\n📦 {plugin.name} v{plugin.version}")
            print(f"   {plugin.description}")
            print(f"   作者: {plugin.author}")
            print(f"\n规则列表:")
            for rule in plugin.get_rules()[:10]:
                print(f"  - [{rule['severity']}] {rule['id']}: {rule['title']}")
            if len(plugin.get_rules()) > 10:
                print(f"  ... 还有 {len(plugin.get_rules()) - 10} 个规则")
        else:
            print(f"❌ 插件未找到: {args.info}")
        return
    
    # 执行扫描
    if not args.plugin or not args.target:
        parser.print_help()
        print("\n⚠️  请指定 --plugin 和 --target")
        return
    
    print("\n" + "="*60)
    print(f"🚀 SecureAgent 扫描")
    print("="*60)
    
    result = scanner.scan(args.plugin, args.target, args.rules)
    
    # 显示结果
    print(f"\n📊 扫描结果")
    print(f"   状态: {result.status.value}")
    print(f"   耗时: {result.duration_ms:.2f}ms")
    
    if result.findings:
        print(f"\n⚠️  发现 {len(result.findings)} 个问题:")
        for f in result.findings[:10]:
            print(f"   [{f.severity.value.upper()}] {f.title}")
    
    if result.error:
        print(f"\n❌ 错误: {result.error}")
    
    # 保存报告
    if args.output:
        import json
        from datetime import datetime
        
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_{args.plugin}_{timestamp}.{args.format}"
        
        scanner.export_report(
            type('Report', (), {'to_dict': lambda self: result.to_dict(), 
                               'summary': {'total': 1, 'passed': 1 if result.status.value == 'passed' else 0}})(),
            str(output_dir / filename),
            args.format
        )


if __name__ == "__main__":
    main()
