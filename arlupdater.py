from playwright.async_api import async_playwright

DEEZER_LOGIN_URL = "https://www.deezer.com/en/login"


async def update_deezer_arl(login_mail, login_password):
    async with async_playwright() as playwright:
        try:
            browser = await playwright.chromium.launch(headless=True)

            page = await browser.new_page()
            await page.goto(DEEZER_LOGIN_URL)

            await page.fill("input[id='login_mail']", login_mail)
            await page.fill("input[id='login_password']", login_password)
            login_button = await page.query_selector("button[id='login_form_submit']")
            await login_button.click(force=True)

            requests = []
            page.on(
                "request",
                lambda request: requests.append(f"{request.method} {request.url}")
            )

            """
            while page.url == DEEZER_LOGIN_URL:
                if page.url == "https://www.deezer.com/en/offers":
                    break
            """
        except Exception as error:
            print(f"{type(error).__name__}: {error}")
            return False, f"{type(error).__name__}: {error}"
        else:
            print(page.url)
            # return True, await page.context.cookies()
            return True, {"cookies": await page.context.cookies(), "requests": requests}
        finally:
            await browser.close()
