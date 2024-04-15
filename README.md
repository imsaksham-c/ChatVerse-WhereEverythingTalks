# ChatVerse: Where Everything Talks!

Welcome to ChatVerse! This dynamic platform enables conversational interactions with various types of content, including YouTube videos, websites, and documents of any format. With ChatVerse, you can engage in context-aware conversations, extract information, and explore a wide range of topics effortlessly.

## Demo

Experience the power of ChatVerse through our deployed demo on Streamlit:

- [ChatVerse Demo on Streamlit](https://chatverse-demo.streamlit.app/)
- [ChatVerse Demo on Render](https://webchat-websitechatbot.onrender.com/)

Note: Website URL syntax should be "https://<website>", else the connection will not be secure which will further cause error while scraping. Example - https://en.wikipedia.org/wiki/Edward_Snowden


https://github.com/imsaksham-c/WebChat-WebsiteChatbot/assets/43902924/f385ee52-a058-401e-8138-3e12a7802bb1



## Features

- **Multimedia Interaction:** ChatVerse allows seamless interaction with YouTube videos, websites, and documents, offering a versatile experience.
  
- **Contextual Conversations:** The chatbot maintains context-aware conversation history, providing relevant responses based on previous interactions.
  
- **Retrieval-Augmented Generation (RAG):** ChatVerse employs advanced RAG techniques to enhance response generation by augmenting its knowledge with retrieved information from various sources.

- **Streamlit GUI:** Built with a user-friendly Streamlit interface, ChatVerse offers an intuitive platform for engaging conversations and exploring content effortlessly.

## Installation

Get started with ChatVerse by following these simple steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/imsaksham-c/WebChat-WebsiteChatbot.git
    cd WebChat-WebsiteChatbot
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create your own `.env` file with the following variables:

    ```plaintext
    OPENAI_API_KEY=[your-openai-api-key]
    ```

## Usage

Launch the Streamlit app to start exploring ChatVerse:

```bash
streamlit src/run app.py
```

![alt text](https://github.com/imsaksham-c/WebChat-WebsiteChatbot/blob/main/docs/HTML-rag-diagram.jpg)

## Contributing

Contributions from the community are highly encouraged! Whether it's fixing bugs, improving documentation, adding new features, or enhancing existing ones, your contributions are valuable in making ChatVerse better for everyone.

Please ensure that your contributions align with the project's goals and guidelines. Be respectful of others' work and adhere to the project's code of conduct.

If you have any questions or need assistance, don't hesitate to reach out via GitHub issues or discussions.

Happy coding! 🚀👨‍💻🤖

## License

ChatVerse is licensed under the MIT License. For more details, refer to the [LICENSE](LICENSE) file.

**Note:** ChatVerse is intended for educational and research purposes. Users are advised to comply with the terms of use and guidelines of any APIs and services utilized within the project.

We hope ChatVerse serves as a valuable resource for your journey in exploring AI and chatbot development. Don't forget to star this repository if you find it useful!

## Upcoming Features

Stay tuned for exciting updates and new features in future releases:

- [x] Website Integration
- [x] Document Integration
- [x] Youtube Integration 
- [ ] WhatsApp Integration
- [ ] Custom API & Deployment Options
- [ ] Integration with other vector databases (e.g., Pinecone, LanceDB, etc.)
- [ ] Support for additional language models (e.g., Gemini, Mistral, etc.)

---
Connect with the developer on [LinkedIn](https://www.linkedin.com/in/saksham-chaurasia/) or reach out via email at imsaksham.c@gmail.com.

Let's keep ChatVerse evolving and exploring the possibilities of conversational AI together!
