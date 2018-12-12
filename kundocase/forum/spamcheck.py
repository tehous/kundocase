import requests
bad_domains = ["spam.com", "universitydiploma.com"]
bad_names = ["thord", "curt", "madicken"]
bad_words = ["spam", "universitydiploma"]


#requires attribute for function 
def attr_req(argument):
    def real_decorator(function):
        def wrapper(obj,*args,**kwargs):
            if hasattr(obj,argument):
                return function(obj,*args,**kwargs)
            else:
                return False
        return wrapper
    return real_decorator


# Different ways to check for spam
@attr_req("content")
def long_texts_are_spam(postm, maxLen=200):
    if len(postm.content) > maxLen:
        return True
    return False

@attr_req("user_email")
def all_users_from_domain_are_spam(postm, bad_domains=bad_domains):
    domain = "@" in postm.user_email and postm.user_email.split("@")[1] #error avoidance
    if domain and domain in bad_domains:
        return True
    return False

@attr_req("user_name")
def some_usernames_are_spam(postm,bad_names=bad_names):
    name = postm.user_name
    for bad_name in bad_names:
        if name in bad_name:
            return True
    return False

@attr_req("content")
def words_in_text_are_spam(postm,bad_words=bad_words):
    text = postm.content
    for word in bad_words:
        if word in text:
            return True
    return False

@attr_req("user_email")
def known_spammers_are_spam(postm):
    email = postm.user_email
    url = "https://www.stopforumspam.com/api?f=json&email=" + email
    response = requests.get(url, timeout=2)
    data = response.json()
    if data and data["success"] and data["email"]["appears"]:
        return True
    return False


def spamcheck(obj,
              spamcheckers=[
                            long_texts_are_spam,
                            all_users_from_domain_are_spam,
                            some_usernames_are_spam,
                            words_in_text_are_spam,
                            known_spammers_are_spam,
                            ],
              max_len=200):
    for checker in spamcheckers:
        if checker(obj):
            return True
    return False
