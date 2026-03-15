from newspaper import Article


def read_page(url):

    try:

        article = Article(url)

        article.download()
        article.parse()

        text = article.text

        # limit text length to keep prompt clean
        text = text[:4000]

        return text

    except Exception as e:

        print("Failed to read:", url)

        return ""