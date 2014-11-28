
.. _tle_modules_index:

TLE Modules
===========

These modules mirror the published TLE API.  Some of the modules do contain 
methods that are not part of that API, but all API methods are reflected in 
these modules, using the same argument prototypes as the published API.

.. toctree::
   :maxdepth: 2

   alliance
   body
   building
   captcha
   empire
   inbox
   map
   stats

CAVEAT - There are a few spots where the TLE API mirroring is incomplete:

- Buildings

  - I more or less ran out of steam while working on the trade and transporter 
    buildings, and since the listed methods didn't look to me like the sorts 
    of things anybody would need to do much scripting with anyway, I skipped 
    them.  They should be completed at some point, but for now they don't 
    exist.

  - :ref:`bldg_trade`

    - create_supply_chain()
    - delete_supply_chain()
    - update_supply_chain()
    - update_waste_chain()
    - add_supply_ship_to_fleet()
    - add_waste_ship_to_fleet()
    - remove_supply_ship_from_fleet()
    - remove_waste_ship_from_fleet()
    - report_abuse()

  - :ref:`bldg_transporter`

    - trade_one_for_one()
    - report_abuse()

  - Announcement
  - Payment

    - There are no plans to add either Announcement or Payment modules to 
      MontyLacuna.

