import math
import random
import string
import functools
from fastapi import FastAPI
import re
import csv
from io import StringIO
from enum import Enum
import socket
from collections import deque
import subprocess
import os

app = FastAPI()

status_pipeline = ['backlog', 'in_progress', 'review', 'done' ]

class BeginningPhase:
    def __init__(self, initiation, planning, execution):
        self.initiation = initiation
        self.planning = planning
        self.execution = execution
        self.tasks = []
    def load_tasks(self, task_input):
          if isinstance(task_input, str):
                self.tasks.append(task_input)
          elif isinstance(task_input, (list, tuple)):
                for item in task_input:
                      if isinstance(item, (list, tuple)):
                            self.tasks.append(" ".join(item))
                      elif isinstance(item, str):
                            random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 3))
                            tagged_task = f"{item.strip()} [ID:{random_id}]"
                            self.tasks.append(tagged_task)
                      else:
                            self.tasks.append(str(item))
          elif isinstance(task_input, dict):
                self.tasks.extend(task_input.keys())
          else: 
                raise ValueError("Unsupported task data type")
            

    def review_tasks(self):
          finishedTasks = []
          unfinishedTasks = []
          for task in self.tasks:
                if ("urgent" in task.lower()
                    or "important" in task.lower()
                    or "critical" in task.lower()
                    or "priority" in task.lower()
                    ):
                     project_list = task + " +  is done"
                     level_of_urgency = math.ceil(len(task) * 1.5)
                     finishedTasks.append((project_list, level_of_urgency))
                else:
                    unfinishedTasks.append(f"{task} needs to get done")
          return finishedTasks, unfinishedTasks

def simulate_connection():
    try:
          s = socket.create_connection(("127.0.0.1", 9999), timeout = 2)
          return "Connection successful"
    except ConnectionRefusedError:
          return "ConnectionRefusedError: Could not connect to the server"
    except Exception as e:
          return f"Other error: {type(e).__name__} - {e}"
    

  # DATA STRUCTURES: LINKED LIST  
class TaskNode:
      def __init__(self, data):
            self.data = data
            self.next = None

class TaskLinkedList:
      def __init__(self):
            self.head = None
      def append(self, data):
            new_node = TaskNode(data)
            if not self.head:
                  self.head = new_node
                  return
            current = self.head
            while current.next:
                  current = current.next
            current.next = new_node
      def display(self):
            tasks = []
            current = self.head
            while current:
                  tasks.append(current.data)
                  current = current.next
            return tasks
     


# === SORTING THROUGH TASKS ===
def sort_tasks_by_length(task_list):
          return sorted(task_list, key = len) 

def sort_tasks_by_keyword_priority(task_list):
          def priority_value(task):
                task_lower = task.lower()
                if "critical" in task_lower:
                      return 1   
                elif "urgent" in task_lower:
                      return 2
                elif "important" in task_lower:
                      return 3
                elif "priority" in task_lower:
                      return 4
                else: 
                      return 5
          return sorted(task_list, key = priority_value)  
    
def sort_tasks_alphabetically(task_list, reverse=False):
          return sorted(task_list, reverse=reverse)
  


# === SETS AND FROZENSETS ===
def get_unique_tags(*tag_groups):
          all_tags = set()
          for group in tag_groups:
                all_tags.update(group)
          return frozenset(all_tags)
    
tags1 = ["urgent", "planning", "execution"]
tags2 = ["execution", "control", "review"]
unique_tags = get_unique_tags(tags1, tags2)

def find_common_team_members(team_a, team_b):
          return set(team_a) & set(team_b)
    
team1 = ["alice", "bob", "charlie"]
team2 = ["charlie", "dana", "bob"]
common_members = find_common_team_members(team1, team2)


# === BINARY SEARCH ===
def binary_search_task_by_title(task_list, target_title):
    sorted_tasks = sorted(task_list)
    low = 0
    high = len(sorted_tasks) -1

    while low <= high:
          mid = (low + high) // 2
          mid_task = sorted_tasks[mid]
          if mid_task == target_title:
                return mid
          elif mid_task < target_title:
                low = mid +1
          else:
                high = mid -1
    return -1

      
      # === GRAPH TRAVERSAL DFS ===
def dfs_traverse(graph, start_task, visited=None):
       """
    Performs a Depth-First Search traversal of a task graph.
    Returns the list of visited tasks in order.
    """
       if visited is None:
             visited = []
       visited.append(start_task)
       for neighbor in graph.get(start_task, []):
             if neighbor not in visited:
                   dfs_traverse(graph, neighbor, visited)
       return visited



# === DYNAMIC PROGRAMMING: TASK SELECTION
def select_tasks_by_value(tasks, max_capacity):
 
      n = len(tasks)
      dp = [[0] * (max_capacity +1) for _ in range(n +1)]
      for i in range(1, n + 1):
            name, value, cost = tasks[i - 1] 
            for c in range(max_capacity + 1):
                  if cost > c:
                        dp[i][c] = dp[i - 1][c]
                  else:
                        dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - cost] + value)

      selected = []  
      c = max_capacity
      for i in range(n, 0, -1):
            if dp[i][c] != dp[i-1][c]:
                  name, value, task = tasks[i-1]
                  selected.append(name)
                  c -= cost
      return {
            "max_value": dp[n][max_capacity],
            "selected_tasks": selected[::-1]
      }

