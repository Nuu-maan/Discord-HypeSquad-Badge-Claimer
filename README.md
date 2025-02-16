### `README.md`

```markdown
# Discord HypeSquad Badge Claimer

A Python tool to automatically claim Discord HypeSquad badges for multiple accounts. Supports both `email:pass:token` and `token-only` formats. Built with multi-threading for efficient processing and includes detailed logging.

![Banner](https://i.imgur.com/your-banner-image.png) <!-- Replace with your banner image -->

---

## Features

- **Multi-Account Support**: Process multiple Discord accounts simultaneously.
- **Token Format Flexibility**: Supports both `email:pass:token` and `token-only` formats.
- **Threaded Execution**: Utilizes multi-threading for faster processing.
- **Detailed Logging**: Logs all actions with colored output and file logging.
- **Random House Assignment**: Automatically assigns accounts to random HypeSquad houses (Bravery, Brilliance, Balance).
- **Rate Limit Handling**: Detects and handles Discord API rate limits.
- **Secure Token Masking**: Masks tokens in logs for security.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nuu-maan/Discord-HypeSquad-Badge-Claimer.git
   cd Discord-HypeSquad-Badge-Claimer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your accounts file**:
   - Create a file named `accounts.txt` in the `input` folder.
   - Add your accounts in the following format:
     ```
     email:password:token
     email2:password2:token2
     ```
   - Alternatively, you can use the `token-only` format:
     ```
     token
     token2
     ```

4. **Run the script**:
   ```bash
   python hypesquad_claimer.py
   ```

---

## Usage

1. Place your accounts in the `input/accounts.txt` file.
2. Run the script:
   ```bash
   python hypesquad_claimer.py
   ```
3. View the logs in the console or in the `hypesquad.log` file.

---

## Configuration

You can configure the script by modifying the following:

- **Threads**: Adjust the number of threads in the script for faster processing.
- **Logging**: Enable or disable debug mode in the `NovaLogger` class.
- **House Selection**: Modify the `house_id` logic to assign specific houses.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

Please ensure your code follows the project's style and includes appropriate documentation.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool is for educational purposes only. Use it at your own risk. The developers are not responsible for any misuse or damage caused by this tool.
