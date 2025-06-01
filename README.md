# AI Cloud Ops Assistant

A modern web application that helps cloud engineers get instant, reliable, and sourced answers about AWS operations using RAG (Retrieval-Augmented Generation).

## Features

- 🤖 AI-powered Q&A about AWS services and best practices
- 📚 Real-time search through AWS documentation
- 💡 Detailed answers with source citations
- 🌙 Dark/Light mode support
- 📱 Responsive design
- 🔍 Topic-based navigation
- 💾 Save and share answers
- ⚡ Fast and modern UI

## Tech Stack

### Frontend
- Vite + React + TypeScript
- Tailwind CSS for styling
- ShadCN UI components
- React Query for data fetching
- React Router for navigation

### Backend
- Node.js + Express
- OpenAI API for LLM
- Supabase PGVector for vector storage
- LangChain for RAG implementation

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn
- OpenAI API key
- Supabase account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-cloud-ops-assistant.git
cd ai-cloud-ops-assistant
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```env
VITE_OPENAI_API_KEY=your_openai_api_key
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

4. Start the development server:
```bash
npm run dev
```

## Project Structure

```
ai-cloud-ops-assistant/
├── src/
│   ├── components/     # React components
│   ├── lib/           # Utility functions
│   ├── hooks/         # Custom React hooks
│   ├── types/         # TypeScript types
│   └── App.tsx        # Main App component
├── public/            # Static assets
├── index.html         # Entry HTML file
└── package.json       # Project dependencies
```

## Development Roadmap

### Phase 1: MVP (2-3 weeks)
- [x] Basic UI setup
- [x] Chat interface
- [x] RAG implementation
- [x] Vector store integration

### Phase 2: Core Features (2-4 weeks)
- [ ] AWS docs crawler
- [ ] User authentication
- [ ] Saved answers
- [ ] Topic browsing

### Phase 3: Scale & Polish (1-2 months)
- [ ] Live search
- [ ] Feedback system
- [ ] Analytics dashboard
- [ ] Deployment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- AWS Documentation
- OpenAI
- LangChain
- Supabase
- ShadCN UI
