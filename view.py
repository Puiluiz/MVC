class CowStrikeView:
    def display_status(self, model):
        print(f"ปริมาณน้ำนมที่รีดได้ทั้งหมด: {model.total_milk} ลิตร")
        print(f"จำนวนครั้งที่ระบบถูกแทรกแซง: {model.interruptions}")
        print(f"จำนวนวัวที่ถูกรีดนมแล้ว: {model.milked_cows}")
        print(f"จำนวนวัวที่มีปัญหาและถูกนำออกจากระบบ: {model.removed_cows}")

    def display_machines(self, machines):
        for machine in machines:
            print(f"เครื่องรีดนมที่ {machine.id}:")
            if machine.cow:
                print(f"  วัว: {machine.cow.id} (จำนวนเต้า: {machine.cow.udders}, {'ตัวผู้' if machine.cow.is_male else 'ตัวเมีย'})")
                print(f"  สถานะหัวรีดนม: {', '.join(head.status for head in machine.heads)}")
            else:
                print("  ว่าง")

    def display_problems(self, problems):
        if problems:
            print("พบปัญหา:")
            for problem in problems:
                print(f"- {problem}")
        else:
            print("ไม่พบปัญหา")