#!/usr/bin/env python3
"""
Helper script to create a test user in Redis.

Usage:
    python scripts/create_user.py <username> <password>

Example:
    python scripts/create_user.py testuser3 mypassword
"""

import asyncio
import sys
import os
import uuid
import bcrypt

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import redis.asyncio as redis


async def create_user(username: str, password: str, redis_host: str = "localhost", redis_port: int = 6379):
    """Create a user in Redis."""
    redis_client = redis.Redis(
        host=redis_host, port=redis_port, decode_responses=True
    )
    
    try:
        user_exists = await redis_client.exists(f"user:{username}")
        if user_exists:
            print(f"User '{username}' already exists.")
            return False
        
        user_id = str(uuid.uuid4())
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
        hashed_password = hashed.decode('utf-8')
        
        await redis_client.hset(
            f"user:{username}",
            mapping={
                "user_id": user_id,
                "username": username,
                "hashed_password": hashed_password,
            },
        )
        
        print(f"User '{username}' created successfully!")
        print(f"  Username: {username}")
        print(f"  User ID: {user_id}")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        await redis_client.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/create_user.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    
    asyncio.run(create_user(username, password, redis_host, redis_port))


if __name__ == "__main__":
    main()

