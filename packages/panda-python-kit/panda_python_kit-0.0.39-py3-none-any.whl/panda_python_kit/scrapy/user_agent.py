from fake_useragent import UserAgent
ua = UserAgent()
def get_one_user_agent():
    return ua.random