
import ast
import re
import tkinter as tk
from tkinter import ttk
MON_CNT = 2998
armor_file_path = "Armors.txt"
enemy_file_path = "Enemies.txt"
enemies_rv_path = "Enemies.rvdata2"
item_file_path = "Items.txt"
weapon_file_path = "Weapons.txt"
#slayer_file_path = "Scripts\\ベース\\145 - Module.rb"
lib_enemy_path = "Scripts\\201 - Library(Enemy).rb"

class entry():
    def __init__(self, eid):
        self.eid = eid
        self.name = "MONSTER_NAME"
        self.locations = ["LOCATION"]
        self.drops = []
        self.steal = []
        self.steal_m = []
        self.steal_f = []
        self.steal_p =  False
        self.jexp = -1
        self.slayer = []
        self.recruitable = False
    
    def __str__(self):
        return f"Id: {self.eid}\n"
        f"Name: {self.name}\n"
        f"Locations: {self.locations}\n"
        f"Drops: {self.drops}\n"
        f"Stealable items: {self.steal}\n"
        f"Stealable material: {self.steal_m}\n"
        f"Stealable food: {self.steal_f}\n"
        f"Stealable panties: {self.steal_p}\n"
        f"Job XP: {self.jexp}\n"
        f"Slayer: {self.slayer}\n"
        f"Recruitable: {self.recruitable}\n"
    
    #def __repr__(self):
    #    return self.__str__()

def parse_lib_enemy(path, mdict):
    try:
        f = open(path, encoding = "utf-8")
    except:
        return
    #big_dict = dict()
    current_dict_name = ""
    key = None
    value = None
    image_pattern = r'\[".+?", ".+?",\d+,-?\d+,-?\d+(?:,\d*\.?\d*)?\]'
    location_pattern = r"\[:[^,\[\]]+(?:\s+[^,\[\]]+)*(?:,\s*:[^,\[\]]+(?:\s+[^,\[\]]+)*)*\]"
    for line in f:
        line = line.strip()
        line = line.replace("\xa0", " ")
        if not line or line.startswith('#'):
            continue
        if '=' in line and '{' in line:
            current_dict_name = line.split()[0]
            #big_dict[current_dict_name] = dict()
            continue
        elif "=>" in line:
            key, value = line.split(" => ")
            #print(f"Line: {line}")
            #print(f"Key: {key}")
            #print(f"Value: {value}")
        if line.endswith('],'):
            if matches := re.findall(location_pattern, value):
                value = [s.replace(', ', '').replace('"', '') for s in matches[0][1:-1].split(":") if s]
                #print(int(key), matches)
                #big_dict[current_dict_name][int(key)] = value
                mdict[int(key)].locations = value
            #elif re.findall(image_pattern, value):
            #    big_dict[current_dict_name][int(key)] = ast.literal_eval(value[:-1])
            #else:
            #    value += "]"
            #    #print(f"Failed to parse value: {value}")
            #    big_dict[current_dict_name][int(key)] = ast.literal_eval(value)
            key = None
        #elif not line.endswith('[') and value:
        #    value += line
    #return big_dict    

def parse_enemies(path):
    try:
        f = open(path, encoding = "utf-8")
    except:
        return
    mdict = dict()
    eid = 0
    name = ""
    for line in f:
        if line.startswith("Enemy "):
            line = line[6:]
            if " " in line:
                line = line[:line.index(" ")]
            eid = int(line)
            mdict[eid] = entry(eid = eid)
        elif line.startswith("Name = "):
            if name := line.strip()[8:-1]:
                mdict[eid].name = name
        elif line.startswith("Note = "):
            if note := line.strip()[8:-1]:
                mdict[eid].note = note
                parse_note(note, mdict[eid])
    mdict = {eid:mdict[eid] for eid in mdict if mdict[eid].name != "MONSTER_NAME"}
    return mdict

