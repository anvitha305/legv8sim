import legv8sim as lsim
import yaml

registers = dict(zip(["x"+str(i) for i in range(0,32)],[0]*32))
flags={"n":0, "c":0, "z":0, "v":0}
mem = dict()
pc = (None, 0)
ret_instr = (None,0)
def parse(fname):
    global pc
    program = []
    file = open(fname)
    branchline = list(map(lambda x: x[:x.find("//")]+" " if x.find("//")!=-1 else x, file.read().split("\n")))
    file.close()
    if len(branchline) == 0:
        return
    branches = dict()
    branchlocs = [i for i,e in enumerate(branchline) if ':' in e]
    ir = dict()
    for i in range(len(branchlocs)):
        try:
            branches[branchline[branchlocs[i]].replace(":", "")] = branchline[branchlocs[i]+2:branchlocs[i+1]]
        except IndexError:
            branches[branchline[branchlocs[i]].replace(":", "")] = branchline[branchlocs[i]:]
    if len(branchlocs)>0:
        branches[branchline[branchlocs[-1]].replace(":", "")] = branchline[branchlocs[-1]+1:]
    if len(branchlocs) ==0:
        branches[""]=branchline
        pc = ("",0)
    else:
        pc = (list(branches.keys())[0], 0)
    for branch in branches:
        ir[branch] = []
        for line in branches[branch]:
            funcs = [lsim.i_inst, lsim.r_inst, lsim.d_inst, lsim.b_inst, lsim.cb_inst]
            res=""
            for func in funcs:
                try:
                    res = func(line)
                    break
                except:
                    pass
            if res=="" and line!="":
                raise Exception("issue with parsing instruction: " + line)
            else:
                ir[branch].append(res)
    return ir
