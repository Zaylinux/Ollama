#!/usr/bin/env python3
"""
Simplified ingest script for privateGPT
"""
import os
import glob
from typing import List
from tqdm import tqdm

# Simple document processing without complex embeddings
def load_documents(source_dir: str = "source_documents") -> List[str]:
    """Load and process documents from source directory"""
    all_files = []
    
    # Support basic file types
    extensions = [".txt", ".md", ".pdf"]
    
    for ext in extensions:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    
    documents = []
    print(f"Found {len(all_files)} files to process")
    
    for file_path in tqdm(all_files, desc="Loading documents"):
        try:
            if file_path.endswith('.pdf'):
                # Use PyMuPDF for PDF files
                import fitz
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                documents.append(f"File: {file_path}\n\n{text}")
            else:
                # Handle text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    documents.append(f"File: {file_path}\n\n{content}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue
    
    return documents

def chunk_documents(documents: List[str], chunk_size: int = 1000) -> List[str]:
    """Split documents into chunks"""
    chunks = []
    
    for doc in documents:
        # Simple chunking by character count
        for i in range(0, len(doc), chunk_size):
            chunk = doc[i:i + chunk_size]
            if len(chunk.strip()) > 50:  # Only keep meaningful chunks
                chunks.append(chunk)
    
    return chunks

def save_processed_documents(chunks: List[str], output_file: str = "processed_documents.txt"):
    """Save processed documents to a text file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"=== CHUNK {i+1} ===\n")
            f.write(chunk)
            f.write("\n\n" + "="*50 + "\n\n")
    
    print(f"Saved {len(chunks)} chunks to {output_file}")

def main():
    print("🚀 Starting simplified document ingestion...")
    
    # Check if source directory exists
    source_dir = "source_documents"
    if not os.path.exists(source_dir):
        print(f"❌ Source directory '{source_dir}' not found!")
        return
    
    # Load documents
    print("📄 Loading documents...")
    documents = load_documents(source_dir)
    
    if not documents:
        print("❌ No documents found to process!")
        return
    
    print(f"✅ Loaded {len(documents)} documents")
    
    # Chunk documents
    print("✂️  Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Save processed documents
    print("💾 Saving processed documents...")
    save_processed_documents(chunks)
    
    print("🎉 Document ingestion complete!")
    print("📝 Your documents have been processed and saved to 'processed_documents.txt'")
    print("🔍 You can now use these processed documents with your privateGPT application")

if __name__ == "__main__":
    main()