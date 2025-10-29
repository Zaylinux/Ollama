#!/usr/bin/env python3
"""
Simplified privateGPT that works with processed documents
"""
import os
import time
import re
from typing import List, Tuple

try:
    from langchain_community.llms import Ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: Ollama integration not available")

def load_processed_documents(file_path: str = "processed_documents.txt") -> List[str]:
    """Load the processed document chunks"""
    if not os.path.exists(file_path):
        print(f"❌ Processed documents file '{file_path}' not found!")
        print("Please run the ingest script first.")
        return []
    
    chunks = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Split by chunk separators
        chunk_parts = content.split("=== CHUNK")
        for part in chunk_parts[1:]:  # Skip the first empty part
            # Extract the actual content (remove chunk number and separators)
            lines = part.split('\n')
            chunk_content = '\n'.join(lines[1:]).strip()
            chunk_content = chunk_content.replace('='*50, '').strip()
            if chunk_content:
                chunks.append(chunk_content)
    
    return chunks

def simple_search(query: str, chunks: List[str], max_results: int = 4) -> List[Tuple[str, float]]:
    """Simple keyword-based search through document chunks"""
    query_words = set(query.lower().split())
    results = []
    
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        # Calculate simple relevance score based on word overlap
        overlap = len(query_words.intersection(chunk_words))
        if overlap > 0:
            score = overlap / len(query_words)
            results.append((chunk, score))
    
    # Sort by relevance score and return top results
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:max_results]

def format_context(search_results: List[Tuple[str, float]]) -> str:
    """Format search results into context for the LLM"""
    if not search_results:
        return "No relevant information found in the documents."
    
    context = "Based on the following information from your documents:\n\n"
    for i, (chunk, score) in enumerate(search_results, 1):
        # Truncate very long chunks
        display_chunk = chunk[:500] + "..." if len(chunk) > 500 else chunk
        context += f"Document {i} (relevance: {score:.2f}):\n{display_chunk}\n\n"
    
    return context

def query_ollama(prompt: str, model: str = "mistral") -> str:
    """Query Ollama with the given prompt"""
    if not OLLAMA_AVAILABLE:
        return "❌ Ollama integration not available. Please install langchain-community."
    
    try:
        llm = Ollama(model=model)
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f"❌ Error querying Ollama: {e}"

def create_prompt(query: str, context: str) -> str:
    """Create a prompt for the LLM with context and query"""
    return f"""You are a helpful assistant that answers questions based on provided documents.

Context from documents:
{context}

Question: {query}

Please provide a helpful answer based on the information in the documents. If the documents don't contain relevant information, please say so clearly.

Answer:"""

def main():
    print("🚀 Starting Simple PrivateGPT...")
    print("📚 Loading processed documents...")
    
    # Load processed documents
    chunks = load_processed_documents()
    if not chunks:
        return
    
    print(f"✅ Loaded {len(chunks)} document chunks")
    print("🤖 Connecting to Ollama...")
    
    # Test Ollama connection
    if OLLAMA_AVAILABLE:
        try:
            test_llm = Ollama(model="mistral")
            test_response = test_llm.invoke("Hello")
            print("✅ Ollama connection successful!")
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            print("Please make sure Ollama is running and the mistral model is available.")
            return
    else:
        print("❌ Ollama not available")
        return
    
    print("\n" + "="*60)
    print("🎉 Simple PrivateGPT is ready!")
    print("💬 Ask questions about your documents")
    print("📝 Type 'exit' to quit")
    print("="*60)
    
    # Interactive chat loop
    while True:
        try:
            query = input("\n🔍 Enter your question: ").strip()
            
            if query.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("🔎 Searching documents...")
            start_time = time.time()
            
            # Search for relevant chunks
            search_results = simple_search(query, chunks)
            
            if not search_results:
                print("❌ No relevant information found in your documents.")
                continue
            
            # Format context
            context = format_context(search_results)
            
            # Create prompt
            prompt = create_prompt(query, context)
            
            print("🤖 Generating response...")
            
            # Query Ollama
            response = query_ollama(prompt)
            
            end_time = time.time()
            
            # Display results
            print("\n" + "="*60)
            print(f"❓ Question: {query}")
            print("="*60)
            print(f"🤖 Answer:\n{response}")
            print("="*60)
            print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
            print(f"📄 Found {len(search_results)} relevant document sections")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()