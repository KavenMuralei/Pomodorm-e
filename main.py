import re
import time
from google import genai
from transcribe import transcribe, set_mute, is_muted, start_keyboard_listener, stop_keyboard_listener

client = genai.Client()


# cases:
# stop, listen, timer, question, roam
def main():
    state = "stop"
    last_transcript = ""  # Store transcript for use in other states
    
    # Start muted by default to avoid wasting API calls
    set_mute(True)
    
    # Start keyboard listener for 'M' key
    start_keyboard_listener(set_mute)
    print("\n=== Pomodorm-e State Machine ===")
    print("Press 'M' to toggle mute/unmute")
    print("When unmuted, you can speak commands: 'timer', 'question', 'roam'")
    print("Press 'M' again to mute and return to stop state")
    print("===========================\n")
    
    try:
        while True:
            match state:
                case "stop":
                    print("State: STOP (waiting)")
                    # In stop state, if unmuted, transition to listen
                    if not is_muted():
                        state = "listen"
                    else:
                        # Small sleep to prevent busy-waiting
                        time.sleep(0.1)
                        
                case "listen":
                    # In listen state, transcribe and parse for keywords
                    print("\nState: LISTEN (unmuted - recording)")
                    transcript = transcribe()
                    last_transcript = transcript  # Store for other states
                    print(f"Transcribed: {transcript}")
                    
                    # Parse transcript for state keywords
                    transcript_lower = transcript.lower()
                    if re.search(r"\b(timer|pomodoro)\b", transcript_lower):
                        state = "timer"
                    elif re.search(r"\b(question|ask)\b", transcript_lower):
                        state = "question"
                    elif re.search(r"\b(roam|free)\b", transcript_lower):
                        state = "roam"
                    else:
                        # If no keyword recognized, stay in listen
                        print("No recognized command, continuing to listen...")
                        state = "listen"
                    
                case "timer":
                    print("\nState: POMODORO_TIMER")
                    print("Starting 25-minute Pomodoro timer...")
                    # TODO: Implement timer logic
                    state = "stop"
                        
                case "question":
                    print("\nState: GEMINI_QUESTION")
                    # Extract question from stored transcript (remove keyword)
                    question = re.sub(r"\b(question|ask)\b", "", last_transcript, flags=re.IGNORECASE).strip()
                    if question:
                        print(f"Asking: {question}")
                        response = client.models.generate_content(
                            model="gemini-2-flash",
                            contents=question,
                        )
                        print(f"\nResponse:\n{response.text}\n")
                    state = "stop"
                        
                
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop_keyboard_listener()
                


if __name__ == "__main__":
    main()