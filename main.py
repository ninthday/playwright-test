#!/usr/bin/env python3

import asyncio

from playwright.async_api import async_playwright

# 目標網址
TARGET_URL = "https://24h.pchome.com.tw/"


async def scrape_pchome():
    """
    使用 Playwright 爬抓 PChome 24h 首頁的內容。
    """
    # 啟動 Playwright
    async with async_playwright() as p:
        print("🚀 正在啟動瀏覽器...")

        # 啟動 Chromium 瀏覽器實例。headless=True 表示無頭模式 (背景執行)
        # 如果想看到瀏覽器開啟，可以設定 headless=False
        browser = await p.chromium.launch(headless=True)

        # 開啟一個新的頁面 (Tab)
        page = await browser.new_page()

        print(f"🌐 正在導航至 {TARGET_URL}...")

        # 導航到目標網址
        # timeout=60000 設置等待時間為 60 秒
        await page.goto(TARGET_URL, timeout=60000)

        # 🎯 關鍵步驟：等待頁面上的特定元素載入
        # PChome 24h 首頁上的主要內容區塊通常會動態載入。
        # 我們等待一個常見的元素，例如 id="mainArea" 或 .hot-prods-title 載入完成。
        # 這樣可以確保在取得 HTML 時，前端渲染的內容已經到位。
        try:
            # 這裡我們等待一個標題元素 '.hot-prods-title' 出現，確保頁面已渲染
            await page.wait_for_selector(".hot-prods-title", timeout=10000)
            print("✅ 頁面主要內容已載入。")
        except Exception as e:
            # 如果找不到特定的 selector 也不要緊，可能是頁面結構變動，
            # Playwright 在 page.goto() 後通常會等待基本載入完成。
            print(f"⚠️ 找不到特定元素，可能頁面載入未完全。繼續擷取... 錯誤: {e}")

        # 取得整個頁面的 HTML 內容
        html_content = await page.content()

        print(f"📄 成功擷取 {len(html_content)} 字節的 HTML 內容。")

        # 關閉瀏覽器
        await browser.close()

        # 返回 HTML 內容
        return html_content


# 執行非同步函數
if __name__ == "__main__":
    # 執行爬抓任務
    html_result = asyncio.run(scrape_pchome())

    print("\n--- HTML 內容片段 (前 500 字元) ---")
    # 為了不印出大量的內容，我們只顯示開頭片段
    print(html_result[:500])
    print("\n--- 擷取結束 ---")
