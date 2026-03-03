# Devines Backend Service

Minimal Node.js Express backend for Devines with streaming chat and CHAOS codex injection.

## Deploy on Render (Web Service)

1. Push repository to GitHub.
2. In Render, create a New Web Service from the repository.
3. Use:
   - Environment: Node
   - Build Command: npm install
   - Start Command: npm start
4. Add environment variable:
   - OPENAI_API_KEY = your OpenAI API key
5. Deploy.

Service listens on process.env.PORT || 10000.

## API

POST /chat

Body:

{
  "messages": [
    { "role": "user", "content": "Hello CHAOS" }
  ],
  "devine": "chaos"
}
