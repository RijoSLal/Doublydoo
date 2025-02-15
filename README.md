# DoublyDoo - AI-Powered Storytelling for Kids

DoublyDoo is a LangChain-based children's storytelling app that brings stories to life with AI-generated **text, audio narration, and images**. Kids can select a **genre** and enter their **age and gender**, and the app will create a unique, engaging story tailored just for them.

## Features ✨
- **AI-Generated Stories** 📖: Creates personalized short stories based on the child's preferences.
- **Text-to-Speech Narration** 🔊: Reads the story aloud using realistic AI-generated voices.
- **AI-Generated Illustrations** 🎨: Generates vivid, cartoon-style images for different story scenes.
- **Genre Selection** 🎭: Includes a variety of story genres like Fantasy, Adventure, Mystery, and more.

## Tech Stack 🛠️
- **LangChain**: For managing AI-driven story generation.
- **Google Gemini API**: To generate the story content and prompts.
- **Stable Diffusion**: For creating AI-generated images.
- **Edge-TTS**: For text-to-speech functionality.
- **Streamlit**: For an interactive user-friendly interface.

## Installation & Setup 🚀
### 1. Clone the Repository
```sh
git clone https://github.com/RijoSLal/doublydoo.git
cd doublydoo
```
### 2. Install Dependencies
```sh
pip install -r requirements.txt
```
### 3. Set Up Environment Variables
Create a `.env` file in the project root and add your API keys:
```
API_TOKEN_IMAGE=your_huggingface_api_key
API_KEY_LLM=your_gemini_api_key
```

### 4. Run the Application
```sh
streamlit run doublydoo.py
```

## How It Works 🏗️
1. Select a **genre**, enter your **age**, and choose a **gender**.
2. The app generates a **unique story** with a title and moral.
3. Each paragraph is illustrated with an **AI-generated image**.
4. The story is **read aloud** using AI-generated speech.
5. Enjoy an interactive storytelling experience! 🎉

## Future Improvements 🌱
- Support for **multiple voices** and language options.
- **Interactive storytelling** elements where kids can make choices.
- Enhanced **story customization** features.

## Contributing 🤝
Contributions are welcome! Feel free to fork the repo, make improvements, and submit a pull request.

## License 📜
This project is licensed under the **MIT License**.

Enjoy the magical world of **DoublyDoo**! ✨📚

