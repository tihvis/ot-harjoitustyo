import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_kassassa_oikea_maara_rahaa_alussa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_alussa_ei_myytyja_edullisia_lounaita(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_alussa_ei_myytyja_maukkaita_lounaita(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullisen_lounaan_ostaminen_kateisella_onnistuu(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_vaihtoraha_oikein_kun_ostaa_edullisen_lounaan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_kassan_rahamaara_kasvaa_kun_ostaa_edullisen_lounaan_kateisella(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_edullisen_lounaan_ostaminen_ei_onnistu_jos_kateista_liian_vahan(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukkaaan_lounaan_ostaminen_kateisella_onnistuu(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
                # self.kassapaate.kassassa_rahaa = 100000
        # self.kassapaate.edulliset = 0
        # self.kassapaate.maukkaat = 0
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_vaihtoraha_oikein_kun_ostaa_maukkaan_lounaan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)


    def test_kassan_rahamaara_kasvaa_kun_ostaa_maukkaan_lounaan_kateisella(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_maukkaan_lounaan_ostaminen_ei_onnistu_jos_kateista_liian_vahan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullisen_lounaan_ostaminen_kortilla_onnistuu_jos_saldoa_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)

    def test_edullisen_lounaan_ostaminen_kortilla_ei_onnistu_jos_saldoa_liian_vahan(self):
        kortti = Maksukortti(200)

        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(kortti), False)

    def test_edullisen_lounaan_ostaminen_kortilla_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullisen_lounaan_ostaminen_kortilla_ei_muuta_kateisen_maaraa_kassassa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukkaan_lounaan_ostaminen_kortilla_onnistuu_jos_saldoa_tarpeeksi(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)

    def test_maukkaann_lounaan_ostaminen_kortilla_ei_onnistu_jos_saldoa_liian_vahan(self):
        kortti = Maksukortti(200)
        
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), False)

    def test_maukkaann_lounaan_ostaminen_kortilla_kasvattaa_myytyjen_lounaiden_maaraa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukkaan_lounaan_ostaminen_kortilla_ei_muuta_kateisen_maaraa_kassassa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_saldon_lataaminen_kortille_onnistuu_positiivisella_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 2000)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 102000)

    def test_saldon_lataaminen_kortille_ei_onnistu_negatiivisella_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -200)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_rahamaara_euroina_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
