class Weblinks(object):
    def __init__(self):
        self.links = {
            'Lead_kg': 'http://www.carexcanada.ca/en/lead/', 
            'Nick_kg': 'http://www.carexcanada.ca/en/nickel/', 
            'Dichlor_kg': 'http://www.carexcanada.ca/en/dichloromethane/', 
            'Cadm_kg': 'http://www.carexcanada.ca/en/cadmium/', 
            'Chrys_kg': 'http://www.carexcanada.ca/en/polycyclic_aromatic_hydrocarbons/', 
            'Chlor_kg': 'http://www.carexcanada.ca/en/chloroform/', 
            'Perc_kg': 'http://www.carexcanada.ca/en/tetrachloroethylene/', 
            'BBF_kg': 'http://www.carexcanada.ca/en/polycyclic_aromatic_hydrocarbons/', 
            'PCB_kg': 'http://www.carexcanada.ca/en/polychlorinated_biphenyls/', 
            'Pm25_kg': 'http://www.carexcanada.ca/en/particulate_air_pollution/', 
            'Indeno_kg': 'http://www.carexcanada.ca/en/polycyclic_aromatic_hydrocarbons/', 
            'BAP_kg': 'http://www.carexcanada.ca/en/polycyclic_aromatic_hydrocarbons/', 
            'Ethylb_kg': 'http://www.carexcanada.ca/en/ethylbenzene/', 
            'Acet_kg': 'http://www.carexcanada.ca/en/acetaldehyde/', 
            'Chrom_kg': 'http://www.carexcanada.ca/en/chromium_(hexavalent)/', 
            'Form_kg': 'http://www.carexcanada.ca/en/formaldehyde/', 
            'Ars_kg': 'http://www.carexcanada.ca/en/arsenic/', 
            'Buta_kg': 'http://www.carexcanada.ca/en/1,3-butadiene/', 
            'Hexcr_kg': 'http://www.carexcanada.ca/en/chromium_(hexavalent)/', 
            'BAA_kg': 'http://www.carexcanada.ca/en/polycyclic_aromatic_hydrocarbons/', 
            'Benz_kg': 'http://www.carexcanada.ca/en/benzene/', 
            'BKF_kg': 'http://www.carexcanada.ca/en/polycyclic_aromatic_hydrocarbons/',
            'Tcdd_kg': 'http://www.carexcanada.ca/en/2,3,7,8-tetrachlorodibenzo-para-dioxin/'
}

    def getlink(self, substance):
        if substance in self.links:
            return self.links[substance]
        else:
            return None