tasks = [
    ("Prototype", 7, 3),
    ("Testing", 6, 2),
    ("Documentation", 4, 1),
    ("Deployment", 8, 4),
]

best = select_tasks_by_value(tasks, max_capacity=5)


# DATA STRUCTURES: QUEUE
class TaskQueue:
      def __init__(self):
            self.queue = deque()

      def enqueue(self, task):
            self.queue.append(task)

      def dequeue(self):
            if not self.queue:
                  return None
            return self.queue[0]
      
      def is_empty(self):
            return len(self.queue) == 0
      
      def size(self):
            return len(self.queue)
      

# DATA STRUCTURES: STACK
class TasksStack:
      def __init__(self):
            self.stack = []
      def push(self, task):
            self.stack.append(task)
      def pop(self):
            if not self.stack:
                  return None
            return self.stack.pop()
      
      def peek(self):
            if not self.stack:
                  return None
            return self.stack[-1]
      
      def is_empty(self):
            return len(self.stack) == 0
      def size(self):
            return len(self.stack)


#  STRING ANALYSIS: LCP
def longest_common_prefix(strings):
      if not strings:
            return ""
      
      strings.sort()
      first = strings[0]
      last = strings[-1]
      prefix = ""

      for i in range(min(len(first), len(last))):
            if first[i] == last[i]:
                  prefix += first[i]
            else:
                  break
      return prefix



 #REGEX PATTERNS
def match_task_code(text):
      pattern = r'\b(?:PRJ|TASK|BUG) - \d{1, 4}\b'
      return re.findall(pattern, text)
text = "Update PRJ-001, check TASK-42, and ignore BUG-999 for now"



import re

def extract_emails_and_deadlines(task_list):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    deadline_pattern = r'\d{4}-\d{2}-\d{2}'
    
    emails = []
    deadlines = []
    
    for text in task_list:
        emails.extend(re.findall(email_pattern, text))
        deadlines.extend(re.findall(deadline_pattern, text))
    
    return {"emails": emails, "deadlines": deadlines}

text = "Contact alice@acme.com or bob_dev@example.org. Deadline: 2025-09-01. Another task is due by 2025-10-15."



# CSV EXPORT
def export_tasks_to_csv(task_list):
      output = StringIO()
      writer = csv.writer(output)
      writer.writerow(["Task"])

      for task in task_list:
            writer.writerow([task])
      return output.getvalue()


def export_task_dicts_to_csv(task_dicts):
      if not task_dicts:
            return ""

      output = StringIO()
      fieldnames = task_dicts[0].keys()
      writer = csv.DictWriter(output, fieldnames = fieldnames)
      writer.writeheader()

      for row in task_dicts:
            writer.writerow(row)
      return output.getvalue()

task_data = [
    {"title": "urgent fix", "status": "in_progress"},
    {"title": "plan Q4", "status": "backlog"},
]

csv_data = export_task_dicts_to_csv(task_data)



# DATA STRUCTURES: HASH MAP
def group_tasks_by_priority(task_list):
      priority_map = {
            "high": [],
            "medium": [],
            "low": []
      }
      for task in task_list:
            lower = task.lower()
            if "critical" in lower or "urgent" in lower:
                  priority_map["high"].append(task)
            elif "important" in lower:
                  priority_map["medium"].append(task)
            else:
                  priority_map["low"].append(tasks)
      return priority_map

def group_tasks_by_priority(task_list):
      priority_map = {
            "high": [],
            "medium": [],
            "low": []
      }

      for task in task_list:
            lower = task.lower()
            if "critical" in lower or "urgent" in lower:
                  priority_map["high"].append(task)
            elif "important" in lower:
                  priority_map["medium"].append(task)
            else:
                  priority_map["low"].append(tasks)
      return priority_map


# ENUMS
class ProjectStatus(Enum):
      BACKLOG = "backlog"
      IN_PROGRESS = "in_progress"
      REVIEW =  "review"
      DONE = "done"

      def is_valid_status(status: str):
            try:
                  ProjectStatus(status)
                  return True
            except ValueError:
                  return False
            
      def convert_to_status_enum(status: str):
            return ProjectStatus(status)

# PYTHON CORE: REFERNCE VS VALUE
def demonstrate_reference_vs_value():
      original = ["alpha", "beta", "gamma"]
      reference = original
      value_copy = original[:]
      reference.append("delta")
      value_copy.append("epsilon")

      return {
            "original": original,
            "reference": reference,
            "value_copy": value_copy
      }

