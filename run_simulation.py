import sys
import os

# Ensure backend root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.energy_engine import suggest_optimization, EnergyLevel, TaskPriority

def run_simulation():
    # Scenario: User says "I feel great, energy is high!"
    print("--- Voice Input Simulation ---")
    user_input_text = "I feel great, energy is high!"
    print(f"User Voice: '{user_input_text}'")
    
    # 1. Parsing (Mocked)
    detected_energy = EnergyLevel.HIGH
    print(f"-> Parsed Energy: {detected_energy.value.upper()}")
    
    # 2. Logic Engine
    # Assume 2 tasks: Routine Email (Now), Hard ML Project (Tomorrow)
    pending_tasks = [
        {"id": 1, "title": "Reply to Emails", "priority": TaskPriority.P3, "time": "Now"},
        {"id": 2, "title": "Machine Learning Algorithm Design", "priority": TaskPriority.P2, "time": "Tomorrow 10:00"}
    ]
    
    print("\n--- Current Schedule ---")
    for task in pending_tasks:
        print(f"- {task['title']} ({task['priority'].value}, {task['time']})")
        
    print("\n--- Engine Processing ---")
    suggestion = suggest_optimization(detected_energy, pending_tasks)
    
    print(f"Engine Decision: {suggestion['action']}")
    print(f"Logic: {suggestion['reason']}")
    
    if suggestion['moved_tasks']:
        moved = suggestion['moved_tasks'][0]
        print(f"\n--- AI Output (Voice) ---")
        print(f"ASSISTANT: 'Great to hear! Since you're energetic, should we tackle the **{moved['title']}** now instead of emails? It's your hardest task for the week.'")
        
if __name__ == "__main__":
    run_simulation()
