# CL-Chat

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/your-username/CL-Chat/blob/main/LICENSE)

CL-Chat is a simple command line based chatroom application written in Python. It allows users to connect and communicate with each other in real-time using a server-client architecture. The application provides a seamless chat experience with essential features such as private messaging, user authentication, and customizable chat rooms.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/instax-duttaCL-Chat.git
   ```

2. Navigate to the project directory:

   ```bash
   cd CL-Chat
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:

   ```bash
   python server.py
   ```

2. Start the client:

   ```bash
   python client.py
   ```

3. Enter your nickname and join the universal chatroom and have fun.

4. Enjoy being connected with your team or freinds in real time.

## How It Works

CL-Chat uses the `socket` library in Python to establish a TCP connection between the server and clients. The server acts as a central hub, receiving and routing messages from clients to the appropriate recipients. Each client connects to the server and sends messages using the `socket` API.

The client-side application provides a simple command line interface for users to interact with the server. It allows users to send public messages to the chat room or send private messages to specific users. The client also handles user authentication and enforces chat room rules.

The server-side application manages the connections, routing of messages, and user authentication. It maintains a list of connected clients and their corresponding chat rooms. The server validates user credentials and enforces chat room rules to ensure a secure and controlled chat environment.

## Contributing

Contributions are always welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request. Make sure to follow the existing code style and conventions. 

## License

This project is licensed under the [MIT License](https://github.com/instax-dutta/CL-Chat/blob/main/LICENSE).

## Contact

For any questions or inquiries, please contact the project maintainer:

Your Name - [email@example.com](mailto:bffsproductionhouse456@gmail.com)

Project Link: [https://github.com/your-username/CL-Chat](https://github.com/instax-dutta/CL-Chat)