def parse_note(note, entry):
    global sdict
    pat_jexp = r"<職業Exp (\d+)>"
    if match := re.search(pat_jexp, note):
        entry.jexp = int(match.group(1))
    pat_steal = r"<スティールリスト (.+?)>"
    matches = re.findall(pat_steal, note)
    for match in matches:
        mlist = match.split(",")
        steal_type = int(mlist[0])
        item_type = mlist[1]
        item_id = int(mlist[2])
        if item_type == "A":
            item_name = adict[item_id]
        elif item_type == "W":
            item_name = wdict[item_id]
        else: ## "I"
            item_name = idict[item_id]
        if steal_type == 1:
            entry.steal.append(item_name)
        elif steal_type == 2:
            entry.steal_f.append(item_name)
        elif steal_type == 3:
            entry.steal_m.append(item_name)
        elif steal_type == 4:
            entry.steal_p = True
    pat_slayer = r"<特殊カテゴリー (.+?)>"
    if match := re.search(pat_slayer, note):
        entry.slayer = [sdict[int(x)] for x in match.group(1).split(",")]
    pat_nakama = r"<仲間ID:(\d+)>"
    if match := re.search(pat_nakama, note):
        entry.recruitable = True
    pat_name = r"<図鑑名称:(.+?)>"
    if match := re.search(pat_name, note):
        entry.name = match.group(1)
    
def parse_item_file(path, typestr):
    try:
        f = open(path, encoding = "utf-8")
    except:
        return
    eid = 0
    out = dict()
    for line in f:
        if line.startswith(typestr + " "):
            line = line[len(typestr) + 1:]
            if " " in line:
                line = line[:line.index(" ")]
            eid = int(line)
        elif line.startswith("Name = "):
            #print(typestr, eid, line.strip())
            if name := line.strip()[8:-1]:
                out[eid] = name
            else:
                out[eid] = f"UNDEFINED {typestr}"
    return out

def drop_item_id(segm, pos):
    if (len(segm) == 4 and pos < 10) or len(segm) == 3:
        iid = segm[2] - 5
    elif (len(segm) == 5 and pos < 10) or len(segm) == 4:
        iid = segm[3]
    elif (len(segm) == 6 and pos < 10) or len(segm) == 5:
        iid = segm[3] + segm[4] * 256
    else:
        print(f"\ninvalid id block {pos} {[hex(x) for x in segm]} in:")
        
        iid = 0
    return iid

def format_item_name(ituple):
    global idict
    global wdict
    global adict
    if ituple[1] == 'n':
        return "Nothing"
    elif ituple[1] == 'u':
        return "Undefined"
    elif ituple[1] == 'i':
        target = idict
    elif ituple[1] == 'w':
        target = wdict
    elif ituple[1] == 'a':
        target = adict
    try:
        out = f"{target[ituple[2]]} (1/{ituple[0]})"
        return out
    except:
        print(ituple)

def parse_drops_file(path, mdict):
    try:
        f = open(path, 'rb')
    except Exception as e:
        print(e)
        return
    out = []
    block_start_index = 0
    in_block = False
    mid = 1
    arr = []
    
    for line in f:
        if in_block:
            arr += list(line)
            dlist = []
            raw_semis = [i for i, x in enumerate(arr) if x == ord(';')]
            #print(raw_semis)
            last_name = "slime"
            for i in raw_semis:
                ## start of next enemy entry
                if i < len(arr) - 2 and arr[i + 1] == 0x06 and arr[i + 2] == ord('I') and arr[i + 3] == ord('"'):
                    in_block = False
                    arr = arr[:i]
                    if mid == 1:
                        ## replace tag identifiers in first entry
                        new_arr = []
                        ignore = 0
                        word = ""
                        for x in arr:
                            if ignore == -1:
                                ignore = int(x) - 5
                            elif ignore > 0:
                                ignore -= 1
                                word += chr(x)
                                if word == "@denominator":
                                    new_arr.append(0x1f)
                                elif word == "@kind":
                                    new_arr.append(0x20)
                                #print(word)
                            elif x == ord(':'):
                                ignore = -1
                                new_arr.append(ord(';'))
                            else:
                                word = ""
                                new_arr.append(x)
                        arr = new_arr
                    ## split block using semicolons
                    semis = [-1] + [i for i, x in enumerate(arr) if x == ord(';')]
                    split = [arr[semis[i]+1:semis[i+1]] for i in range(len(semis) - 1)] + [arr[semis[-1]:]]
                    #print(split)
                    drops_start = 0
                    for j in range(len(split)):
                        #print([hex(i) if i is int else i for i in x])
                        #if (split[j].count(ord('i')) > 5 and split[j + 3][0] == 0x1f):
                        if split[j] and split[j][0] == 0x1f:
                            drops_start = j
                            break
                    for j in range(drops_start, drops_start + 14):
                        segm = split[j]
                        if segm[0] == 0x1f:
                            if len(segm) == 3:
                                denom = segm[2] - 5
                            else:
                                denom = segm[3]
                        elif segm[0] == 0x20:
                            itype = 'i' if segm[2] == 0x06 else 'w' if segm[2] == 0x07 else 'a' if segm[2] == 0x08 else 'n' if segm[2] == 0x00 else 'u'
                        elif segm[0] == 0x1a:
                            if len(segm) < 3 or len(segm) == 3 and segm[2] == 0x02:
                                segm = segm + [ord(';')] + split[j + 1]
                            iid = drop_item_id(segm, j - drops_start)
                            dropstr = format_item_name((denom, itype, iid))
                            if dropstr is None:
                                print(mid)
                            dlist.append(dropstr)
                    out.append(dlist)
                    if mid in mdict:
                        mdict[mid].drops = dlist
                        lastmid = mid
                    if mid <= MON_CNT:
                        #mid = list(mdict.keys())[list(mdict.keys()).index(mid) + 1]
                        mid += 1
                    else:
                        break
                    drops_start = 0
                    line_semis = [i for i, x in enumerate(line) if x == ord(';')]
        else:
            in_block = True
            block_start_index = 0
            arr = list(line)
    return out

