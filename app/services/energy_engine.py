from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Any

class EnergyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"  # e.g., haven't slept

class TaskPriority(str, Enum):
    P1 = "urgent"      # Do Now / High Impact
    P2 = "important"   # Deep Work / Strategy
    P3 = "routine"     # Admin / Maintenance
    P4 = "optional"    # Someday

def calculate_energy_window(sleep_duration: float, wake_time: datetime) -> EnergyLevel:
    """
    Determines baseline energy for the day based on sleep.
    """
    if sleep_duration < 5.0:
        return EnergyLevel.CRITICAL
    elif sleep_duration < 7.0:
        return EnergyLevel.LOW
    else:
        return EnergyLevel.HIGH

def suggest_optimization(current_energy: EnergyLevel, pending_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Core Logic: Suggests rescheduling based on real-time energy input.
    Use Case: User says 'My energy is good'.
    """
    suggestion = {
        "action": "maintain",
        "reason": "Schedule aligns with energy.",
        "moved_tasks": []
    }

    if current_energy == EnergyLevel.HIGH:
        # Strategy: Pull forward P2 (Deep Work) tasks
        deep_work_tasks = [t for t in pending_tasks if t['priority'] == TaskPriority.P2]
        if deep_work_tasks:
            suggestion = {
                "action": "prioritize_deep_work",
                "reason": "Since your energy is high, let's tackle deep work now.",
                "moved_tasks": deep_work_tasks
            }
            
    elif current_energy == EnergyLevel.LOW:
        # Strategy: Push P2 tasks, focus on P3 (Routine) or Rest
        suggestion = {
            "action": "conserve_energy",
            "reason": "Energy is low. Recommended moving deep work to later or tomorrow.",
            "moved_tasks": []  # Logic to find tasks to defer
        }

    return suggestion
