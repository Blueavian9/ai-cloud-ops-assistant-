import os
from dotenv import load_dotenv
from langchain.docstore.document import Document
from vector_store import VectorStore
import shutil

def setup_test_environment():
    """Set up test environment and return test documents."""
    # Load environment variables
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Create test documents
    test_docs = [
        Document(
            page_content="AWS EC2 is a web service that provides resizable compute capacity in the cloud.",
            metadata={"source": "aws_ec2.txt", "category": "compute"}
        ),
        Document(
            page_content="Amazon S3 is an object storage service that offers industry-leading scalability, data availability, security, and performance.",
            metadata={"source": "aws_s3.txt", "category": "storage"}
        ),
        Document(
            page_content="AWS Lambda lets you run code without provisioning or managing servers.",
            metadata={"source": "aws_lambda.txt", "category": "serverless"}
        ),
        Document(
            page_content="Amazon RDS is a managed relational database service that makes it easy to set up, operate, and scale databases in the cloud.",
            metadata={"source": "aws_rds.txt", "category": "database"}
        )
    ]

    return openai_api_key, test_docs

def cleanup_test_environment(directory: str):
    """Clean up test environment."""
    if os.path.exists(directory):
        shutil.rmtree(directory)

def test_vector_store():
    """Run comprehensive tests on the VectorStore implementation."""
    # Setup
    openai_api_key, test_docs = setup_test_environment()
    test_dir = "test_vector_store"
    
    try:
        # Initialize vector store
        print("\n1. Testing initialization...")
        vector_store = VectorStore(openai_api_key)
        print("✅ Initialization successful")

        # Test creating vector store with batch processing
        print("\n2. Testing vector store creation with batch processing...")
        vector_store.create_vector_store(test_docs, test_dir, batch_size=2)
        print("✅ Vector store creation successful")

        # Test loading vector store
        print("\n3. Testing vector store loading...")
        vector_store.load_vector_store(test_dir)
        print("✅ Vector store loading successful")

        # Test similarity search with different queries and score thresholds
        print("\n4. Testing similarity search with scoring...")
        test_queries = [
            ("What is AWS Lambda?", 0.7),
            ("Tell me about cloud storage", 0.6),
            ("How do I run code in the cloud?", 0.5)
        ]

        for query, threshold in test_queries:
            print(f"\nQuery: {query}")
            print(f"Score threshold: {threshold}")
            results = vector_store.similarity_search(query, k=2, score_threshold=threshold)
            print("Results:")
            for i, (doc, score) in enumerate(results, 1):
                print(f"\n{i}. Score: {score:.3f}")
                print(f"   Content: {doc.page_content}")
                print(f"   Source: {doc.metadata.get('source', 'Unknown')}")
                print(f"   Category: {doc.metadata.get('category', 'Unknown')}")

        print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise
    finally:
        # Cleanup
        cleanup_test_environment(test_dir)

if __name__ == "__main__":
    test_vector_store() 