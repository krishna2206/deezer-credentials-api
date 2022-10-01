import asyncio

from playwright.async_api import async_playwright

DEEZER_LOGIN_URL = "https://www.deezer.com/en/login"
#? Used only locally because Deezer is not available in Madagascar
# DEEZER_REDIRECT_URL = "https://www.deezer.com/en/offers"
DEEZER_REDIRECT_URL = "https://www.deezer.com/en/"


async def update_deezer_arl(login_mail, login_password):
    async with async_playwright() as playwright:
        try:
            #? Chromium is used because for unknown reason, Firefox doesn't work
            browser = await playwright.chromium.launch(headless=True)

            page = await browser.new_page()
            await page.goto(DEEZER_LOGIN_URL)

            while True:
                print("Waiting for cookie banner")
                cookie_banner = await page.query_selector("div[data-testid='cookie-banner']")
                if cookie_banner:
                    print("Cookie banner found, accepting all cookies")
                    await page.locator("button[id='gdpr-btn-accept-all']").click()
                    break
            
            print("Filling login form")
            await page.fill("input[id='login_mail']", login_mail)
            await page.fill("input[id='login_password']", login_password)
            print("Clicking on login button")
            await page.locator("button[id='login_form_submit']").click()

            print("Current URL: ", page.url)
            print("Waiting for redirect")
            await page.wait_for_url(DEEZER_REDIRECT_URL)

        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False, f"{type(error).__name__}: {error}"
        else:
            cookies = await page.context.cookies()
            for cookie in cookies:
                if cookie["name"] == "arl":
                    return True, cookie
        finally:
            await browser.close()


if __name__ == "__main__":
    login_mail = input("Deezer login mail: ")
    login_password = input("Deezer login password: ")
    success, result = asyncio.run(update_deezer_arl(login_mail, login_password))
    if success:
        print(result)
