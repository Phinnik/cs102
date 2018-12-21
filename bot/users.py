from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import update


Base = declarative_base()
engine = create_engine('sqlite:///users.db')
Session = scoped_session(sessionmaker(bind=engine))

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	telegram_id = Column(Integer)
	group = Column(String)
	notify = Column(Boolean)
	friendly = Column(Boolean)
	last_active = Column(Integer)

	def __repr__(self):
		line = """id:{};\
		telegram_id:{};\
		 group:{};\
		 last_active:{}""".format(self.id,
								  self.telegram_id,
								  self.group,
								  self.last_active).replace('		', ' ')
		return line


Base.metadata.create_all(bind=engine)
Session.configure(bind=engine)
session = Session()


#me = User(telegram_id=1, group='K3142', notify=False, friendly=True, last_active=2)


def get_telegram_user(telegram_id: int, close: bool = True) -> User:
	''' Returns database user by his telegram id or None if there is no such User'''
	user = session.query(User).filter(User.telegram_id==telegram_id).all()
	if close:
		session.close()
	if user == []:
		return None
	else:
		return user[0]

def add_user(user: User) -> None:
	''' Ads user to databaase '''
	session.add(user)
	session.commit()

def update_user(user, group=None, notify=None, friendly=None, last_active=None) -> None:
	''' Updates user parameters in database '''
	if group  is not None:
		user.group = group
	if notify is not None:
		user.notify = notify
	if friendly is not None:
		user.friendly = friendly
	if last_active is not None:
		user.last_active = last_active
	session.commit()
