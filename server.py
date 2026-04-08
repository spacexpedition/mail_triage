import uvicorn
from env import app

def main():
    """
    Main entry point for the OpenEnv server.
    This function satisfies the requirement for a 'main' function reference.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()