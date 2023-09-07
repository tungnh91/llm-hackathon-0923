import os
import openai
import weaviate

openai.api_key = os.environ["OPENAI_API_KEY"]

client = weaviate.Client("http://localhost:8080")


def put_in_db(file):
    print("done")
