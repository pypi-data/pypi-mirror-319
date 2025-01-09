from virtuals_sdk.game import Agent
from virtuals_sdk.functions.telegram import TelegramClient
from virtuals_sdk.functions.farcaster import FarcasterClient
from virtuals_sdk.functions.discord import DiscordClient

# # Create agent with just strings for each component
# agent = Agent(
# 	api_key="985f75776b45337f0a9c2c11ddf7bd795950ee13b4e5074af604762f449114bd",
#     goal="Autonomously analyze crypto markets and provide trading insights",
#     description="HODL-9000: A meme-loving trading bot powered by hopium and ramen",
#     world_info="Virtual crypto trading environment where 1 DOGE = 1 DOGE"
# )

# # list available functions that can be added to agent
# # print(agent.list_available_default_twitter_functions()) 
# # agent.list_available_default_twitter_functions()
# # agent.use_default_twitter_functions(["wait", "reply_tweet"])

# print("here")
# # response = agent.simulate_twitter(session_id="session-twitter")
# # print(response)

# ### TEST TELEGRAM FUNCTIONS
# # get telegram custom functions through client
# tg_client = TelegramClient(bot_token="7210003118:AAGDgu4PgMJEwY892B_U0wyfZ0xCm-sMOGk")

# # get available telegram functions
# print(tg_client.available_functions)

# # get telegram custom functions through client
# reply_message_fn = tg_client.get_function("send_message")
# create_poll_fn = tg_client.get_function("create_poll")
# pin_message_fn = tg_client.get_function("pin_message")
# # set_chat_title_fn = tg_client.get_function("set_chat_title")

# reply_message_fn("5394289251", "Hello World")
# create_poll_fn("5394289251", "What is your favorite color?", ["Red", "Blue", "Green"], "True")
# pin_message_fn("5394289251", "82", "True")


# ### TEST FARCASTER FUNCTIONS
# NEYNAR_API_KEY = ""
# NEYNAR_SIGNER_UUID = ""
# farcaster_client = FarcasterClient(api_key=NEYNAR_API_KEY,
#                                    signer_uuid=NEYNAR_SIGNER_UUID)

# # get available farcaster functions
# print(farcaster_client.available_functions)

# # get farcaster custom functions through client
# post_cast_fn = farcaster_client.get_function("post_cast")
# reply_to_cast_fn = farcaster_client.get_function("reply_to_cast")
# get_trending_casts_fn = farcaster_client.get_function("get_trending_casts")
# search_casts_fn = farcaster_client.get_function("search_casts")



### TEST DISCORD FUNCTIONS
discord_client = DiscordClient(bot_token="MTMxODQ1MDE2OTYxNTc0OTE4MA.Gr4v3O.JC_lXLQ_EvVMd-C_BeC0xwrFLZDQE5DZqtndXk")
dis_send_message_fn = discord_client.get_function("send_message")
dis_reaction_fn = discord_client.get_function("add_reaction")
dis_pin_message_fn = discord_client.get_function("pin_message")
dis_delete_message_fn = discord_client.get_function("delete_message")

channel_id = "1318449474195947522"
dis_send_message_fn(channel_id, "Hello World")

message_id = "1321715872863092736"
dis_reaction_fn(channel_id, message_id, "😊")

dis_pin_message_fn(channel_id, message_id)

message_id = "1321732428250877984"
dis_delete_message_fn(channel_id, message_id)