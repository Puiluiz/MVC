import random

class Cow:
    def __init__(self, id):
        self.id = id
        # สุ่มจำนวนเต้านม โดยมีโอกาส 5% ที่จะมีจำนวนเต้าไม่เท่ากับ 4
        self.udders = random.randint(3, 5) if random.random() < 0.05 else 4
        # สุ่มเพศของวัว โดยมีโอกาส 5% ที่จะเป็นวัวตัวผู้
        self.is_male = random.random() < 0.05
        # สุ่มเลขเครื่องรีดนมที่วัวต้องการ
        self.target_machine = random.randint(1, 10)
        self.current_machine = None
        self.milk_produced = 0
        self.is_irritated = False

class MilkingMachine:
    def __init__(self, id):
        self.id = id
        # สร้างหัวรีดนม 4 หัวสำหรับแต่ละเครื่อง
        self.heads = [Head() for _ in range(4)]
        self.cow = None

class Head:
    def __init__(self):
        # สถานะเริ่มต้นของหัวรีดนมคือ "idle" (ว่าง)
        self.status = "idle"  # สถานะอื่นๆ: cleaning (กำลังทำความสะอาด), ready (พร้อมรีดนม), milking (กำลังรีดนม)

class CowStrikeModel:
    def __init__(self):
        # สร้างวัว 100 ตัวเริ่มต้น
        self.cows = [Cow(i) for i in range(100)]
        # สร้างเครื่องรีดนม 10 เครื่อง
        self.machines = [MilkingMachine(i) for i in range(1, 11)]
        self.total_milk = 0
        self.interruptions = 0
        self.milked_cows = 0
        self.removed_cows = 0

    def generate_new_cow(self):
        # สร้างวัวตัวใหม่และเพิ่มเข้าไปในรายการวัว
        new_cow = Cow(len(self.cows) + 1)
        self.cows.append(new_cow)
        return new_cow

    def process_step(self):
        for machine in self.machines:
            if machine.cow:
                self._process_machine(machine)
            else:
                self._assign_new_cow(machine)

    def _process_machine(self, machine):
        cow = machine.cow
        all_ready = all(head.status == "ready" for head in machine.heads)
        all_milking = all(head.status == "milking" for head in machine.heads)

        if all_milking:
            self._milk_cow(cow, machine)
        elif all_ready:
            # ถ้าหัวรีดนมทั้งหมดพร้อม ให้เริ่มรีดนม
            for head in machine.heads:
                head.status = "milking"
        else:
            # ปรับสถานะของหัวรีดนมตามลำดับ
            for head in machine.heads:
                if head.status == "idle":
                    head.status = "cleaning"
                elif head.status == "cleaning":
                    head.status = "ready"

    def _milk_cow(self, cow, machine):
        # คำนวณปริมาณน้ำนมที่รีดได้ (น้อยลงถ้าวัวหงุดหงิด)
        milk_amount = 0.5 if cow.is_irritated else 1
        self.total_milk += milk_amount
        cow.milk_produced += milk_amount
        self.milked_cows += 1
        # นำวัวออกจากเครื่องรีดนมและรีเซ็ตสถานะหัวรีดนม
        machine.cow = None
        for head in machine.heads:
            head.status = "idle"

    def _assign_new_cow(self, machine):
        for cow in self.cows:
            if cow.current_machine is None:
                if cow.target_machine == machine.id:
                    # ถ้าเป็นเครื่องรีดที่วัวต้องการ
                    machine.cow = cow
                    cow.current_machine = machine.id
                    break
                elif all(m.cow for m in self.machines):
                    # ถ้าทุกเครื่องไม่ว่าง ให้วัวเข้าเครื่องนี้แทนและทำให้วัวหงุดหงิด
                    machine.cow = cow
                    cow.current_machine = machine.id
                    cow.is_irritated = True
                    break

    def check_problems(self):
        problems = []
        irritated_cows = 0

        for machine in self.machines:
            if machine.cow:
                if machine.cow.is_male:
                    problems.append(f"วัวตัวผู้อยู่ในเครื่องรีดนมที่ {machine.id}")
                if any(head.status != "idle" and i >= machine.cow.udders for i, head in enumerate(machine.heads)):
                    problems.append(f"พยายามรีดนมจากเต้าที่ไม่มีอยู่จริงในเครื่องรีดนมที่ {machine.id}")
                if machine.cow.is_irritated:
                    irritated_cows += 1

        if irritated_cows >= 8:
            problems.append("มีวัวที่หงุดหงิด 8 ตัวหรือมากกว่า")

        return problems

    def reset_system(self):
        # ระบุวัวที่มีปัญหา (วัวตัวผู้หรือวัวที่มีจำนวนเต้าไม่เท่ากับ 4)
        problematic_cows = [machine.cow for machine in self.machines if machine.cow and (machine.cow.is_male or machine.cow.udders != 4)]
        self.removed_cows += len(problematic_cows)
        
        # นำวัวออกจากเครื่องรีดนมและรีเซ็ตสถานะของเครื่อง
        for machine in self.machines:
            if machine.cow:
                self.cows.remove(machine.cow)
                machine.cow = None
            for head in machine.heads:
                head.status = "idle"

        # นำวัวที่มีปัญหาออกจากระบบ
        self.cows = [cow for cow in self.cows if cow not in problematic_cows]
        # เรียงลำดับวัวใหม่ตาม ID
        self.cows.sort(key=lambda c: c.id)