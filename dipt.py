import requests
import re
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import json
from bs4 import BeautifulSoup


#PUT YOUR DISCORD WEBHOOK HERE
dcord_hook = "HERE"

#PUT YOUR DELAY HERE IN SECONDS
retrydelay = 1

def dipt():
   old_name = ''
   while 2 > 1:
      request = requests.get('https://www.vancityoriginal.com/new-dipt-kicks/?limit=1')
      
      soup = BeautifulSoup(request.text, 'html.parser')

      for div in soup.findAll('div', attrs={'class':'card-body'}):

         links = (div.find('a')['href'])
         names = (div.find('a').contents[0])

         requesting = requests.get(links)
         data = requesting.text

         soup1 = BeautifulSoup(data, 'html.parser')
         image = soup1.find("meta",  property="og:image")
         pic = image["content"]

         price = re.search('"formatted":(.+?),', data)
         newprice = price.group(1)
         finalprice = re.sub("\"", "", newprice)
         
         id = re.search('"content_ids":(.+?),', data)
         newid = id.group(1)
         finalid = re.sub("\"", "", newid)
         pid1 = re.sub("\[", "", finalid)
         pid = re.sub("\]", "", pid1)


         if names != old_name:

            old_name = names

            webhook = DiscordWebhook(url=dcord_hook)
            embed = DiscordEmbed(title=f"Dipt Monitor", description='New Product', color=242424)
            embed.add_embed_field(name='Product', value=f'{names}')
            embed.add_embed_field(name='Price', value=f'{finalprice}')
            embed.add_embed_field(name='PID', value=f'{pid}')
            embed.add_embed_field(name='Link', value=f'[Product Link]({links})')
            embed.set_thumbnail(url=f'{pic}')
            embed.set_timestamp()
            embed.set_footer(text=f'Dipt by @carsonleckyy')  
            webhook.add_embed(embed)
            response = webhook.execute()
            time.sleep(retrydelay)

         else:
            print(f'same product {names}')
            time.sleep(retrydelay)

dipt()

