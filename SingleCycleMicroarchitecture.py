class FUM_MIPS():
    PC = 0
    RegisterFile = list()
    InstructionMemory = list()
    DataMemory = list()

    # Control Signals
    RegDest = 0
    Jump = 0
    Branch = 0
    MemRead = 0
    MemToReg = 0
    ALUOp = 0
    MemWrite = 0
    ALUSrc = 0
    RegWrite = 0

    def __init__(self, instructions):
        self.InstructionMemory = instructions
        self.RegisterFile = [
            "00000000000000000000000000000000", "00000000000000000000000000000001", "00000000000000000000000000000011",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000", "00000000000000000000000000000000",
            "00000000000000000000000000000000", "00000000000000000000000000000000"
            ]
    
    def run(self):
        while (self.PC <= len(self.InstructionMemory)):
            self.execute(self.InstructionMemory[self.PC // 4]) # PC += 4
            PC += 4 # TODO: after jump & branch -> PC + 4 + 4 -> wrong? -> should use PC without +4 in jump & branch?

    def execute(self, instruction):
        # Decode
        rs = instruction[6:11] # 21 - 25 bits
        rt = instruction[11:16] # 16 - 20 bits
        rd = instruction[16:21] # 11 - 15 bits
        imm = instruction[16:] # 0 - 15 bits
        func = instruction[26:] # 0 - 5 bits
        Opcode = instruction[:6] # 26 - 31 bits
        shamt = instruction[22:27] # 6 - 10 bits
        jump_address = instruction[6:] # 0 - 25 bits

        # Fetch
        A = self.RegisterFile[int(rs, 2)]
        B = self.RegisterFile[int(rt, 2)]

        if (Opcode == "000000"):
            self.RType(A, B, rd, shamt, func)
        else:
            if (Opcode == "000010"):
                self.JType(jump_address)
            else:
                self.IType() # TODO: implement
    
    def RType(self, A, B, rd, shamt, func):
        match func:
            case "100000":
                # add
                result = int(A, 2) + int(B, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rd, 2)] = result
                
            case "100010":
                # sub
                result = int(A, 2) - int(B, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rd, 2)] = result
                
            case "100101":
                # or
                result = int(A, 2) | int(B, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rd, 2)] = result

            case "100100":
                # and
                result = int(A, 2) & int(B, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rd, 2)] = result

            case "101010":
                # slt
                result = int(B, 2) << int(shamt, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rd, 2)] = result

    def JType(self, jump_address):
        jump_address = int(jump_address, 2) << 2
        jump_address_bit_string = f"{jump_address:b}".zfill(28)
        PC_bits = f"{self.PC + 4:b}".zfill(32)[0:4] # 28 - 31 bits
        target = PC_bits + jump_address_bit_string

        self.PC = int(target, 2)

    def IType(self, Opcode, A, rt, imm):
        match Opcode:
            case "101011":
                # sw
                effective_address = int(A, 2) + int(imm, 2)
                self.DataMemory[effective_address] = self.RegisterFile[int(rt, 2)]

            case "100011":
                # lw
                effective_address = int(A, 2) + int(imm, 2)
                self.RegisterFile[int(rt, 2)] = self.DataMemory[effective_address]

            case "001000":
                # addi
                result = int(A, 2) + int(imm, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rt, 2)] = result

            case "001010":
                # slti
                if (int(A, 2) < int(imm, 2)):
                    self.RegisterFile[int(rt, 2)] = f"{1:b}".zfill(32)
                else:
                    self.RegisterFile[int(rt, 2)] = f"{0:b}".zfill(32)

            case "001100":
                # andi
                result = int(A, 2) & int(imm, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rt, 2)] = result

            case "001101":
                # ori
                result = int(A, 2) | int(imm, 2)
                result = f"{result:b}".zfill(32) # extend to 32 bits
                self.RegisterFile[int(rt, 2)] = result

            case "000100":
                # beq
                imm = int(imm, 2) << 2
                target = self.PC + 4 + imm
                if (A == self.RegisterFile[int(rt, 2)]):
                    self.PC = target

            case "000101":
                # bne
                imm = int(imm, 2) << 2
                target = self.PC + 4 + imm
                if (A != self.RegisterFile[int(rt, 2)]):
                    self.PC = target


# 000000 00001 00010 00011 00000 100000
microarchitecture = FUM_MIPS([])
microarchitecture.execute("00000000001000100001100000100000")