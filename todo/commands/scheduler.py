# todo/commands/scheduler.py
import time
import schedule
from todo.commands.autoclose_overdue import run

def main():
    schedule.every(15).minutes.do(run)

    print("Scheduler started. Running every 15 minutes. Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