def interpretOne(instruction, regs="", flags=""):
    parsed =  yaml.safe_load(instruction[11:].lower())
    global pc
    global ret_instr
    global mem
    next_instr= (pc[0], pc[1]+1)
    if parsed['typ'] == 'd':
        if parsed['instr'] == "ldur":
            try:
                rt, rn = parsed['regs']
                addr = parsed['addr']
                regs[rt] = mem[regs[rn] + addr]
            except Exception as e:
                raise Exception("error parsing load instruction - invalid or incorrect number of operands.")
        if parsed['instr'] == "stur":
            try:
                rt, rn = parsed['regs']
                addr = parsed['addr']
                mem[regs[rn] + addr] = regs[rt]
            except Exception as e:
                raise Exception("error parsing load instruction - invalid or incorrect number of operands.")
        if parsed['instr'] == "lda":
            try:
                rt, rn = parsed['regs']
                addr = parsed['addr']
                mem[regs[rn]+ addr] = regs[rt]
            except Exception as e:
                raise Exception("error parsing load instruction - invalid or incorrect number of operands.") 
        if parsed['instr']=="mov":
            try:
                rt, rn = parsed['regs']
                regs[rt] = regs[rn]
            except Exception as e:
                raise Exception("error parsing load instruction - invalid or incorrect number of operands.") 
    elif parsed['typ'] == 'c':
        if parsed['instr'] == "b.gt":
            if (flags['z']==0) and (flags['n']==flags['v']):
                try:
                    next_instr = (parsed["bname"], 0)
                except Exception as e:
                    raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "b.ge":
            if flags['n'] == flags['v']:
                try:
                    next_instr = (parsed["bname"], 0)
                except Exception as e:
                    raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "b.le":
            if (flags['z']==1) and (flags['n']!=flags['v']):
                try:
                    next_instr = (parsed["bname"], 0)
                except Exception as e:
                    raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "b.lt":
            if flags['n'] != flags['v']:
                try:
                    next_instr = (parsed["bname"], 0)
                except Exception as e:
                    raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "b.eq":
            if flags['z'] == 1:
                try:
                    next_instr = (parsed["bname"], 0)
                except Exception as e:
                    raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "b.ne":
            if flags['z'] == 0:
                try:
                    next_instr = (parsed["bname"], 0)
                except Exception as e:
                    raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "cbz":
            try:
                if len(parsed['regs'])!=1:
                    raise Exception("incorrect args...")
                res = parsed["regs"][0]
                if res == 0:
                    next_instr = (parsed["bname"], 0)
            except Exception as e:
                 raise Exception("cannot adjust the branch address...")
        if parsed['instr'] == "cbnz":
            try:
                if len(parsed['regs'])!=1:
                    raise Exception("incorrect args...")
                res = parsed["regs"][0]
                if res != 0:
                    next_instr = (parsed["bname"], 0)
            except Exception as e:
                 raise Exception("cannot adjust the branch address...")
    elif parsed['typ']=='b':
        if parsed["instr"] == "b":
            try:
                next_instr = (parsed["bname"], 0)
            except Exception as e:
                raise Exception("cannot adjust the branch address...")
        if parsed["instr"] == "bl":
            try:
                next_instr = (parsed["bname"], 0)
                ret_instr = pc
            except Exception as e:
                raise Exception("cannot adjust the branch address...")
    elif parsed['typ'] == 'r':
        if parsed["instr"] == "fadd":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]+regs[s2]
                regs[dest] = float(regs[dest])
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed["instr"] == "fsubd":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]-regs[s2]
                regs[dest] = float(regs[dest])
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed["instr"] == "fdivd":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]/regs[s2]
                if type(regs[dest])!=float:
                    raise Exception("non float result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed["instr"] == "fmuld":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]*regs[s2]
                regs[dest] = float(regs[dest])
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr']=="umulh":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]*regs[s2]
                if type(regs[dest])!=int or regs[s1]<0 or regs[s2]<0:
                    raise Exception("not unsigned integer result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr']=="smulh":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]*regs[s2]
                if type(regs[dest])!=int:
                    raise Exception("not integer result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed["instr"] == "fcmpd":
            try:
                dest, s1, s2 = parsed['regs']
                res = regs[s1]-regs[s2]
                regs[dest] = res
                if type(regs[dest])!=float:
                    raise Exception("non float result...")
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr']=="udiv":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]//regs[s2]
                if type(regs[dest])!=int or regs[s1]<0 or regs[s2]<0:
                    raise Exception("not unsigned integer result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr']=="mul":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]*regs[s2]
                if type(regs[dest])!=int:
                    raise Exception("not integer result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr']=="sdiv":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]//regs[s2]
                if type(regs[dest])!=int:
                    raise Exception("not integer result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "add":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]+regs[s2]
                if type(regs[dest])!=int:
                    raise Exception("not integer result...")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "adds":
            try:
                dest, s1, s2 = parsed['regs']
                sum = regs[s1] +regs[s2]
                flags['z'] = 1 if sum==0 else 0
                flags['n'] = 1 if sum < 0 else 0
                flags['v'] = 1 if(abs(sum) > (2 ** 31 - 1)) or (abs(sum) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "and":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]&regs[s2]
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "ands":
            try:
                dest, s1, s2 = parsed['regs']
                res = regs[s1] &regs[s2]
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed["instr"] == "br":
            try:
                if len(parsed['regs'])!=1:
                    raise Exception("bad!!!")
                reg = parsed['regs'][0]
                if reg == "x30":
                    pc= ret_instr
                else:
                    raise Exception("make sure you br with the LR/PC!")
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" " + str(e))
        if parsed["instr"]=="cmp":
            try:
                rn, rm = parsed["regs"]
                res = rn-rm
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "eor":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]^regs[s2]
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "lsl":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]<<regs[s2]
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "lsr":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]>>regs[s2]
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "orr":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]|regs[s2]
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "sub":
            try:
                dest, s1, s2 = parsed['regs']
                regs[dest] = regs[s1]-regs[s2]
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "subs":
            try:
                dest, s1, s2 = parsed['regs']
                sum = regs[s1] -regs[s2]
                flags['z'] = 1 if sum==0 else 0
                flags['n'] = 1 if sum < 0 else 0
                flags['v'] = 1 if(abs(sum) > (2 ** 31 - 1)) or (abs(sum) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
    elif parsed['typ']=='i':
        if parsed['instr'] == "addi":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]+parsed['imm']
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "addis":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]+parsed['imm']
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed["instr"]=="cmpi":
            try:
                if len(parsed['regs'])!=1:
                    raise Exception("bad!!!")
                rn = parsed["regs"][0]
                res = rn-parsed["imm"]
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "andis":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]&parsed['imm']
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "andi":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]&parsed['imm']
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "eori":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]^parsed['imm']
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "orri":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]|parsed['imm']
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "subi":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]-parsed['imm']
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
        if parsed['instr'] == "subis":
            try:
                dest, s1 = parsed['regs']
                regs[dest] = regs[s1]-parsed['imm']
                flags['z'] = 1 if res==0 else 0
                flags['n'] = 1 if res < 0 else 0
                flags['v'] = 1 if(abs(res) > (2 ** 31 - 1)) or (abs(res) > (1 << 31) - 1) else 0
                flags['c'] = 0
            except Exception as e:
                print("Error interpreting instruction "+instruction[12:-1]+" - invalid number/type of operands")
    else:
        raise Exception("Invalid instruction " + str(parsed))
    if regs["x31"]!=0:
        regs["x31"] = 0
        raise Exception("Tried setting zero register to a value.")
    if ret_instr != pc:
        ret_instr = (None, 0)
    pc = next_instr
    return regs, flags

#def run():
 #   parsed = parse()
  #  while True:
   #     try:
    #        print(interpretOne(parsed[pc[0]][pc[1]], registers, flags))
     #   except IndexError:
      #      break