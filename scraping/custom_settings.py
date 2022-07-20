from latest_user_agents import get_random_user_agent

USER_AGENT = get_random_user_agent()

DOWNLOADER_MIDDLEWARES = {
    'scraping.proxy_middleware.CustomProxyMiddleware': 350
}

# ITEM_PIPELINES = {
#     'scraping.file_pipeline.FilePipeline': 350
# }

AUTOTHROTTLE_ENABLED = True

COOKIES_ENABLED = False
