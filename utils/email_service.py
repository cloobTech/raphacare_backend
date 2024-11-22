# import asyncio
# import yagmail
# from settings.pydantic_config import settings
# from jinja2 import Environment, FileSystemLoader
# from typing import Callable


async def send_email():
    # yag = yagmail.SMTP(settings.EMAIL_CONFIG_USERNAME, settings.EMAIL_CONFIG_PASSWORD)

    # to = 'cloobtechse@gmail.com'
    # subject = 'Hello'

    # env = Environment(loader=FileSystemLoader('templates'))
    # template = env.get_template('email_verification.html')

    # with open('static/styles.css') as f:
    #     css = f.read()
    # html_body = template.render(token='123456', css_content=css)
    #     # Inline the CSS

    # await asyncio.to_thread(yag.send, to, subject, html_body)
    async def send():
        print('Email sent')
    return send
