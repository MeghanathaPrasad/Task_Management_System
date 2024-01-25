import mysql.connector
import pandas as pd
from datetime import datetime, timedelta


class TaskManager:
    def __init__(self, db_host, db_user, db_password, db_database):
        self.connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks_ (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                due_date DATE NOT NULL,
                priority INT DEFAULT 1,
                assigned_to VARCHAR(255),
                status VARCHAR(20) DEFAULT 'Pending',
                completed BOOLEAN NOT NULL
            )
        ''')
        self.connection.commit()
    


    def add_task(self, title, description, due_date, priority=1, assigned_to=None):
        query = "INSERT INTO tasks_ (title, description, due_date, priority, assigned_to, completed) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (title, description, due_date, priority, assigned_to, False)
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f'Task "{title}" added successfully!')

    def view_tasks(self, assigned_to=None):
        if assigned_to:
            query = "SELECT id, title, due_date, priority, status, completed FROM tasks_ WHERE assigned_to = %s"
            values = (assigned_to,)
        else:
            query = "SELECT id, title,  due_date, priority, status, completed FROM tasks_"
            values = None

        self.cursor.execute(query, values)
        tasks = self.cursor.fetchall()

        if not tasks:
            print("No tasks available.")
        
        else:
            
            for task in tasks:
                status = "Completed" if task[5] else task[4]
                print(f"{task[0]} task title: {task[1]} - Due Date: {task[2]} - Priority: {task[3]} - Status: {status}")

        

    def update_task_details(self, task_id, status=None, due_date=None):
        updates = []
        if status:
            updates.append(("status", status))
        if due_date:
            updates.append(("due_date", due_date))

        if not updates:
            print("No updates provided.")
            return

        set_clause = ", ".join([f"{field} = %s" for field, _ in updates])
        values = [value for _, value in updates]
        values.append(task_id)

        query = f"UPDATE tasks_ SET {set_clause} WHERE id = %s"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f'Task with ID {task_id} updated successfully.')

    def assign_task(self, task_id, assigned_to):
        query = "UPDATE tasks_ SET assigned_to = %s WHERE id = %s"
        values = (assigned_to, task_id)
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f'Task with ID {task_id} assigned to {assigned_to}.')

    
    def view_assign_task(self, assigned_to=None):
        if assigned_to:
            query = "SELECT id, title, due_date, priority, status FROM tasks_ WHERE assigned_to = %s"
            values = (assigned_to,)
        else:
            query = "SELECT id, title,  due_date, priority, status FROM tasks_"
            values = None

        self.cursor.execute(query, values)
        tasks = self.cursor.fetchall()

        if not tasks:
            print("No tasks available.")
        
        else:
            
            for task in tasks:
                print(f"{task[0]} task title: {task[1]} - Due Date: {task[2]} - Priority: {task[3]} - Status: {task[4]}")
        
    
    def mark_task_completed(self, task_id):
        query = "UPDATE tasks_ SET status = 'completed' WHERE id = %s"
        values = (task_id,)
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f'Task with ID {task_id} marked as completed.')

    def remove_task(self, task_id):
        query = "DELETE FROM tasks_ WHERE id = %s"
        values = (task_id,)
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f'Task with ID {task_id} removed successfully.')

    def members(self):
        query = "SELECT assigned_to FROM tasks_"
        values = None
        self.cursor.execute(query, values)
        tasks = self.cursor.fetchall()
        self.connection.commit()

        if not tasks:
            print("No tasks available.")
        
        else:  
            for task in tasks:
                print(task)
