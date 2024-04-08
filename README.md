# WebChat - Chat with Website

Welcome to the WebChat - Chat with Website GitHub repository! This project serves as a dynamic platform for building a chatbot capable of interacting with websites, extracting information, and engaging in context-aware conversations through a Streamlit graphical interface. By harnessing the capabilities of LangChain 0.1.0, developers can create powerful conversational AI applications.

## Demo

You can access the deployed demo of the chatbot on Streamlit by visiting [WebChat Demo](https://webchat-demo.streamlit.app/).

## Features

- **Website Interaction:** The application scrapes website content based on user input, allowing them to specify the scraping depth.
    - Depth 1: Scrapes only the content of the given page.
    - Depth 2: Scrapes the content of the given page along with the links present on that page, etc.

    This depth parameter enables users to control the extent of the scraping process, facilitating comprehensive data extraction from websites.

- **Contextual Conversation:** The chatbot maintains a context-aware conversation history, allowing it to provide relevant responses based on previous interactions.

- **Retrieval-Augmented Generation (RAG):** The chatbot employs RAG techniques to enhance response generation by augmenting its knowledge with retrieved information from websites.

- **Streamlit GUI:** Built using Streamlit, the chatbot offers an intuitive and user-friendly interface. Users can easily interact with the chatbot and view conversation history.

## Installation

Ensure you have Python installed on your system. Then clone this repository:

```bash
git clone [repository-link]
cd [repository-directory]
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create your own `.env` file with the following variables:

```plaintext
OPENAI_API_KEY=[your-openai-api-key]
```

## Usage

To run the Streamlit app:

```bash
streamlit run app.py
```

![alt text](https://github.com/alejandro-ao/chat-with-websites/blob/master/docs/HTML-rag-diagram.jpg)

## Contributing

Contributions from the community are highly encouraged! Whether it's fixing bugs, improving documentation, adding new features, or enhancing existing ones, your contributions are valuable in making this project better for everyone.

Feel free to submit pull requests for bug fixes, typo corrections, or any improvements you deem necessary. Additionally, substantial changes or new features beyond the scope of the tutorial are also welcome.

Please ensure that your contributions align with the project's goals and guidelines. Be respectful of others' work and adhere to the project's code of conduct.

Thank you for your interest in contributing to WebChat - Create Chatbot from Website! Together, let's make this project even better.

If you have any questions or need assistance, don't hesitate to reach out via GitHub issues or discussions.

Happy coding! 🚀👨‍💻🤖

## License

This project is licensed under the MIT License. For more details, refer to the [LICENSE](LICENSE) file.

**Note:** The project is intended for educational and research purposes. Users are advised to comply with the terms of use and guidelines of any APIs and services utilized within the project.

We hope this repository serves as a valuable resource for your journey in exploring AI and chatbot development. For additional tutorials and information, visit [Your YouTube Channel].

If you find this repository useful, don't forget to star it!

---
Connect with me on [LinkedIn](https://www.linkedin.com/in/saksham-chaurasia/) or reach out via email at imsaksham.c@gmail.com.
