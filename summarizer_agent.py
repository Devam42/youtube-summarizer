import os
import logging
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Text splitter for managing transcript size
text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=3950, chunk_overlap=100)

def generate_summary(transcript_text):
    try:
        model = genai.GenerativeModel("gemini-pro")

        # Creating the prompt for summarization
        prompt = (
            f"You are an expert summarizer. Read the following transcript and generate a highly detailed, "
            f"in-depth summary covering all key points and important information. The summary should be approximately "
            f"2000 words.\n\n"
            f"Transcript:\n{transcript_text}\n\n"
            f"Detailed Summary:"
        )

        # Calling the Gemini Pro model to generate content
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary

    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        raise RuntimeError("Failed to generate summary.")

def create_summary(docs):
    transcript_text = " ".join([doc.page_content for doc in docs])
    return generate_summary(transcript_text)

def summarize_youtube_video(youtube_url: str) -> str:
    """
    Useful to get the summary of a YouTube video. Applies if the user sends a YouTube link.
    """
    video_id = youtube_url.split("=")[1]
    loader = YoutubeLoader(video_id)
    docs = loader.load_and_split(text_splitter)

    return create_summary(docs)

class summary_agent:
    def __init__(self) -> None:
        pass

    def summarize(self, query):
        output = summarize_youtube_video(query)
        print(output)
        return output

if __name__ == "__main__":
    print("Input YouTube URL...")
    agent = summary_agent()
    query = input()
    print(agent.summarize(query))
