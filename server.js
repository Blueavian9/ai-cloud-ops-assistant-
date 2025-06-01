require('dotenv').config();

// Environment variables
const openaiKey = process.env.OPENAI_API_KEY;
const groqKey = process.env.GROQ_API_KEY;

// Validate environment variables
if (!openaiKey) {
    console.error('Error: OPENAI_API_KEY is not set in environment variables');
    process.exit(1);
}

if (!groqKey) {
    console.warn('Warning: GROQ_API_KEY is not set in environment variables');
}

// Log successful loading (without exposing keys)
console.log('Environment variables loaded successfully:');
console.log('- OPENAI_API_KEY:', openaiKey ? '✓' : '✗');
console.log('- GROQ_API_KEY:', groqKey ? '✓' : '✗');

// Export for use in other files
module.exports = {
    openaiKey,
    groqKey
}; 