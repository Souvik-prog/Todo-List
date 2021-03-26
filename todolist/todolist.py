# Write your code here
import todo_db
from datetime import datetime, timedelta
class todo:
    def _init_(self):
        self.todo_list = []
    def today_tasks(self):
        today = datetime.today()
        print("Today:",today.strftime("%d %b"))
        # Get all rows of the table as a python list
        self.todo_list = todo_db.session.query(todo_db.Table).all()
        if len(self.todo_list) == 0:
            print("Nothing to do!")
            return
        self.print_tasks()
        return
    def week_tasks(self):
        start_day = datetime.today()
        start_day1 = datetime.today() - timedelta(days=1)
        end_day = datetime.today() + timedelta(days=7)
        self.rows = ( todo_db.session.query(todo_db.Table)
                      .filter(todo_db.Table.deadline.between(start_day1,end_day))
                      .order_by(todo_db.Table.deadline)
                      .all()
                      )
        print(self.rows)
        date_range = [
            start_day + timedelta(days=day)
            for day in range((end_day - start_day).days)
        ]
        row_deadline = [row.deadline.strftime('%A %d %b:') for row in self.rows]
        for day in date_range:
            print(day.strftime('%A %d %b:'))
            if day.strftime('%A %d %b:') not in row_deadline:
                print("Nothing to do!\n")
            else:
                i = 1
                for row in self.rows:
                    if row.deadline.strftime('%A %d %b:') == day.strftime('%A %d %b:'):
                        print(str(i)+". "+row.task)
                        i +=1
                print("\n")
    def all_tasks(self):
        print("All Tasks:")
        self.rows = todo_db.session.query(todo_db.Table).order_by(todo_db.Table.deadline).all()
        for row in self.rows:
            print(row,end="")
            print(". ",end="")
            x = row.deadline.strftime('%d')
            if x[0] == '0':
                x = x[1]
            # print(row.deadline.strftime('%-d %b'))
            print( f"{x}{row.deadline.strftime(' %b')}")
    def add_task(self):
        self.inp_task = input("Enter task\n")
        self.inp_deadline = input("Enter the deadline\n")
        self.new_row = todo_db.Table(
                        task = self.inp_task,
                        deadline=todo_db.datetime.strptime(self.inp_deadline, '%Y-%m-%d').date()
                        )
        todo_db.session.add(self.new_row)
        todo_db.session.commit()
        print("The task has been added!")
    def missed_task(self):
        # Print all tasks ordered by deadline date
        self.missed = todo_db.session.query(todo_db.Table).\
                        filter(todo_db.Table.deadline < datetime.today()).all()
        if len(self.missed) == 0:
            print("Nothing is missed!")
            return
        for l in self.missed:
            print(l,end=". ")
            print(l.deadline.strftime('%d %b'))
        return
    def delete_task(self):
        print("Choose the number of task you want to delete:")
        self.rows = todo_db.session.query(todo_db.Table).order_by(todo_db.Table.deadline).all()
        for row in self.rows:
            print(row, end="")
            print(". ", end="")
            print(row.deadline.strftime("%d %b"))
        n = int(input())  # Number of tasks you want to delete
        # Delete all rows where deadline < datetime.today()
        self.del_ = todo_db.session.query(todo_db.Table).\
                    filter(todo_db.Table.deadline <= datetime.today()).all()
        for i in range(len(self.del_)):
            self.specific_row = self.del_[i]
            todo_db.session.delete(self.specific_row)
            todo_db.session.commit()
        print("The task has been deleted!")
    def print_tasks(self):
        for loop in self.todo_list:
            print(loop)
todos = todo()
# Create the table task with the DDL in todo_db.py
todo_db.Base.metadata.create_all(todo_db.engine)
while(True):
    x = """
1) Today's tasks
2) Week's Tasks
3) All Tasks
4) Missed Tasks
5) Add Task
6) Delete Task
0) Exit
        """
    print(x)
    # Accept the task you want to perform
    choice = int(input())
    if choice == 1:
        todos.today_tasks()
    elif choice == 5:
        todos.add_task()
    elif choice == 2:
        todos.week_tasks()
    elif choice == 3:
        todos.all_tasks()
    elif choice == 4:
        todos.missed_task()
    elif choice == 6:
        todos.delete_task()
    elif choice == 0:
        print("\nBye!")
        exit()
    else:
        print("Please select a valid option")
# todos.tasks()
# todos.print_tasks()