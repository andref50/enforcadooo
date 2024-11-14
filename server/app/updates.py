from app import app, db, data
from app.models import Palavra, CurrentDay, UsedCount
import sqlalchemy as sa

from app.encryption import encrypt

def update_word():
    with app.app_context():
        current_day = db.session.scalar(sa.select(CurrentDay))
        current_day.curDay += 1
        
        ativa = db.session.scalar(sa.select(Palavra).where(Palavra.ativa == True))
        ativa.ativa = False

        usedCount = db.session.scalar(sa.select(UsedCount))
        palavra = db.session.scalar(sa.select(Palavra).where(Palavra.used == usedCount.usedCount).order_by(sa.func.random()))

        if palavra is None:
            usedCount.usedCount += 1
            palavra = db.session.scalar(sa.select(Palavra).where(Palavra.used == usedCount.usedCount).order_by(sa.func.random()))

        palavra.ativa = True
        palavra.used += 1

        db.session.commit()

        data.palavra = palavra.palavra
        data.palavra_encrypt = encrypt(palavra.palavra).decode('utf-8', 'ignore')
        data.dica    = palavra.dica
        data.curDay  = current_day.curDay

        print(data.to_dict())


def refresh_word():
    with app.app_context():
        palavra = db.session.scalar(sa.select(Palavra).where(Palavra.ativa == True))
        current_day = db.session.scalar(sa.select(CurrentDay))

        data.palavra = palavra.palavra
        data.palavra_encrypt = encrypt(palavra.palavra).decode('utf-8', 'ignore')
        data.dica    = palavra.dica
        data.curDay  = current_day.curDay

        print(data.to_dict())

def update_placar(req):
    with app.app_context():
        palavra = db.session.scalar(sa.select(Palavra).where(Palavra.ativa == True))
        if(req['status'] == 'winner'):
            palavra.acertos += 1
        else:
            palavra.erros += 1

        db.session.commit()