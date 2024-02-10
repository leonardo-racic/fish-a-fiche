class Account:
    def __init__(self, username: str, password: str, id: int) -> None:
        self.username: str = username
        self.password: str = password # keep in mind that the password is hashed before being passed.
        self.id: str = id
        print(f"Initialised account with username {self.get_username()!r}")


    def __str__(self) -> str:
        return f"Account(username={self.get_username()!r}, password={self.get_password()!r})"
    

    def __repr__(self) -> str:
        return f"Account(username={self.get_username()!r}, password={self.get_password()!r})"
    

    def __eq__(self, other_account: object) -> bool:
        if isinstance(other_account, Account):
            return self.get_username() == other_account.get_username()
        return False
    

    def check_password(self, a_password_hash: str) -> bool:
        return self.get_password() == a_password_hash


    def get_username(self) -> str:
        return self.username
    

    def get_password(self) -> str:
        return self.password



if __name__ == "__main__":
    account: Account = Account("test", "test")
    input_password: str = "test"
    print(account)
    print(account.check_password(input_password))