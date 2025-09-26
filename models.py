from datetime import datetime, date
from dataclasses import dataclass
from typing import Optional

@dataclass
class Veicolo:
    id: Optional[int]
    nome: str
    tipo: str
    anno: Optional[int] = None
    km_attuali: int = 0
    foto: Optional[bytes] = None
    note: Optional[str] = None
    data_creazione: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        if row is None:
            return None
        return cls(
            id=row[0],
            nome=row[1],
            tipo=row[2],
            anno=row[3],
            km_attuali=row[4] or 0,
            foto=row[5],
            note=row[6],
            data_creazione=datetime.fromisoformat(row[7]) if row[7] else None
        )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'anno': self.anno,
            'km_attuali': self.km_attuali,
            'note': self.note,
            'data_creazione': self.data_creazione.isoformat() if self.data_creazione else None
        }

@dataclass
class Manutenzione:
    id: Optional[int]
    veicolo_id: int
    data_intervento: date
    km_intervento: int
    tipo_manutenzione: str
    descrizione: Optional[str] = None
    costo: Optional[float] = None
    prossima_manutenzione_km: Optional[int] = None
    prossima_manutenzione_data: Optional[date] = None
    data_creazione: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        if row is None:
            return None
        return cls(
            id=row[0],
            veicolo_id=row[1],
            data_intervento=datetime.strptime(row[2], '%Y-%m-%d').date() if row[2] else None,
            km_intervento=row[3],
            tipo_manutenzione=row[4],
            descrizione=row[5],
            costo=row[6],
            prossima_manutenzione_km=row[7],
            prossima_manutenzione_data=datetime.strptime(row[8], '%Y-%m-%d').date() if row[8] else None,
            data_creazione=datetime.fromisoformat(row[9]) if row[9] else None
        )

    def to_dict(self):
        return {
            'id': self.id,
            'veicolo_id': self.veicolo_id,
            'data_intervento': self.data_intervento.isoformat() if self.data_intervento else None,
            'km_intervento': self.km_intervento,
            'tipo_manutenzione': self.tipo_manutenzione,
            'descrizione': self.descrizione,
            'costo': self.costo,
            'prossima_manutenzione_km': self.prossima_manutenzione_km,
            'prossima_manutenzione_data': self.prossima_manutenzione_data.isoformat() if self.prossima_manutenzione_data else None,
            'data_creazione': self.data_creazione.isoformat() if self.data_creazione else None
        }

class VeicoloService:
    def __init__(self, db_manager):
        self.db = db_manager

    def crea_veicolo(self, nome, tipo, anno=None, km_attuali=0, note=None):
        veicolo_id = self.db.inserisci_veicolo(nome, tipo, anno, km_attuali, note)
        return self.get_veicolo_by_id(veicolo_id)

    def get_tutti_veicoli(self):
        rows = self.db.get_veicoli()
        return [Veicolo.from_db_row(row) for row in rows]

    def get_veicolo_by_id(self, veicolo_id):
        row = self.db.get_veicolo_by_id(veicolo_id)
        return Veicolo.from_db_row(row)

    def elimina_veicolo(self, veicolo_id):
        return self.db.elimina_veicolo(veicolo_id)

    def aggiorna_km(self, veicolo_id, nuovi_km):
        return self.db.aggiorna_km_veicolo(veicolo_id, nuovi_km)

class ManutenzioneService:
    def __init__(self, db_manager):
        self.db = db_manager

    def crea_manutenzione(self, veicolo_id, data_intervento, km_intervento,
                         tipo_manutenzione, descrizione=None, costo=None,
                         prossima_manutenzione_km=None, prossima_manutenzione_data=None):

        if isinstance(data_intervento, str):
            data_intervento = datetime.strptime(data_intervento, '%Y-%m-%d').date()

        if isinstance(prossima_manutenzione_data, str) and prossima_manutenzione_data:
            prossima_manutenzione_data = datetime.strptime(prossima_manutenzione_data, '%Y-%m-%d').date()

        manutenzione_id = self.db.inserisci_manutenzione(
            veicolo_id, data_intervento, km_intervento, tipo_manutenzione,
            descrizione, costo, prossima_manutenzione_km, prossima_manutenzione_data
        )
        return manutenzione_id

    def get_manutenzioni_veicolo(self, veicolo_id):
        rows = self.db.get_manutenzioni_by_veicolo(veicolo_id)
        return [Manutenzione.from_db_row(row) for row in rows]

    def get_tutte_manutenzioni(self):
        rows = self.db.get_tutte_manutenzioni()
        manutenzioni = []
        for row in rows:
            manutenzione_data = row[:-1]  # Tutti i campi tranne l'ultimo (nome_veicolo)
            manutenzione = Manutenzione.from_db_row(manutenzione_data)
            if manutenzione:
                manutenzione.nome_veicolo = row[-1]  # Aggiungi il nome del veicolo
                manutenzioni.append(manutenzione)
        return manutenzioni

    def get_prossime_manutenzioni(self):
        rows = self.db.get_prossime_manutenzioni()
        prossime = []
        for row in rows:
            manutenzione_data = row[:-2]  # Tutti i campi tranne gli ultimi due
            manutenzione = Manutenzione.from_db_row(manutenzione_data)
            if manutenzione:
                manutenzione.nome_veicolo = row[-2]
                manutenzione.km_attuali_veicolo = row[-1]
                prossime.append(manutenzione)
        return prossime

    def elimina_manutenzione(self, manutenzione_id):
        return self.db.elimina_manutenzione(manutenzione_id)

    def get_statistiche_spese(self, veicolo_id):
        return self.db.get_statistiche_spese_veicolo(veicolo_id)

# Tipi di manutenzione predefiniti
TIPI_MANUTENZIONE = [
    'Cambio olio motore',
    'Cambio filtro olio',
    'Cambio filtro aria',
    'Cambio filtro carburante',
    'Cambio gomme',
    'Equilibratura e convergenza',
    'Controllo freni',
    'Cambio pastiglie freni',
    'Cambio dischi freni',
    'Revisione generale',
    'Tagliando',
    'Cambio batteria',
    'Controllo climatizzatore',
    'Cambio catena distribuzione',
    'Cambio cinghia distribuzione',
    'Controllo sospensioni',
    'Altro'
]

# Tipi di veicoli predefiniti
TIPI_VEICOLI = [
    'Auto',
    'Moto',
    'Scooter',
    'Bicicletta',
    'Camper',
    'Furgone',
    'Autocarro',
    'Quad',
    'Altro'
]