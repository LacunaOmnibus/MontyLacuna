
.. _translatable_types:

types
=====

Several types of resources in the game have both a human-readable name, which 
you'll be used to seeing from use in the game, as well as a system name.  The 
system name is often what needs to be passed to various methods, but since 
you, the user, are familiar with the human readable names, it can be difficult 
to remember what the @#$% correct system name is.

The types.Translator class allows us to translate from various spellings that 
will be commonly passed in by the user, into the correct system name, saving 
the user from having to look up, once again, what the system name for "Placebo 
IV" is.

Resources that don't have a listed translation probably don't need one (a 
barge is a barge, and nobody's going to spell it any differently).  All names 
are case insensitive, so if the user passes in "barge" or "Barge" or "bArGe", 
it will be recognized.

.. _ship_translations:

Ship Translations
-----------------

============================ ============================= ============== 
Human                        System                        Translations  
============================ ============================= ============== 
Barge                        barge                                          
Bleeder                      bleeder                                      
Cargo Ship                   cargo_ship                    cargo, "cargo ship"                  
Colony Ship                  colony_ship                                      
Detonator                    detonator                                      
Dory                         dory
Drone                        drone
Excavator                    excavator
Fighter                      fighter
Fissure Sealer               fissure_sealer                fissure
Freighter                    freighter
Galleon                      galleon
Gas Giant Settlement Ship    gas_giant_settlement_ship     gg, "gas giant", "gas giant settlement ship"
Hulk                         hulk                                           
Hulk Fast                    hulk_fast                     "hulk fast"                      
Hulk Huge                    hulk_huge                     "hulk huge"                      
Mining Platform Ship         mining_platform_ship          min, minplat, "min plat", "mining platform ship"                                 
Observatory Seeker           observatory_seeker            obs, "obs seeker", "observatory seeker"
Placebo                      placebo                       placebo1, "placebo 1"
Placebo II                   placebo2                      "placebo 2", placeboII, "placebo II"             
Placebo III                  placebo3                      "placebo 3", placeboIII, "placebo III"             
Placebo IV                   placebo4                      "placebo 4", placeboIV, "placebo IV"             
Placebo V                    placebo5                      "placebo 5", placeboV, "placebo V"             
Placebo VI                   placebo6                      "placebo 6", placeboVI, "placebo VI"             
Probe                        probe                                           
Probe                        probe                                           
Scanner                      scanner                                           
Scow                         scow                                           
Scow Fast                    scow_fast                     "scow fast"            
Scow Large                   scow_large                    "scow large"             
Scow Mega                    scow_mega                     "scow mega"            
Security Ministry Seeker     security_ministry_seeker      sec, "secmin seeker", "sec min seeker", "security ministry seeker"                                     
Short Range Colony Ship      short_range_colony_ship       srcs, "short range colony", "short range colony ship"
Smuggler Ship                smuggler_ship                 smug, smuggler, "smuggler ship"                           
Snark                        snark                         snark1, "snark 1"                  
Snark II                     snark2                        "snark 2"                   
Snark III                    snark3                        "snark 3"                   
Space Station Hull           space_station                 hull, ss, "ss hull", "space station", "space station hull"                          
Spaceport Seeker             spaceport_seeker              sp, "sp seeker", "port seeker", "spaceport seeker", "space port seeker"                             
Spy Pod                      spy_pod                       "spy pod"                    
Spy Shuttle                  spy_shuttle                                           
Stake                        stake
Supply Pod                   supply_pod                    supply, supply1, "supply 1", "supply pod", "supply pod 1"                       
Supply Pod II                supply_pod2                   supply2, "supply 2", "supply pod 2", supplyII, "supply II", "supply pod II" 
Supply Pod III               supply_pod3                   supply3, "supply 3", "supply pod 3", supplyIII, "supply III", "supply pod III" 
Supply Pod IV                supply_pod4                   supply4, "supply 4", "supply pod 4", supplyIV, "supply IV", "supply pod IV" 
Supply Pod V                 supply_pod5                   supply5, "supply 5", "supply pod 5", supplyV, "supply V", "supply pod V" 
Surveyor                     surveyor                      
Sweeper                      sweeper                                           
Terraforming Platform Ship   terraforming_platform_ship    terra, "terra plat", "terraforming platform ship"                                       
Thud                         thud                                           
============================ ============================= ============== 

.. _ore_translations:

Ore Translations
----------------

============================ ============================= ============== 
Human                        System                        Translations  
============================ ============================= ============== 
Anthracite                   anthracite                    anth, anthra 
Bauxite                      bauxite                       baux
Beryl                        beryl 
Chromite                     chromite                      chrom, chrome
Chalcopyrite                 chalcopyrite
Fluorite                     fluorite                      flor, flour, fluor, floride, flouride, fluoride
Galena                       galena                        gal
Goethite                     goethite                      goeth
Gold                         gold 
Gypsum                       gypsum 
Halite                       halite
Kerogen                      kerogen                       kero
Magnetite                    magnetite                     mag
Methane                      methane 
Monazite                     monazite                      mona 
Rutile                       rutile 
Sulfur                       sulfur
Trona                        trona 
Uraninite                    uraninite                     uran, urin, urine (because somebody's going to do that.)
Zircon                       zircon
============================ ============================= ============== 

.. automodule:: lacuna.types
   :members:
   :show-inheritance:

