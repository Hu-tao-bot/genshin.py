# Authentication

## Cookies

Cookies are the default form of authentication over the majority of Mihoyo APIs. These are used in web events and hoyolab utilities such as the Battle Chronicle.
The cookies used in these APIs are the same as the ones you use to log in to your hoyolab account and make payments.
This means it's highly recommended to use your own cookies only for local testing and to create alt accounts for actual API requests.

For authentication, you will need to send two cookies: `ltuid` and `ltoken`. `ltuid` is your hoyolab UID and `ltoken` is a unique token used for the actual authentication.

### Setting cookies

There are several ways to set cookies but `set_cookies` is preferred.

```py
# set as an __init__ parameter
client = genshin.GenshinClient({"ltuid": ..., "ltoken": ...})

# set dynamically
client = genshin.GenshinClient()
client.set_cookies({"ltuid": ..., "ltoken": ...}) # mapping
client.set_cookies(ltuid=..., ltoken=...) # kwargs
client.set_cookies("ltuid=...; ltoken=...") # cookie header
```

### How can I get my cookies?

1. Go to [hoyolab.com](https://www.hoyolab.com/genshin/).
2. Login to your account.
3. Press `F12` to open Inspect Mode (ie. Developer Tools).
4. Go to `Application`, `Cookies`, `https://www.hoyolab.com`.
5. Copy `ltuid` and `ltoken`.

### Setting cookies automatically

For testing, you may want to use your own personal cookies.
As long as you are logged into your account on one of your browsers, you can get these dynamically with `genshin.get_browser_cookies()`.

### Installation

```console
pip install genshin[cookies]
```

### Example

```py
# get cookies from a browser and set them
client = genshin.GenshinClient()
cookies = genshin.get_browser_cookies()
client.set_cookies(cookies)

# implicitly set browser cookies
client = genshin.GenshinClient()
client.set_browser_cookies()
```

In case of conflicts/errors, you may specify the browser you want to use.

```py
cookies = genshin.get_browser_cookies("chrome")
```

### Details

Sadly not even this is inconsistent enough. For some endpoints like `redeem_code`, you might need to set `account_id` and `cookie_token` cookies instead. You can get them by going to [genshin.mihoyo.com](https://genshin.mihoyo.com/en/gift).

## Authkey

Authkeys are an alternative authentication used mostly for paginators like `client.wish_history()` and `client.transaction_log()`. They last only 24 hours, and it's impossible to do any write operations with them. That means authkeys, unlike cookies, are absolutely safe to share.

These authkeys should always be a base64 encoded string and 1024 characters long.

### Setting authkeys

Similar to cookies, you may set authkeys through multiple ways.

```py
# set as an __init__ parameter
client = genshin.GenshinClient(authkey="...")

# set dynamically
client.authkey = "..."
```

Since authkeys are safe to share, all functions which use authkeys also accept them as a parameter.

```py
client = genshin.GenshinClient()
async for wish in client.wish_history(authkey="..."):
    pass
```

### How can I get my authkey?

To get your authkey manually from other platforms, you can use any of these approaches:

- PC
  - Open the wish history in the game and wait for it to load
  - Open the file at `~\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt`
  - Find the link which starts with `OnGetWebViewPageFinish` and copy it
- Android
  - Open the Paimon menu
  - Click Feedback
  - Wait for it to load, and a feedback page should open
  - Turn off your Wi-Fi
  - Refresh the page
  - The page should display an error containing a link
  - Copy the link
- PS
  - Open any event mail which contains a QR Code
  - Scan the QR Code with your phone
  - Copy the link
    > You can only use this if you have an in-game mail with QR Code to open the web event

After that, you can extract the authkey from the link using `genshin.extract_authkey`.

```py
url = "https://webstatic-sea.mihoyo.com/ys/event/im-service/index.html?..."
authkey = genshin.extract_authkey(url)

client = genshin.GenshinClient()
client.authkey = authkey
```

### Setting authkeys automatically

If you open a wish history or a wish details page in genshin, then the authkey will show up in your logfiles. It's possible to dynamically get the authkey using `genshin.get_authkey()`.

```py
# get the authkey from a logfile
client = genshin.GenshinClient()
client.authkey = genshin.get_authkey()

# implicitly set the authkey
client = genshin.GenshinClient()
client.set_authkey()
```
