import tkinter as tk
from tkinter import filedialog, messagebox
import dropbox, os

TOKEN = "sl.u.AGDmuKxwjxkai-XCHXPfjh2YgF3CnHJRiQYa3C_uF7jdQfaHL7SANVlVyl-xQl6IoINxyFJb0sCkFnnWU-27PwcMLNaKIdm0-gBpgYEKQ7-oLzveBCnnFvx0dlZUZdtNxa-pKhZ2c9Na1w8cY-SIFkxjJRQwEs_M_Dem6fXgP2OsU5RmbP_e8JhcoAq-Adjpe-s2OpBguPnBVC3Sp0f5o6LL31FXC1sqyubBj78jQLCC71ySDKafz-sIQru5IQ_15s22VMYX_KEQvntPuSmzDmaIx4tNVSKr860YLdWGZE-IrXU9v2mMinmv9MONXTCAe7CYDBJ_FJ6mYteUldoy3BiZG2dA9qKntS5_E_OxTeavw8ED8zvOfp29JtAwhyAecK68Q4NXUJj9fe5O382XaUTqyhd1o5d-CCPBD9AmpnnjaHpGMsUB-oYRM5-nXMDpgGulLvGbSuI02EnYjznqFYFvyk_oRRULkjzFRjKVJBjU8A54D1q-2N_oYEynzHOg7HUQ9Bx3hPhJ7Gs6CDPYXM5Zf88qR1uMi24V1Q9wa5Jp9ytxwvhDzMVDqAJE_3X8fZHKJ18F8gq1ozVjbCWQpDQJQhif5SE5pzvTUPgoINoOsDMAVPfArXfm_kJ719PahHNWFpXZeyUdIO68T_Zk7dX2nFRSt9AXZaaBP0ApFdEHmUIJWe8IREyTJFZPunkq_kMZHUmqfV-e_VdtR6Tvc4T-cTR14N9_u7vhNhBjoXJ-W6B7CsLpYxVHLfsStogcr4NdKWjXD4UsyTLoB2IF-9sROzKGGUzMyUNDwrpgo3enJ42HFt4cO9y8lFHPOCVGAJZZd5Ndp8_iU4MrsfWPuponqGwUA3Iz661g3IHG27gSZ-panC0G9bw94gWDg90fqlGjJLf0p8mFm81HIDMW93GBVCEeVMXi47SZyjt33lGP_1q8cTdcgpi4unjmA_PBlPJoOdG4hLhFSa7tXL6kz8CTGQvHvkdP-p4sYB-uD5csG00s0K681X0vo5UysOYdT6Ot5A3qXtf9tdlJ9OJpdUpIzNCCS4TmIW0dSBn1ldk4a5kL423_ut7-Gq6qcQmKX0mBf53mtj4ZCQBgpMuJfmdlGbxBsKWivfLfVKEYW86n1_OSbRGhWb3uN3l0iPuIUg3mX_k05KkQezjwIqL30vr8CnFoq6034COcJdKDFFJe0H8mk4wjCxWPDEdy_7OaG_2w0gNG9qRfUrUgHImIC3FFS-2ppNUoPPkfjyQA4CujKvBEkC6K34WTndiL6_tyyOZr-Jva9P4BDbkd-TYBCYLmRs88-EWI1-4z3JVFOghtUXLMDD_pg6wrpttAb9ohKczsRGiGoHjutSzEbZTaHGkLjt3P1DtjjyC7LkjJgOg9EgS0AIBRC5r5jbdV7jEda5U7LwMbgzgGKiRu3iaompwftR4g5AIO9NFAF7TG7xwtDuLCltHP2Kc4HPfkhZu4KrQ"
dbx = dropbox.Dropbox(TOKEN)
ACCOUNT_NAME = dbx.users_get_current_account().name.display_name

root = tk.Tk()
root.title("Dropbox Manager")
root.geometry("640x420")

status_var = tk.StringVar()
listbox = tk.Listbox(root)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Scrollbar(root, command=listbox.yview).pack(side=tk.LEFT, fill=tk.Y)
listbox.config(yscrollcommand=lambda *args: None)

def human(n):  # bytes -> human readable
    for u in ['B','KB','MB','GB','TB']: 
        if n<1024: return f"{n:.1f}{u}"; n/=1024
    return f"{n:.1f}PB"

def list_files():
    listbox.delete(0,tk.END)
    files=dbx.files_list_folder("").entries
    for f in files:
        if isinstance(f, dropbox.files.FileMetadata):
            listbox.insert(tk.END,f"{f.name} ({human(f.size)})")
    status_var.set(f"{ACCOUNT_NAME} - {len(files)} files")

def upload():
    path=filedialog.askopenfilename()
    if path: dbx.files_upload(open(path,"rb").read(), f"/{os.path.basename(path)}", mode=dropbox.files.WriteMode.overwrite); list_files()

def delete():
    sel=listbox.curselection()
    if sel:
        name=listbox.get(sel[0]).split(" ")[0]
        if messagebox.askyesno("Delete?",name): dbx.files_delete_v2(f"/{name}"); list_files()

def download():
    sel=listbox.curselection()
    if sel:
        name=listbox.get(sel[0]).split(" ")[0]
        folder=filedialog.askdirectory()
        if folder:
            md,res=dbx.files_download(f"/{name}")
            open(os.path.join(folder,name),"wb").write(res.content)
            messagebox.showinfo("Downloaded",f"{name} saved to {folder}")

tk.Frame(root).pack(side=tk.TOP)
tk.Button(root,text="Upload",command=upload).pack(side=tk.LEFT)
tk.Button(root,text="Download",command=download).pack(side=tk.LEFT)
tk.Button(root,text="Delete",command=delete).pack(side=tk.LEFT)
tk.Button(root,text="Refresh",command=list_files).pack(side=tk.LEFT)
tk.Label(root,textvariable=status_var).pack(side=tk.BOTTOM,fill=tk.X)
list_files()
root.mainloop()
