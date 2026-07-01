#!/usr/bin/env python3
"""
原型 HTML 截图工具

用法:
    python3 screenshot.py <config.json>

config.json 结构见 screenshot_schema_example.json

功能:
    - 用 Playwright 无头浏览器打开原型 HTML
    - 按配置点击导航菜单切换页面
    - 对每个页面/弹窗截图
    - 输出截图文件 + manifest.json

依赖: playwright (需 playwright install chromium)
"""

import sys
import os
import json

from playwright.sync_api import sync_playwright


def run_screenshots(config_path):
    """执行截图流程"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    html_path = config.get("html_path", "")
    out_dir = config.get("output_dir", "/tmp/guide-screenshots")
    viewport = config.get("viewport", {"width": 1440, "height": 900})
    wait_initial = config.get("wait_initial_ms", 2500)
    wait_between = config.get("wait_between_ms", 800)
    pages = config.get("pages", [])

    if not html_path or not os.path.exists(html_path):
        print(f"❌ 原型 HTML 不存在: {html_path}")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    shots = []
    p = sync_playwright().start()
    # 优先用 chromium channel（playwright install chromium 安装的），
    # 回退到默认 headless_shell（playwright install chromium-headless-shell 安装的）
    try:
        browser = p.chromium.launch(headless=True, channel="chromium")
    except Exception:
        browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport=viewport)

    print(f"打开原型: {html_path}")
    page.goto(f"file://{html_path}", wait_until="networkidle")
    page.wait_for_timeout(wait_initial)

    for pg in pages:
        name = pg.get("name", "screenshot")
        filename = pg.get("file", f"{name}.png")
        filepath = os.path.join(out_dir, filename)

        # 执行前置点击
        clicks = pg.get("clicks", [])
        success = True
        for click in clicks:
            try:
                selector = click.get("selector", "")
                click_type = click.get("type", "css")  # css | text | eval
                wait_after = click.get("wait_after_ms", wait_between)

                if click_type == "text":
                    page.click(f"text={selector}", timeout=3000)
                elif click_type == "eval":
                    page.evaluate(selector)
                else:
                    page.click(selector, timeout=3000)

                page.wait_for_timeout(wait_after)
            except Exception as e:
                print(f"  ⚠️  点击失败 [{selector}]: {e}")
                success = False

        # 截图
        try:
            full_page = pg.get("full_page", True)
            page.screenshot(path=filepath, full_page=full_page)
            shots.append(filename)
            print(f"✅ {filename}")
        except Exception as e:
            print(f"❌ {filename}: {e}")

    browser.close()
    p.stop()

    # 输出清单
    manifest_path = os.path.join(out_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(shots, f, ensure_ascii=False, indent=2)

    print(f"\n总计截图 {len(shots)} 张，保存到 {out_dir}/")
    return shots


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 screenshot.py <config.json>")
        print("config.json 格式见 screenshot_schema_example.json")
        sys.exit(1)
    run_screenshots(sys.argv[1])
