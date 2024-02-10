import hashlib


def get_hash(this_hash: str) -> str:
    return hashlib.sha256(this_hash.encode()).hexdigest()


class Account:
    def __init__(self, username: str, password: str, id: int) -> None:
        self.username: str = username
        self.password: str = password
        self.id: str = id
        print(f"initialized account {self.id} with username")


    def __str__(self) -> str:
        return f"Account(username={self.username!r}, password={self.password!r})"
    

    def __repr__(self) -> str:
        return f"Account(username={self.username!r}, password={self.password!r})"
    

    def __eq__(self, other_account: object) -> bool:
        if isinstance(other_account, Account):
            return self.id == other_account.id and self.password == other_account.password
        return False
    

    def check_password_hash(self, this_hash: str) -> bool:
        password_hash: str = get_hash(self.password)
        return password_hash == this_hash
    

    def get_username(self) -> str:
        return self.username
    

    def get_password_hash(self) -> str:
        return get_hash(self.password)



if __name__ == "__main__":
    account: Account = Account("test", "test")
    input_password: str = get_hash(input("Password: "))
    print(account)
    print(account.check_password_hash(input_password))