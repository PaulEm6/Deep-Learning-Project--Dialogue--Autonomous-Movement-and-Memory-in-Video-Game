from my_app.chain import chain

def test_chain():
    print(
        #ASKING FOR USER INPUT=> chain.invoke({"text": input("> ")}).content
        chain.invoke({"text": "Hi there, do you have any gold for me"}).content
    )