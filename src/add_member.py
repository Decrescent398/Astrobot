def add_member(member: str):
    print(member)
    with open(f"data/members/{member}.txt", 'w', newline='') as df:
        pass