class CowStrikeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            input("กดปุ่ม Enter เพื่อดำเนินการขั้นต่อไป...")
            self.model.process_step()
            problems = self.model.check_problems()
            
            if problems:
                self.model.interruptions += 1
                self.view.display_problems(problems)
                self.model.reset_system()
                print("ระบบถูกรีเซ็ตเนื่องจากพบปัญหา")
            
            self.view.display_status(self.model)
            self.view.display_machines(self.model.machines)