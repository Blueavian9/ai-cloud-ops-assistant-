// config.js
const { openaiKey, groqKey } = require('./server');

const config = {
    // API Configuration
    openai: {
        apiKey: openaiKey,
        model: 'gpt-4-turbo-preview',
        temperature: 0.7,
        maxTokens: 2000
    },
    groq: {
        apiKey: groqKey,
        model: 'mixtral-8x7b-32768',
        temperature: 0.7,
        maxTokens: 2000
    },

    // Application Settings
    app: {
        port: process.env.PORT || 3000,
        environment: process.env.ENVIRONMENT || 'development',
        debug: process.env.ENVIRONMENT === 'development'
    },

    // RAG System Settings
    rag: {
        chunkSize: 1000,
        chunkOverlap: 200,
        vectorStorePath: './data/vectorstore',
        documentPath: './data/documents'
    }
};

module.exports = config; 