
import lacuna.exceptions as err

class Translator():
    """ Translates the human name and various misspellings of common 
    resources into the appropriate TLE system name.
    """

    def translate_oretype( self, type:str ):
        """ Translates recognized ore type misspellings into the system ore 
        name.

        Args:
            type (str): The mispeling or tyop to correct.
        Returns:
            str: the system ore name associated with the type passed in if it 
                was recognized.
        Raises:
            KeyError: If the passed-in string isn't recognized

        Example::

            tr = lacuna.types.Translator()
            print( tr.translate_oretype('Anth') )  # 'anthracite'
        """
        system = [
            "anthracite", "bauxite", "beryl", "chromite", "chalcopyrite", "fluorite", "galena", "goethite", "gold", "gypsum",
            "halite", "kerogen", "magnetite", "methane", "monazite", "rutile", "sulfur", "trona", "uraninite", "zircon",
        ]
        if type.lower() in system:
            return type.lower()

        trans = {
            "anth": "anthracite",
            "anthra": "anthracite",
            "baux": "bauxite", 
            "chrom": "chromite", 
            "chrome": "chromite", 
            "chalc": "chalcopyrite",
            "chalk": "chalcopyrite",
            "flor": "fluorite", 
            "fluor": "fluorite", 
            "flour": "fluorite", 
            "fluoride": "fluorite", 
            "floride": "fluorite", 
            "flouride": "fluorite", 
            "gal": "galena", 
            "goeth": "goethite", 
            "kero": "kerogen", 
            "mag": "magnetite", 
            "mona": "monazite", 
            "uran": "uraninite", 
            "urin": "uraninite", 
            "urine": "uraninite",   # you know somebody's going to type that 'e' out of habit.
        }
        if type.lower() in trans:
            return trans[ type.lower() ]
        raise KeyError( "{} is not a valid ore type.".format(type) )


    def translate_shiptype( self, type:str ):
        """ Translates recognized ship type misspellings into the system ship 
        name.

        Args:
            type (str): generally passed in by the user.

        Returns:
            str: the system ship name associated with the type passed in if it 
                was recognized.
        Raises:
            lacuna.exceptions.NoSuchShipError: if the passed-in string was not 
                recognized.
        """

        system = [
            'barge', 'bleeder', 'cargo_ship', 'colony_ship', 'detonator', 'dory', 
            'drone', 'excavator', 'fighter', 'fissure_sealer', 'freighter', 
            'galleon', 'gas_giant_settlement_ship', 'hulk', 'hulk_fast', 
            'hulk_huge', 'mining_platform_ship', 'observatory_seeker', 'placebo',
            'placebo2', 'placebo3', 'placebo4', 'placebo5', 'placebo6', 'probe',
            'scanner', 'scow', 'scow_fast', 'scow_large', 'scow_mega',
            'security_ministry_seeker', 'short_range_colony_ship', 'smuggler_ship',
            'snark', 'snark2', 'snark3', 'space_station', 'spaceport_seeker',
            'spy_pod', 'spy_shuttle', 'stake', 'supply_pod', 'supply_pod2',
            'supply_pod3', 'supply_pod4', 'supply_pod5', 'surveyor', 'sweeper',
            'terraforming_platform_ship', 'thud',
        ]
        if type.lower() in system:
            return type.lower()

        trans = {
            "cargo": "cargo_ship",
            "cargo ship": "cargo_ship",
            "colony": "colony_ship",
            "colony ship": "colony_ship",
            "excav": "excavator",
            "fissure": "fissure_sealer",
            "fissure sealer": "fissure_sealer",
            "gg": "gas_giant_settlement_ship",
            "gas ": "gas_giant_settlement_ship",
            "gas giant": "gas_giant_settlement_ship",
            "gas giant settlement ship": "gas_giant_settlement_ship",
            "hulk fast": "hulk_fast",
            "hulk huge": "hulk_huge",
            "min": "mining_platform_ship",
            "minplat": "mining_platform_ship",
            "min plat": "mining_platform_ship",
            "mining platform ship": "mining_platform_ship",
            "obs": "observatory_seeker",
            "obs seeker": "observatory_seeker",
            "observatory seeker": "observatory_seeker",
            "placebo1": "placebo",
            "placebo 1": "placebo",
            "placebo 2": "placebo2",
            "placeboII": "placebo2",
            "placebo II": "placebo2",
            "placebo 3": "placebo3",
            "placeboIII": "placebo3",
            "placebo III": "placebo3",
            "placebo 4": "placebo4",
            "placeboIV": "placebo4",
            "placebo IV": "placebo4",
            "placebo 5": "placebo5",
            "placeboV": "placebo5",
            "placebo V": "placebo5",
            "placebo 6": "placebo6",
            "placeboVI": "placebo6",
            "placebo VI": "placebo6",
            "scow fast": "scow_fast",
            "scow mega": "scow_mega",
            "sec": "security_ministry_seeker",
            "secmin seeker": "security_ministry_seeker",
            "sec min seeker": "security_ministry_seeker",
            "security ministry seeker": "security_ministry_seeker",
            "srcs": "short_range_colony_ship",
            "short range colony": "short_range_colony_ship",
            "short range colony ship": "short_range_colony_ship",
            "smug": "smuggler_ship",
            "smuggler": "smuggler_ship",
            "smuggler ship": "smuggler_ship",
            "snark1": "snark",
            "snark 1": "snark",
            "snark 2": "snark2",
            "snark 3": "snark3",
            "ss": "space_station",
            "hull": "space_station",
            "ss hull": "space_station",
            "space station": "space_station",
            "space station hull": "space_station",
            "sp": "spaceport_seeker",
            "sp seeker": "spaceport_seeker",
            "port seeker": "spaceport_seeker",
            "spaceport seeker": "spaceport_seeker",
            "space port seeker": "spaceport_seeker",
            "spy pod": "spy_pod",
            "shuttle": "spy_shuttle",
            "spy shuttle": "spy_shuttle",
            "supply": "supply_pod",
            "supply1": "supply_pod",
            "supplyI": "supply_pod",
            "supply 1": "supply_pod",
            "supply I": "supply_pod",
            "supply pod": "supply_pod",
            "supply pod 1": "supply_pod",
            "supply pod I": "supply_pod",
            "supply2": "supply_pod2",
            "supply 2": "supply_pod2",
            "supply pod 2": "supply_pod2",
            "supplyII": "supply_pod2",
            "supply II": "supply_pod2",
            "supply pod II": "supply_pod2",
            "supply3": "supply_pod3",
            "supply 3": "supply_pod3",
            "supply pod 3": "supply_pod3",
            "supplyIII": "supply_pod3",
            "supply III": "supply_pod3",
            "supply pod III": "supply_pod3",
            "supply4": "supply_pod4",
            "supply 4": "supply_pod4",
            "supply pod 4": "supply_pod4",
            "supplyIV": "supply_pod4",
            "supply IV": "supply_pod4",
            "supply pod IV": "supply_pod4",
            "supply5": "supply_pod5",
            "supply 5": "supply_pod5",
            "supply pod 5": "supply_pod5",
            "supplyV": "supply_pod5",
            "supply V": "supply_pod5",
            "supply pod V": "supply_pod5",
            "terra": "terraforming_platform_ship",
            "terra plat": "terraforming_platform_ship",
            "terraforming platform ship": "terraforming_platform_ship",
        }
        if type.lower() in trans:
            return trans[ type.lower() ]
        raise err.NoSuchShipError( "{} is not a valid ship type.".format(type) )

    def translate_assgtype( self, type:str ):
        """ Translates recognized spy assignment misspellings into the system 
        spy assignment name.

        Args:
            type (str): generally passed in by the user.
        Returns:
            str: the system spy assignment name associated with the type passed 
                in if it was recognized.
        Raises:
            KeyError: If the passed-in string was not recognized.
        """
        system = [
            "Idle",
            "Bugout",
            "Counter Espionage",
            "Security Sweep",
            "Intel Training",
            "Mayhem Training",
            "Politics Training",
            "Theft Training",
            "Political Propaganda",
            "Gather Resource Intelligence",
            "Gather Empire Intelligence",
            "Gather Operative Intelligence",
            "Hack Network 19",
            "Sabotage Probes",
            "Rescue Comrades",
            "Sabotage Resources",
            "Appropriate Resources",
            "Assassinate Operatives",
            "Sabotage Infrastructure",
            "Sabotage Defenses",
            "Sabotage BHG",
            "Incite Mutiny",
            "Abduct Operatives",
            "Appropriate Technology",
            "Incite Rebellion",
            "Incite Insurrection",

        ]
        if type.title() in system:
            return type.title()

        trans = {
            "counter": "Counter Espionage",
            "sweep": "Security Sweep",
            "int train": "Intel Training",
            "inttrain": "Intel Training",
            "may train": "Mayhem Training",
            "maytrain": "Mayhem Training",
            "poli train": "Politics Training",
            "politrain": "Politics Training",
            "pol train": "Politics Training",
            "poltrain": "Politics Training",
            "theft train": "Theft Training",
            "thefttrain": "Theft Training",
            "poli prop": "Political Propaganda",
            "pol prop": "Political Propaganda",
            "prop": "Political Propaganda",
            "pp": "Political Propaganda",
            "get res int": "Gather Resource Intelligence",
            "get resint": "Gather Resource Intelligence",
            "get emp int": "Gather Empire Intelligence",
            "get empint": "Gather Empire Intelligence",
            "get op int": "Gather Operative Intelligence",
            "get opint": "Gather Operative Intelligence",
            "hack": "Hack Network 19",
            "rescue": "Rescue Comrades",
            "app res": "Appropriate Resources",
            "steal res": "Appropriate Resources",
            "app tech": "Appropriate Technology",
            "steal tech": "Appropriate Technology",
            "ass op": "Assassinate Operatives",
            "assop": "Assassinate Operatives",
            "kill": "Assassinate Operatives",
            "sab bhg": "Sabotage BHG",
            "sab defenses": "Sabotage Defenses",
            "sab defense": "Sabotage Defenses",
            "sab def": "Sabotage Defenses",
            "sabdef": "Sabotage Defenses",
            "sab infra": "Sabotage Infrastructure",
            "sab inf": "Sabotage Infrastructure",
            "sabinf": "Sabotage Infrastructure",
            "sab probes": "Sabotage Probes",
            "sab probe": "Sabotage Probes",
            "sabprobe": "Sabotage Probes",
            "sab resources": "Sabotage Resources",
            "sab resource": "Sabotage Resources",
            "sab res": "Sabotage Resources",
            "sabres": "Sabotage Resources",
            "mutiny": "Incite Mutiny",
            "abd ops": "Abduct Operatives",
            "abd op": "Abduct Operatives",
            "ab ops": "Abduct Operatives",
            "ab op": "Abduct Operatives",
            "kidnap": "Abduct Operatives",
            "rebellion": "Incite Rebellion",
            "rebel": "Incite Rebellion",
            "insurrect": "Incite Insurrection",
            "insurect": "Incite Insurrection",  # cause somebody's going to do that.
        }
        if type.lower() in trans:
            return trans[ type.lower() ]
        raise KeyError( "{} is not a valid ore type.".format(type) )


