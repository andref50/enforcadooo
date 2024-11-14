from app import app, db, data
from app.models import Palavra, CurrentDay, UsedCount
import sqlalchemy as sa

def update_word():
    with app.app_context():
        current_day = db.session.scalar(sa.select(CurrentDay))
        current_day.curDay += 1
        
        ativa = db.session.scalar(sa.select(Palavra).where(Palavra.ativa == True))
        ativa.ativa = False

        usedCount = db.session.scalar(sa.select(UsedCount))
        nova_palavra = db.session.scalar(sa.select(Palavra).where(Palavra.used == usedCount.usedCount).order_by(sa.func.random()))

        if nova_palavra is None:
            usedCount.usedCount += 1
            nova_palavra = db.session.scalar(sa.select(Palavra).where(Palavra.used == usedCount.usedCount).order_by(sa.func.random()))

        nova_palavra.ativa = True
        nova_palavra.used += 1

        db.session.commit()

        data.palavra = nova_palavra.palavra
        data.dica    = nova_palavra.dica
        data.curDay  = current_day.curDay

        print(data.to_dict())


def refresh_word():
    with app.app_context():
        palavra = db.session.scalar(sa.select(Palavra).where(Palavra.ativa == True))
        current_day = db.session.scalar(sa.select(CurrentDay))

        data.palavra = palavra.palavra
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