def parse_slayers(path):
    try:
        f = open(path, encoding = "utf-8")
    except Exception as e:
        print(e)
        return
    sdict = dict()
    parsing = False
    pat = r"(\d\d) => \"(.*?)\""
    for line in f:
        line = line.strip()
        if "EX_CATEGORY" in line:
            parsing = True
        if parsing:
            if match := re.search(pat, line):
                sdict[match.group(1)] = match.group(2)
            if line == "}":
                return sdict

#pprint.pp(mdict)
idict = parse_item_file(item_file_path, "Item")
wdict = parse_item_file(weapon_file_path, "Weapon")
adict = parse_item_file(armor_file_path, "Armor")
#sdict = parse_slayers(slayer_file_path)
sdict = {
    10: "Boss",
    11: "Human",
    12: "Yoma",
    13: "Demihuman",
    14: "Succubus",
    15: "Vampire",
    16: "Mermaid",
    17: "Elf",
    18: "Fairy",
    19: "Slime",
    20: "Beast",
    21: "Kitsune",
    22: "Lamia",
    23: "Scylla",
    24: "Harpy",
    25: "Dragon",
    26: "Land dweller",
    27: "Sea dweller",
    28: "Insect",
    29: "Alraune",
    30: "Zombie",
    31: "Ghost",
    32: "Doll",
    33: "Chimera",
    34: "Angel",
    35: "Apoptosis",
    37: "Giant",
    38: "Roid",
    39: "Nightmare",
    40: "Flying",
    41: "God",
    42: "Monster lord"
}


mdict = parse_enemies(enemy_file_path)
parse_lib_enemy(lib_enemy_path, mdict)
dlist = parse_drops_file(enemies_rv_path, mdict)


