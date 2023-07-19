from functions import *

def main():
    # secrets
    openai.api_key = os.getenv("OPENAI_API_KEY") # alternatively, you can simply put your OPEN AI key directly here
    session_id = os.getenv("TIKTOK_SESSION_ID")
    
    topic = ""
    print("Welcome to PhiloSim, an AI powered simulator for philosophical conversations.")
    # Ask user for inputs
    topic = input("topic: ")
    # generate a script
    script = generate_script(topic)

    # save the script, both audio and text
    script_path = save_script_and_audio(script, session_id)

    check_fix_audio(script_path)
    # play the script
    play_script(script_path)

if __name__ == "__main__":
   main()
    
        
    



    
