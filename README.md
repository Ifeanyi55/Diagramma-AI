# Diagramma AI

Diagramma AI is a powerful tool that leverages the Nano-Banana Pro (Gemini 3 Pro) model to generate insightful "How-to" guide infographics. With Diagramma AI, you can easily create visually appealing and informative guides on a wide range of topics.

## Features

- **Infographic Generation:** Instantly generate "How-to" guides on any topic.
- **Customization Options:** Tailor the infographics to your needs with options for size, style, and layout.
- **Multiple Export Formats:** Export your infographics in JPG, PNG, or PDF formats for easy sharing and printing.

## Technologies Used

- **Nano-Banana Pro (Gemini 3 Pro):** The core AI model for generating the infographics.
- **Gradio:** Used to create the user-friendly web interface.
- **Python:** The programming language used to build the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/diagramma-ai.git
   ```
2. Navigate to the project directory:
   ```bash
   cd diagramma-ai
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to the local URL provided by Gradio (usually `http://127.0.0.1:7860`).
3. Enter a topic for your "How-to" guide.
4. Customize the infographic using the available options.
5. Click the "Generate" button to create your infographic.
6. Export the infographic in your desired format.

## Error Handling

In the event that the AI model fails to generate an infographic, the application will display a friendly sad face image (`sad-face.png`) to indicate that an error has occurred. This ensures a clear and user-friendly experience, even when things go wrong.