# FILE SYSTEM + CHILD PROCESS INTEGRATION
def export_tasks_to_csv(tasks_with_status, filepath="exported_tasks.csv"):
      try:
            with open(filepath, "w") as f:
                  for task, status in tasks_with_status:
                        f.write(f"{task}, {status}\n")
            return f"Successfully exported to {filepath}"
      except Exception as e:
            return f"Error exporting CSV: {e}"


def open_csv_file(filepath="exported_tasks.csv"):
      try:
            if not os.path.exists(filepath):
                  return f"FileNotFoundError: '{filepath}' does not exist."
            
            #MacOS
            if os.name == "posix":
                  subprocess.run(["open",filepath], check = True)

            #windows
            elif os.name == "nt":
                  os.startfile(filepath)

            #linux
            else:
                  subprocess.run(["xdg-open", filepath])
            return f"Opened file: {filepath}"
      
      except FileNotFoundError:
            return "System command not found. Could not open CSV."
      except subprocess.CalledProcessError:
            return "CalledProcessError: Failed to open CSV"
      except Exception as e:
            return f"Unhandled error: {type(e).__name__} - {e}"



def case_study(self, task1, task2):
          process = f"Analyzing {task1} and {task2}"
          infrastructure = "tools"
          return f"{process} using {infrastructure}"

class Monitoring(BeginningPhase):
            def __init__(self, initiation, planning, execution, control):
                super().__init__(initiation, planning, execution)
                self.control = control
            def case_study(self, task1, task2):
                  process = f"Analyzing {task1} and {task2}"
                  infrastructure = "tools"
                  return f"{process} using {infrastructure}"
            def control_applied(self, risk):
                  return f"If '{risk}' occurs, apply control method {self.control}"


@app.get("/tasks/review")
def get_reviewed_tasks():
      finished, unfinished = pm_phase.review_tasks()
      return {
            "finished" : finished,
            "unfinished" : unfinished
      }


@functools.lru_cache(maxsize=64)
def memoized_effort_estimate(n):
      if n <= 1:
            return 1
      return memoized_effort_estimate(n -1) + memoized_effort_estimate(n -2)


pm_phase = Monitoring("initiation", "planning", "execution", "control")

pm_phase.load_tasks(["urgent client request", "check status report"])
pm_phase.load_tasks([
    ["urgent meeting"],
    ["project charter on starlink"],
    ["business Scope for starlink HQ building"],
    ["important starlink deadline"]
])
pm_phase.load_tasks({
    "call starbucks CEO": "priority/tomorrow @11AM",
    "call Meijers district manager": "eventually",
    "monitor budget for starlink project": "critical",
    "agile or waterfall?": "critical"
})


task_graph = {
      "Plan": ["Design", "Budget"],
      "Design": ["Prototyping"],
      "Prototyping": ["Review"],
      "Budget": [],
      "Review": ["Approval"],
      "Approval": []
      }


task_list = pm_phase.tasks
target = "urgent client request"
csv_data = export_tasks_to_csv(task_list)


index = binary_search_task_by_title(task_list, target)
if index != -1:
      print(f"Found '{target}' at index '{index}'")
else: 
      print(f"'{target}' not found")

visted_order = dfs_traverse(task_graph, "Plan")
result = pm_phase.case_study("A", "B")
bp = BeginningPhase(pm_phase.initiation, pm_phase.planning, pm_phase.execution)    

sample_tasks = [
    "john@boot.com - due by 2025-07-31",
    "daveMac@oswego.edu, deadline: 2026-12-01",
    "maldaven@nyker.org (due by 2023-01-23)"
]
print(extract_emails_and_deadlines(sample_tasks))


def __repr__(self):
          return (
                f"<Monitoring(initiation='{self.initiation}', "
                f"planning='{self.planning}', "
                f"control='{self.control}', "
                f"tasks={len(self.tasks)})>"
          )


if __name__ == "__main__":
            # print("Linked List Tasks:", task_ll.display())
      print("Best Task Combo:", best)
# Output: Best Task Combo: [('Testing', 6, 2), ('Deployment', 8, 4)] — OR similar
# titles = [
#     "project-alpha",
#     "project-beta",
#     "project-charlie",
#     "project-omega"
# ]
# print("Common Prefix:", longest_common_prefix(titles))
# Output: "project-"
      print(match_task_code(text))
      print(extract_emails_and_deadlines("Reach out to mochi@iu.com by 2025-09-10."))
# Output:
# {
#'emails': ['alice@acme.com', 'bob_dev@example.org'],
#'deadlines': ['Deadline: 2025-09-01', 'due by 2025-10-15']
#}
      print(csv_data)
      print(open_csv_file())  # Default: exported_tasks.csv
      q = TaskQueue()
      q.enqueue("Sync calendar")
      q.enqueue("Send client invoice")
      q.enqueue("Clean up project board")
      print("Next task:", q.peek())     # Sync calendar
      print("Dequeued:", q.dequeue())   # Sync calendar
      print("Next up:", q.peek())       # Send client invoice

      result = demonstrate_reference_vs_value()
      print("Original:", result["original"])
      print("Reference:", result["reference"])
      print("Value Copy:", result["value_copy"])
