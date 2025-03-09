#!/usr/bin/env python3
"""
Script to generate test data for the document RAG application.
This creates users, documents, and QA sessions for testing.
"""

import asyncio
import os
import sys
import random
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_async_session
from app.services.user_service import UserService
from app.services.document_service import DocumentService
from app.services.qa_session_service import QASessionService

# Sample documents for testing
SAMPLE_DOCUMENTS = [
    {
        "title": "Introduction to Python",
        "content": """
        Python is a high-level, interpreted programming language known for its readability and simplicity.
        It was created by Guido van Rossum and first released in 1991. Python's design philosophy emphasizes
        code readability with its notable use of significant whitespace. Its language constructs and
        object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects.

        Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including
        structured, object-oriented, and functional programming. Python is often described as a "batteries included"
        language due to its comprehensive standard library.

        Key features of Python include:
        1. Easy to learn and use
        2. Readable and maintainable code
        3. Extensive standard library
        4. Dynamic typing
        5. Interpreted nature
        6. Object-oriented programming support
        7. Integration capabilities with other languages
        8. Cross-platform compatibility

        Python is widely used in various fields such as web development, data analysis, artificial intelligence,
        scientific computing, and automation.
        """,
        "content_type": "text/plain"
    },
    {
        "title": "FastAPI Framework Overview",
        "content": """
        FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+
        based on standard Python type hints. It was created by Sebastián Ramírez and first released in 2018.

        Key features of FastAPI include:

        1. Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic).
        2. Fast to code: Increase the speed to develop features by about 200% to 300%.
        3. Fewer bugs: Reduce about 40% of human (developer) induced errors.
        4. Intuitive: Great editor support. Completion everywhere. Less time debugging.
        5. Easy: Designed to be easy to use and learn. Less time reading docs.
        6. Short: Minimize code duplication. Multiple features from each parameter declaration.
        7. Robust: Get production-ready code. With automatic interactive documentation.
        8. Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.

        FastAPI is built on top of Starlette for the web parts and Pydantic for the data parts.
        It leverages Python type hints for parameter declaration, validation, and conversion.

        FastAPI automatically generates OpenAPI documentation, which can be accessed through Swagger UI
        or ReDoc interfaces. This makes it easy to test and document your API.

        The framework is designed to be easy to use while still providing high performance and robustness.
        It's suitable for production environments and has been adopted by many companies and projects.
        """,
        "content_type": "text/plain"
    },
    {
        "title": "Introduction to Retrieval-Augmented Generation (RAG)",
        "content": """
        Retrieval-Augmented Generation (RAG) is a technique that combines retrieval-based and generation-based
        approaches for natural language processing tasks. It was introduced by researchers at Facebook AI
        (now Meta AI) in 2020.

        RAG works by first retrieving relevant documents or passages from a knowledge base and then using
        these retrieved documents as additional context for a language model to generate responses.
        This approach allows the model to access external knowledge without having to memorize all information
        during training.

        The key components of a RAG system include:

        1. Retriever: Responsible for finding relevant documents from a knowledge base given a query.
           This often uses dense vector embeddings and similarity search.

        2. Generator: A language model that takes the retrieved documents and the original query to
           generate a response. This is typically a sequence-to-sequence model like T5 or BART.

        3. Knowledge Base: A collection of documents or passages that contain information the system
           can reference. These documents are usually preprocessed and indexed for efficient retrieval.

        Advantages of RAG include:

        - Access to external knowledge without increasing model size
        - More factual and accurate responses
        - Ability to cite sources for generated information
        - Easier to update knowledge without retraining the entire model
        - More transparent decision-making process

        RAG has been successfully applied to various tasks such as question answering, fact verification,
        and open-domain dialogue systems. It represents an important step toward more knowledgeable and
        trustworthy AI systems.
        """,
        "content_type": "text/plain"
    },
    {
        "title": "PostgreSQL Database Management",
        "content": """
        PostgreSQL, often simply "Postgres," is an advanced, open-source object-relational database management
        system (ORDBMS). It was initially released in 1989 and has since become one of the most powerful and
        reliable database systems available.

        Key features of PostgreSQL include:

        1. ACID Compliance: PostgreSQL is fully ACID compliant (Atomicity, Consistency, Isolation, Durability),
           ensuring reliable transaction processing.

        2. Advanced Data Types: Support for a wide range of data types including JSON, XML, arrays, hstore,
           and user-defined types.

        3. Extensibility: Users can define custom functions, operators, data types, and index types.

        4. Concurrency Control: Multi-Version Concurrency Control (MVCC) allows readers and writers to work
           simultaneously without blocking each other.

        5. Robust Security: Features include SSL support, column and row-level security, and strong authentication
           mechanisms.

        6. Full-Text Search: Built-in full-text search capabilities with support for multiple languages.

        7. Geographic Objects: PostGIS extension provides robust support for geographic objects and location queries.

        8. Foreign Data Wrappers: Allow PostgreSQL to connect to other databases or data sources.

        9. Replication and High Availability: Support for streaming replication, logical replication, and various
           high-availability configurations.

        PostgreSQL is highly scalable and can handle large amounts of data and concurrent users. It's used by
        organizations of all sizes, from small startups to large enterprises, and is particularly popular in
        applications requiring complex queries, data warehousing, and geographic information systems.

        The database is developed by the PostgreSQL Global Development Group, a diverse community of companies
        and individual contributors. Its open-source nature, robust feature set, and strong community support
        make it an excellent choice for a wide range of database applications.
        """,
        "content_type": "text/plain"
    },
    {
        "title": "Asynchronous Programming in Python",
        "content": """
        Asynchronous programming in Python allows developers to write concurrent code that can handle many
        operations simultaneously without blocking the execution flow. This is particularly useful for I/O-bound
        operations like network requests, file operations, and database queries.

        Python's asyncio library, introduced in Python 3.4, provides a framework for writing asynchronous code.
        The key components of asyncio include:

        1. Coroutines: Functions defined with `async def` that can be paused and resumed. They are the building
           blocks of asynchronous programming in Python.

        2. Event Loop: The core of asyncio, responsible for executing coroutines, handling I/O operations, and
           managing the flow of execution.

        3. Awaitables: Objects that can be used with the `await` keyword, including coroutines, Tasks, and Futures.

        4. Tasks: Wrappers around coroutines that allow them to be scheduled for execution on the event loop.

        5. Futures: Objects representing the eventual result of an asynchronous operation.

        Benefits of asynchronous programming include:

        - Improved performance for I/O-bound operations
        - Better resource utilization
        - Handling many connections simultaneously
        - Non-blocking code execution

        A simple example of asynchronous code in Python:

        ```python
        import asyncio

        async def fetch_data():
            print("Start fetching data")
            await asyncio.sleep(2)  # Simulating an I/O operation
            print("Data fetched")
            return {"data": "result"}

        async def main():
            result = await fetch_data()
            print(result)

        asyncio.run(main())
        ```

        Python 3.7 introduced `asyncio.run()` to simplify running asynchronous programs, and Python 3.8 added
        the `asyncio.create_task()` function for easier task creation.

        Asynchronous programming is widely used in web servers, API clients, database access layers, and other
        applications where concurrent operations can significantly improve performance.
        """,
        "content_type": "text/plain"
    }
]

