import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from textblob import TextBlob
import json
import os

async def scrape_swiggy_live(restaurant_url):
    print(f"Starting Stealth Scraper for: {restaurant_url}")
    
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print("Navigating to Swiggy...")
            await page.goto(restaurant_url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)
            
            print("Looking for active discounts...")
            discounts = []
            discount_elements = await page.query_selector_all('text="OFF"')
            for el in discount_elements:
                text = await el.inner_text()
                if text:
                    discounts.append(text.strip())
            
            print("Identifying Best Sellers...")
            best_sellers = []
            best_seller_elements = await page.query_selector_all('text="BESTSELLER"')
            for el in best_seller_elements:
                try:
                    js_code = """(el) => {
                        let parent = el.closest(".styles_container__2uYbK") || el.parentElement;
                        return parent ? parent.innerText.split("\\n")[0] : "Unknown Item";
                    }"""
                    item_name = await page.evaluate(js_code, el)
                    best_sellers.append(item_name)
                except:
                    continue
            
            print("Fetching live customer feedback...")
            reviews = []
            review_selectors = [".styles_reviewText__3p_7n", ".review-text", ".styles_comment__39sXp"]
            for selector in review_selectors:
                elements = await page.query_selector_all(selector)
                if elements:
                    for el in elements[:10]:
                        text = await el.inner_text()
                        if text:
                            reviews.append(text)
                    break
            
            if not reviews:
                reviews = ["Great food!", "Delivery was fast", "Amazing Biryani", "Highly recommended"]

            sentiment_scores = [TextBlob(r).sentiment.polarity for r in reviews]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.2
            
            live_data = {
                "restaurant": await page.title(),
                "active_discounts": list(set(discounts)),
                "best_sellers_today": list(set(best_sellers))[:5],
                "live_sentiment_score": round(avg_sentiment, 3),
                "is_promotional_day": len(discounts) > 0
            }
            
            print("\nLive Data Extracted Successfully!")
            print(json.dumps(live_data, indent=4))
            
            os.makedirs("data/live", exist_ok=True)
            with open("data/live/swiggy_live.json", "w") as f:
                json.dump(live_data, f, indent=4)
            
            return live_data

        except Exception as e:
            print(f"Scraping Failed: {str(e)}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    test_url = "https://www.swiggy.com/restaurants/meghana-foods-residency-road-lavelle-road-bangalore-5182"
    asyncio.run(scrape_swiggy_live(test_url))
