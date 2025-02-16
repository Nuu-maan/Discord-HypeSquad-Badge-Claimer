# Discord HypeSquad Badge Claimer

A Python tool to automatically claim Discord HypeSquad badges for multiple accounts. Supports both `email:pass:token` and `token-only` formats. Built with multi-threading for efficient processing and detailed logging.

---

## Features

- **Multi-Account Support**: Process multiple Discord accounts simultaneously.
- **Token Format Flexibility**: Supports both `email:pass:token` and `token-only` formats.
- **Threaded Execution**: Utilizes multi-threading for faster processing.
- **Detailed Logging**: Logs all actions with color-coded output and file logging.
- **Random House Assignment**: Automatically assigns accounts to random HypeSquad houses (Bravery, Brilliance, Balance).
- **Rate Limit Handling**: Detects and handles Discord API rate limits efficiently.
- **Secure Token Masking**: Ensures tokens are masked in logs for security.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nuu-maan/Discord-HypeSquad-Badge-Claimer.git
   cd Discord-HypeSquad-Badge-Claimer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Your Accounts File**:
   - Create a file named `accounts.txt` in the `input` folder.
   - Add your accounts in the following formats:
     - **Email/Password/Token Format**:
       ```
       email:password:token
       email2:password2:token2
       ```
     - **Token-Only Format**:
       ```
       token
       token2
       ```

4. **Run the Script**:
   ```bash
   python index.py
   ```

---

## Usage

1. Place your accounts in the `input/accounts.txt` file.
2. Run the script:
   ```bash
   python index.py
   ```
3. View the logs in the console or in the `hypesquad.log` file for detailed output.

---

## Configuration

You can configure the script by modifying the following options:

- **Threads**: Adjust the number of threads for faster or more stable processing.
- **Logging**: Enable or disable debug mode in the `NovaLogger` class.
- **House Selection**: Modify the `house_id` logic to assign accounts to specific HypeSquad houses.

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear and descriptive messages.
4. Submit a pull request.

Ensure your code follows the project's style and includes appropriate documentation.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Disclaimer

This tool is for educational purposes only. Use it at your own risk. The developers are not responsible for any misuse or damage caused by this tool.