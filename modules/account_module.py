from uuid import uuid4 as get_uuid


class Account:
    def __init__(
        self,
        username: str,
        password: str,
        profile_picture: str = "",
        description: str = "...",
        id: str = "",
    ) -> None:
        self.id: str = str(get_uuid()) if id == "" else id
        self.username: str = username
        self.password: str = password # keep in mind that the password is hashed before being passed.
        self.profile_picture: str = profile_picture
        self.description: str = description


    def __str__(self) -> str:
        return f"Account({self.get_id()})"
    

    def __repr__(self) -> str:
        return f"Account({self.get_id()})"
    

    def __eq__(self, other_account: object) -> bool:
        if isinstance(other_account, Account):
            return self.get_id() == other_account.get_id()
        return False
    

    def check_password(self, a_password_hash: str) -> bool:
        return self.get_password() == a_password_hash


    def get_username(self) -> str:
        return self.username
    

    def get_password(self) -> str:
        return self.password
    

    def get_description(self) -> str:
        return self.description
    

    def get_profile_picture(self) -> str:
        return self.profile_picture
    

    def get_id(self) -> str:
        return self.id
    

    def get_info(self) -> dict:
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "description": self.get_description(),
            "profile_picture": self.get_profile_picture(),
            "id": self.get_id(),
        }
    


if __name__ == "__main__":
    account: Account = Account("test", "test")
    input_password: str = "test"
    print(account)
    print(account.check_password(input_password))