class Kassapaate:
    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0
        self.e_hinta = 240
        self.m_hinta = 400

    def syo_edullisesti_kateisella(self, maksu):
        if maksu >= self.e_hinta:
            self.kassassa_rahaa += self.e_hinta
            self.edulliset += 1
            return maksu - self.e_hinta
        else:
            return maksu

    def syo_maukkaasti_kateisella(self, maksu):
        if maksu >= self.m_hinta:
            self.kassassa_rahaa += self.m_hinta
            self.maukkaat += 1
            return maksu - self.m_hinta
        else:
            return maksu

    def syo_edullisesti_kortilla(self, kortti):
        if kortti.saldo >= self.e_hinta:
            kortti.ota_rahaa(self.e_hinta)
            self.edulliset += 1
            return True
        else:
            return False

    def syo_maukkaasti_kortilla(self, kortti):
        if kortti.saldo >= self.m_hinta:
            kortti.ota_rahaa(self.m_hinta)
            self.maukkaat += 1
            return True
        else:
            return False

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.kassassa_rahaa += summa
        else:
            return

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100
