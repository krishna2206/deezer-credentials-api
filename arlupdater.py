from playwright.async_api import async_playwright

DEEZER_LOGIN_URL = "https://www.deezer.com/en/login"


async def update_deezer_arl(login_mail, login_password):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        page = await browser.new_page()
        await page.goto(DEEZER_LOGIN_URL)

        return True, await page.content()
        """
        try:
            browser = await playwright.chromium.launch(headless=True)

            page = await browser.new_page()
            await page.goto(DEEZER_LOGIN_URL)

            await page.fill("input[id='login_mail']", login_mail)
            await page.fill("input[id='login_password']", login_password)
            await page.click("button[id='login_form_submit']")

            while await page.url() == DEEZER_LOGIN_URL:
                if await page.url() == "https://www.deezer.com/en/offers":
                    break
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False, f"{type(error).__name__}: {error}"
        else:
            return True, await page.context.cookies()
        finally:
            await browser.close()
        """
