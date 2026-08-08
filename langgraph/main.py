import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file

    model = ChatOpenAI(
        model=os.getenv("BAILIAN_MODEL", "deepseek-v3.2"),
        api_key=os.environ["DASHSCOPE_API_KEY"],
        base_url=os.environ["BAILIAN_BASE_URL"],
    )

    response = model.invoke("Explain LangGraph in two sentences.")
    print(response.content)