async def generate_test_data():
    """Generate test data for the application."""
    # Get a database session
    async for session in get_async_session():
        try:
            # Create services
            user_service = UserService()
            document_service = DocumentService()
            qa_session_service = QASessionService()

            # Create users
            print("Creating users...")
            admin_user = await user_service.create_user(
                session=session,
                username="admin",
                email="admin@example.com",
                password="adminpass123",
                is_superuser=True
            )
            print(f"Created admin user: {admin_user.username} (ID: {admin_user.id})")

            regular_user = await user_service.create_user(
                session=session,
                username="user",
                email="user@example.com",
                password="userpass123",
                is_superuser=False
            )
            print(f"Created regular user: {regular_user.username} (ID: {regular_user.id})")

            # Create documents for each user
            print("\nCreating documents...")
            admin_documents = []
            for i, doc_data in enumerate(SAMPLE_DOCUMENTS[:3]):
                doc = await document_service.create_document(
                    session=session,
                    user_id=admin_user.id,
                    title=doc_data["title"],
                    content=doc_data["content"],
                    content_type=doc_data["content_type"]
                )
                admin_documents.append(doc)
                print(f"Created document for admin: {doc.title} (ID: {doc.id})")

            user_documents = []
            for i, doc_data in enumerate(SAMPLE_DOCUMENTS[3:]):
                doc = await document_service.create_document(
                    session=session,
                    user_id=regular_user.id,
                    title=doc_data["title"],
                    content=doc_data["content"],
                    content_type=doc_data["content_type"]
                )
                user_documents.append(doc)
                print(f"Created document for user: {doc.title} (ID: {doc.id})")

            # Create QA sessions
            print("\nCreating QA sessions...")
            admin_qa_session = await qa_session_service.create_qa_session(
                session=session,
                user_id=admin_user.id,
                name="Programming Knowledge Base",
                document_ids=[doc.id for doc in admin_documents]
            )
            print(f"Created QA session for admin: {admin_qa_session.name} (ID: {admin_qa_session.id})")

            user_qa_session = await qa_session_service.create_qa_session(
                session=session,
                user_id=regular_user.id,
                name="Database and Async Programming",
                document_ids=[doc.id for doc in user_documents]
            )
            print(f"Created QA session for user: {user_qa_session.name} (ID: {user_qa_session.id})")

            print("\nTest data generation complete!")

        except Exception as e:
            print(f"Error generating test data: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(generate_test_data())
