import streamlit as st
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
import asyncio
import tempfile
import edge_tts
import os
from dotenv import load_dotenv


load_dotenv()

API_TOKEN_IMAGE = os.getenv("API_TOKEN_IMAGE") # replace with your actual Hugging Face API key
API_KEY_LLM = os.getenv("API_KEY_LLM") # replace with you actual Gemini API Key


API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HEADERS = {"Authorization": f"Bearer {API_TOKEN_IMAGE}"}

MODEL = "gemini-1.5-flash"


llm = ChatGoogleGenerativeAI(model=MODEL, temperature=0.1, api_key=API_KEY_LLM)


# default_genre = "Fantasy"
# default_age = "7"
# default_gender = "Boy"


def output_for(genre, age, gender):
    template_one = PromptTemplate(
        input_variables=["genre", "age", "gender"],
        template="Write a short story in the {genre} genre for {gender} kids aged {age}.\
                         The story should have three engaging paragraphs with a clear beginning, middle, and end.\
                         Use simple and imaginative language suitable for the child's age. Introduce a relatable main character,\
                         an exciting challenge or adventure, and a satisfying resolution that leaves a positive message or lesson \
                         Ensure the characters name is different each time and suited to the storys setting",
    )
    chain_one = LLMChain(llm=llm, prompt=template_one, output_key="story")

    template_two = PromptTemplate(
        input_variables=["story"],
        template="give one simple titile for this story {story}",
    )
    chain_two = LLMChain(llm=llm, prompt=template_two, output_key="title")

    template_three = PromptTemplate(
        input_variables=["story"], template="give one moral of this story {story}"
    )

    chain_three = LLMChain(llm=llm, prompt=template_three, output_key="moral")

    sequence = SequentialChain(
        chains=[chain_one, chain_two, chain_three],
        input_variables=["genre", "age", "gender"],
        output_variables=["story", "title", "moral"],
    )

    chain_responses = sequence.invoke({"genre": genre, "age": age, "gender": gender})

    title = chain_responses["title"]
    story = chain_responses["story"]
    moral = chain_responses["moral"]

    return title, story, moral


def generate_image(prompt, f_name):

    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    # print("Response Status:", response.status_code)
    # print("Response Headers:", response.headers)
    if response.status_code == 200:
        os.makedirs("images", exist_ok=True)
        
        
        with open(f_name, "wb") as file:
            file.write(response.content)
        print("Image saved as 'generated_image.png'")
      

    else:
        print(f"Error {response.status_code}: {response.text}")
    


def prompter(story_chunk):
    template_prompt = PromptTemplate(
        input_variables=["story_chunk"],
        template="Convert the following story {story_chuck} into a highly detailed cartoon-style image generating prompt.\
                        Describe the scene vividly, including character actions, emotions, setting, and key objects. \
                        Keep it under 30 words while ensuring accuracy",
    )

    llm_chain = LLMChain(llm=llm, prompt=template_prompt)
    prompt_image = llm_chain.invoke(story_chunk)
    return prompt_image["text"]


async def text_to_speech(text, voice, rate, pitch):
    if not text.strip():
        return None, "Please enter text to convert."
    if not voice:
        return None, "Please select a voice."

    voice_short_name = voice.split(" - ")[0]
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    communicate = edge_tts.Communicate(
        text, voice_short_name, rate=rate_str, pitch=pitch_str
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    return tmp_path, None


async def main(tex):
    text = tex
    female = "en-US-AvaNeural - en-US (Female)"
    val, error = await text_to_speech(text, female, 0, 0)
    if error:
        print("Error:", error)
    else:
        print("Saved to:", val)
    return val

def display_image(file_name):
    try:
        st.image(file_name)  
    except:
        st.error("Unable to display the image due to server restrictions")



def main_function():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap');

        .doodle-text {
            font-family: 'Caveat', cursive;
            font-size: 40px;
            font-style: italic;
            text-align: center;
        }
        </style>
        <h1 class="doodle-text">ᯓᡣ Doublydoo 𐭩</h1>
        """,
        unsafe_allow_html=True,
    )

    genres = [
        "Fantasy",
        "Science Fiction",
        "Mystery",
        "Adventure",
        "Comedy",
        "Superhero",
        "Mythology",
        "Animal Tales",
        "Fairy Tales",
        "Bedtime Stories",
        "Friendship & Kindness",
        "Magical Realism",
        "Space Adventures",
        "Pirate Stories",
        "Folktales & Legends",
        "School Stories",
        "Enchanted Worlds",
        "Whimsical Tales",
        "Dinosaur Adventures",
        "Talking Animals",
        "Toy & Doll Stories",
        "Detective Stories",
        "Mythical Creatures",
        "Underwater Adventures",
        "Jungle Tales",
        "Magical School Stories",
        "Time Travel for Kids",
        "Seasonal & Holiday Tales",
        "Silly & Wacky Stories",
        "Inspirational & Moral Stories",
    ]

    option = st.selectbox(
        label=str(),
        options=genres,
        index=None,
        placeholder="Select a genre...",
    )

    st.write("")

    age = str(st.slider("How old are you?", 5, 10))
    gender = st.radio("Gender", ["Boy", "Girl"], index=None, horizontal=True)
    if option and gender:
        title, story, moral = output_for(option, age, gender)
    
        st.subheader(title)
    
        chunks_of_story = story.split("\n\n")
        file_path="images"
        for i, paragraph in enumerate(chunks_of_story):
            prompt = prompter(paragraph)
            file_name = f"{file_path}/image_{i+1}.png"
            
    
            generate_image(prompt, file_name)
    
    
            display_image(file_name)
       
    
            st.write(paragraph)
    
            path = asyncio.run(main(paragraph))
            st.audio(path, format="audio/mp3")
            
            if os.path.exists(path):
                os.remove(path)
            # print(path)
            if os.path.exists(file_name):
                os.remove(file_name)
                
            # print(f"Temporary file {path} deleted.")
    
        st.info(f"#### Moral Of The Story\n{moral}")
    else:
        st.info("Kindly select both a genre and a gender before proceeding")


if __name__ == "__main__":
    main_function()
