# usuário que interage
class User:
    
    def __init__(self, user_id: int, name: str = "user"):
        self.id = user_id
        self.name = name

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}')"
