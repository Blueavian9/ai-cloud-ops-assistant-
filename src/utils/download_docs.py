import os
import requests
from pathlib import Path
from tqdm import tqdm

def download_file(url: str, filename: str, data_dir: str) -> None:
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def download_aws_docs():
    """Download AWS documentation PDFs."""
    # Create data directory if it doesn't exist
    data_dir = "data"
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # List of AWS documentation PDFs to download
    docs = [
        {
            "url": "https://docs.aws.amazon.com/pdfs/cli/latest/userguide/aws-cli.pdf",
            "filename": "aws-cli-user-guide.pdf"
        },
        {
            "url": "https://docs.aws.amazon.com/pdfs/cli/latest/reference/aws-cli-reference.pdf",
            "filename": "aws-cli-reference.pdf"
        },
        {
            "url": "https://docs.aws.amazon.com/pdfs/ec2/latest/userguide/ec2-ug.pdf",
            "filename": "aws-ec2-user-guide.pdf"
        },
        {
            "url": "https://docs.aws.amazon.com/pdfs/s3/latest/userguide/s3-ug.pdf",
            "filename": "aws-s3-user-guide.pdf"
        },
        {
            "url": "https://docs.aws.amazon.com/pdfs/iam/latest/userguide/iam-ug.pdf",
            "filename": "aws-iam-user-guide.pdf"
        },
        {
            "url": "https://docs.aws.amazon.com/pdfs/wellarchitected/latest/framework/wellarchitected-framework.pdf",
            "filename": "aws-well-architected-framework.pdf"
        },
        {
            "url": "https://docs.aws.amazon.com/pdfs/whitepapers/latest/aws-security-best-practices/aws-security-best-practices.pdf",
            "filename": "aws-security-best-practices.pdf"
        }
    ]
    
    print("Downloading AWS documentation...")
    for doc in docs:
        try:
            download_file(doc["url"], doc["filename"], data_dir)
            print(f"✅ Downloaded {doc['filename']}")
        except Exception as e:
            print(f"❌ Failed to download {doc['filename']}: {str(e)}")
    
    print("\nDownload complete! The following documents are now available in the data directory:")
    for file in os.listdir(data_dir):
        print(f"- {file}")

if __name__ == "__main__":
    download_aws_docs() 