'''
recruitable in 195
'''
# GUI Application
class EntryViewer:
    def __init__(self, root, entries):
        self.root = root
        self.entries = entries
        self.index_list = list(entries)
        self.index_index = 0
        self.mindex = self.index_list[0]

        self.root.title("Pocket Monsterpedia")
        self.root.geometry("800x400")

        # Widgets
        self.search_frame = ttk.Frame(root)
        self.search_frame.pack(pady=10)

        self.id_search_label = ttk.Label(self.search_frame, text="Go to ID:")
        self.id_search_label.grid(row=0, column=0, padx=5)

        self.id_search_entry = ttk.Entry(self.search_frame, width=10)
        self.id_search_entry.grid(row=0, column=1, padx=5)

        self.id_search_button = ttk.Button(self.search_frame, text="Go", command=self.search_by_id)
        self.id_search_button.grid(row=0, column=2, padx=5)

        self.name_search_label = ttk.Label(self.search_frame, text="Search by name:")
        self.name_search_label.grid(row=0, column=3, padx=5)

        self.name_search_entry = ttk.Entry(self.search_frame, width=10)
        self.name_search_entry.grid(row=0, column=4, padx=5)

        self.name_search_button = ttk.Button(self.search_frame, text="Search", command=self.search_by_name)
        self.name_search_button.grid(row=0, column=5, padx=5)

        self.item_search_label = ttk.Label(self.search_frame, text="Search by item:")
        self.item_search_label.grid(row=1, column=0, padx=5)

        self.item_search_entry = ttk.Entry(self.search_frame, width=10)
        self.item_search_entry.grid(row=1, column=1, padx=5)

        self.item_search_button = ttk.Button(self.search_frame, text="Go", command=self.search_by_item)
        self.item_search_button.grid(row=1, column=2, padx=5)

        self.loc_search_label = ttk.Label(self.search_frame, text="Search by location:")
        self.loc_search_label.grid(row=1, column=3, padx=5)

        self.loc_search_entry = ttk.Entry(self.search_frame, width=10)
        self.loc_search_entry.grid(row=1, column=4, padx=5)

        self.loc_search_button = ttk.Button(self.search_frame, text="Search", command=self.search_by_location)
        self.loc_search_button.grid(row=1, column=5, padx=5)
        
        self.name_label = ttk.Label(root, text="", font=("Arial", 16))
        self.name_label.pack(pady=10)

        self.details_text = tk.Text(root, wrap=tk.WORD, height=15, width=150)
        self.details_text.pack(pady=10)

        self.nav_frame = ttk.Frame(root)
        self.nav_frame.pack(pady=10)

        self.prev_button = ttk.Button(self.nav_frame, text="Previous", command=self.show_previous)
        self.prev_button.grid(row=0, column=0, padx=10)

        self.next_button = ttk.Button(self.nav_frame, text="Next", command=self.show_next)
        self.next_button.grid(row=0, column=1, padx=10)
        

        # Show the first entry
        self.display_entry()

    def show_text(self, text):
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, text)

    def display_entry(self):
        entry = self.entries[self.mindex]
        self.name_label.config(text=entry.name)

        details = (
            f"ID: {entry.eid}\n"
            f"Locations: {', '.join(entry.locations)}\n"
            f"Drops: {entry.drops if entry.drops else None}\n"
            f"Stealable items: {', '.join(entry.steal) if entry.steal else None}\n"
            f"Stealable Materials: {', '.join(entry.steal_m) if entry.steal_m else None}\n"
            f"Stealable Food: {', '.join(entry.steal_f) if entry.steal_f else None}\n"
            f"Panties: {'Yes' if entry.steal_p else 'No'}\n"
            f"Job XP: {entry.jexp}\n"
            f"Slayers: {entry.slayer}\n"
            #f"Recruitable: {'Yes' if entry.recruitable else 'No'}\n"
        )

        self.show_text(details)

    def show_previous(self):
        self.index_index = self.index_index - 1 if self.index_index > 0 else len(self.entries) - 1
        self.mindex = self.index_list[self.index_index]
        self.display_entry()

    def show_next(self):
        self.index_index = self.index_index + 1 if self.index_index < len(self.entries) - 1 else 0
        self.mindex = self.index_list[self.index_index]
        self.display_entry()
    
    def search_by_id(self):
        try:
            search_id = int(self.id_search_entry.get())
            if search_id in self.index_list:
                self.index_index = self.index_list.index(search_id)
                self.mindex = self.index_list[self.index_index]
                self.display_entry()
            else:
                self.show_error(f"No entry with ID {search_id} found.")
        except ValueError:
            self.show_error("Invalid ID. Please enter a number.")
    
    def search_by_name(self):
        search_str = self.name_search_entry.get().lower()
        found_ids = []
        results = "Found entries:\n"
        for eid, entry in self.entries.items():
            if search_str in entry.name.lower():
                found_ids.append(eid)
                results += f"{eid}: {entry.name}\n"
        self.show_text(f"{results}")
        
    def search_by_item(self):
        search_str = self.item_search_entry.get().lower()
        found_ids = []
        results = "Found entries:\n"
        for eid, entry in self.entries.items():
            if any(search_str in s.lower() for s in entry.steal) or \
                any(search_str in s.lower() for s in entry.steal_m) or \
                any(search_str in s.lower() for s in entry.steal_f) or\
                any(search_str in s.lower() for s in entry.drops):
                found_ids.append(eid)
                results += f"{eid}: {entry.name}\n"
        self.show_text(f"{results}")
    
    def search_by_location(self):
        search_str = self.loc_search_entry.get().lower()
        found_ids = []
        results = "Found entries:\n"
        for eid, entry in self.entries.items():
            if any(search_str in s.lower() for s in entry.locations):
                found_ids.append(eid)
                results += f"{eid}: {entry.name}\n"
        self.show_text(f"{results}")

    def show_error(self, message):
        self.show_text(f"Error: {message}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = EntryViewer(root, mdict)
    root.mainloop()
