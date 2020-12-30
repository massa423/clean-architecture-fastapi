from datetime import datetime

from app.interfaces.gateways.db import Base, engine, session
from app.interfaces.gateways.schema import User

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    now = datetime.now()

    user = User(
        name="squid",
        password="password",
        email="squid@example.com",
        created_at=now,
        updated_at=now,
    )
    session.add(user)

    now = datetime.now()

    user = User(
        name="octopus",
        password="password",
        email="octopus@example.com",
        created_at=now,
        updated_at=now,
    )
    session.add(user)

    session.commit()
    session.close()
